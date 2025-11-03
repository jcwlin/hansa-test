import os
import re
from typing import List, Dict, Any, Tuple, Optional
import logging
import re
from typing import List, Dict, Any
import app

from analyzers.clients.gemini_client import call_gemini
from analyzers.common.json_utils import extract_json_from_response_text


CARGO_COLUMNS_ORDER = [
    'Cargo #', 'BL number', 'B/L quantity (MT)', 'B/L split quantity (MT)',
    'Cargo name', 'Charterer', 'Consignee, order to', 'Notify',
    'Stow', 'LoadPort', 'Disch. Port', 'OBL release date', 'Release cargo against', '__filename__'
]


def is_missing(value: Any) -> bool:
    return value is None or str(value).strip() == '' or str(value).lower() in ['null', 'n/a']


def fix_ocr_errors(text: str) -> str:
    text = re.sub(r'\bRow\b', 'Stow', text, flags=re.IGNORECASE)
    return text


def safe_float(val) -> float:
    try:
        if isinstance(val, str):
            val = val.replace(',', '')
        return float(val)
    except Exception:
        return 0.0


def enforce_column_order_list(data_list: List[Dict[str, Any]], keep_filename: bool = False) -> List[Dict[str, Any]]:
    if not data_list:
        return data_list
    ordered_data = []
    for item in data_list:
        ordered_item = {}
        for col in CARGO_COLUMNS_ORDER:
            if col in item:
                if col == '__filename__' and keep_filename:
                    ordered_item['File name'] = item[col]
                elif col != '__filename__':  # 避免添加 __filename__ 欄位
                    ordered_item[col] = item[col]
        for key, value in item.items():
            if key not in ordered_item and key != '__filename__':  # 排除 __filename__
                ordered_item[key] = value
        ordered_data.append(ordered_item)
    return ordered_data


def sort_by_bl_number_list(data_list):
    """Sort list data by Cargo # first, then BL number"""

    def sort_key(item):
        # Get cargo number
        cargo_num = item.get('Cargo #', '')

        # Convert cargo # to integer for proper numeric sorting
        try:
            if cargo_num and str(cargo_num).strip().lower() != 'total':
                cargo_int = int(''.join(filter(str.isdigit, str(cargo_num))))
            else:
                cargo_int = 999999  # Put "Total" and empty at end
        except:
            cargo_int = 999999

        # Get BL number for secondary sorting
        bl_num = item.get('BL number', '') or ''

        # Normalize BL number for sorting (remove dots, extra spaces)
        bl_normalized = bl_num.replace('.', ' ').replace('  ', ' ').strip()

        return (cargo_int, bl_normalized)

    # Sort by cargo # first, then BL number
    return sorted(data_list, key=sort_key)


def process_same_category_bl(data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not data_list:
        return data_list
    bl_groups = {}
    for i, item in enumerate(data_list):
        bl_number = item.get('BL number', '').strip()
        if not bl_number:
            continue
        if len(bl_number) >= 13:
            try:
                group_key = bl_number[9:11]
                if group_key not in bl_groups:
                    bl_groups[group_key] = []
                bl_groups[group_key].append((i, item))
            except (IndexError, ValueError):
                continue
    for group_key, group_items in bl_groups.items():
        if len(group_items) > 1:
            group_items.sort(key=lambda x: x[1].get('BL number', ''))
            for idx, (original_index, item) in enumerate(group_items):
                if idx > 0:
                    if 'B/L quantity (MT)' in item:
                        item['B/L quantity (MT)'] = None
                    if 'Cargo #' in item:
                        item['Cargo #'] = None
    return data_list


def vlm_fill_field(file_path: str, field_name: str, lang: str = 'zh') -> Tuple[str, int]:
    if field_name == 'OBL release date':
        prompt = f"""
請仔細檢查這份文件圖片，找出「OBL release date（提單簽發日期）」。
請特別注意文件底部的 "Dated at" 區塊或簽發日期相關資訊。
只回傳 YYYY-MM-DD 格式的日期，如果無法明確判斷請回傳 null。
不要有任何多餘的說明或文字。
"""
    else:
        prompt = f"請根據這份文件圖片，找出「{field_name}」，只回傳該欄位的值，不要有多餘說明或文字。"
    result, tokens = call_gemini(prompt, image_path=file_path)
    return (result.strip() if result else ''), tokens


def analyze_text_with_prompt(text: str, prompt_template: str):
    if '{text}' not in prompt_template:
        prompt_str = f"{prompt_template}\n\n檔案內容：\n{text}"
    else:
        prompt_str = prompt_template.replace('{text}', text)
    response_text, tokens_used = call_gemini(prompt_str)
    result = extract_json_from_response_text(response_text)
    return result, tokens_used


from typing import List, Dict, Any
import re


def cargo_bl_postprocess(all_data: List[Dict[str, Any]], keep_filename: bool = False) -> List[Dict[str, Any]]:
    # Step 0: Remove any previous total rows
    all_data = [row for row in all_data if str(row.get('Cargo #', '')).strip().lower() != 'total']

    # Remove copy_type column from all records
    for item in all_data:
        if 'copy_type' in item:
            del item['copy_type']

    # Print collected data before postprocessing
    print("=== SID in cargo_bl_postprocess ===")

    # Step 1: Normalize BL number prefixes (FLOY → FLO for consistent sorting)
    for item in all_data:
        bl_num = item.get('BL number', '')
        if bl_num and 'FLOY' in bl_num:
            item['BL number'] = bl_num.replace('FLOY', 'FLO')
            logging.info(f"Normalized BL: {bl_num} → {item['BL number']}")  # Changed here

    # Step 2: Fix OCR errors
    for item in all_data:
        for key, value in item.items():
            if isinstance(value, str):
                item[key] = fix_ocr_errors(value)

    # Step 3: Clean and validate B/L quantities
    for item in all_data:
        def clean_number(val):
            if isinstance(val, str):
                return val.replace('MTS', '').replace('MT', '').replace('tons', '').replace('噸', '').replace(',', '').strip()
            return val

        bl_qty_clean = clean_number(item.get('B/L quantity (MT)'))
        split_qty_clean = clean_number(item.get('B/L split quantity (MT)'))

        # Convert to float
        try:
            bl_val = float(bl_qty_clean) if bl_qty_clean not in [None, '', 'null', 'n/a'] else None
        except Exception:
            bl_val = None

        try:
            split_val = float(split_qty_clean) if split_qty_clean not in [None, '', 'null', 'n/a'] else None
        except Exception:
            split_val = None

        # Validate split quantity
        if split_val is not None and bl_val is not None:
            # If split > B/L, clear it
            if split_val > bl_val + 0.001:
                logging.warning(f"❌ Invalid split for {item.get('BL number')}: {split_val} > {bl_val}")  # Changed here
                split_val = None
            # If split == B/L, clear it (suspicious)
            elif abs(split_val - bl_val) < 0.001:
                logging.warning(f"⚠️ Split equals B/L for {item.get('BL number')}: {split_val} == {bl_val}")  # Changed here
                split_val = None

        # Format quantities with commas
        item['B/L split quantity (MT)'] = f"{split_val:,.3f}" if split_val is not None else None
        item['B/L quantity (MT)'] = f"{bl_val:,.3f}" if bl_val is not None else None

        # Validate OBL release date
        obl_date = item.get('OBL release date')
        if not (isinstance(obl_date, str) and re.match(r'^\d{4}-\d{2}-\d{2}$', obl_date)):
            item['OBL release date'] = None

    # Step 4: Sorting and column enforcement
    all_data = sort_by_bl_number_list(all_data)
    all_data = enforce_column_order_list(all_data, keep_filename)
    # all_data = process_same_category_bl(all_data)  # DISABLED - Keep all B/L quantities

    # Step 5: Add single total row
    total_bl_qty = sum(safe_float(row.get('B/L quantity (MT)', 0)) for row in all_data)
    total_split_qty = sum(safe_float(row.get('B/L split quantity (MT)', 0)) for row in all_data)

    if all_data:
        total_row = {}
        for key in all_data[0].keys():
            if key == 'Cargo #':
                total_row[key] = 'Total'
            elif key == 'B/L quantity (MT)':
                total_row[key] = f"{total_bl_qty:,.3f}"
            elif key == 'B/L split quantity (MT)':
                total_row[key] = f"{total_split_qty:,.3f}"
            else:
                total_row[key] = ''
        all_data.append(total_row)

    return all_data