import json
import re
from typing import Any, Dict, List, Union


def clean_numeric_fields(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Clean numeric fields like '2,989,045' → '2989.045'."""
    pattern = re.compile(r'^[\d,]+(\.\d+)?$')  # matches numbers with commas and optional decimals

    def clean_value(val: Any) -> Any:
        if isinstance(val, str) and pattern.match(val):
            return val.replace(',', '')
        return val

    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                for key, value in item.items():
                    item[key] = clean_value(value)
    elif isinstance(data, dict):
        for key, value in data.items():
            data[key] = clean_value(value)

    return data


def extract_json_from_response_text(response_text: str) -> Union[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
    """從 LLM 回應字串中提取 JSON 或回傳錯誤物件。"""

    text = response_text.strip()

    # remove markdown code fences
    if text.startswith('```json'):
        text = text[7:]
    if text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    text = text.strip()

    # Try direct parse
    try:
        data = json.loads(text)
        return clean_numeric_fields(data)
    except Exception:
        pass

    # Try to extract first JSON array
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(0))
            return clean_numeric_fields(data)
        except Exception:
            pass

    # Try to extract first JSON object
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        try:
            data = json.loads(match.group(0))
            return clean_numeric_fields(data)
        except Exception:
            pass

    # Fallback
    return {
        "error": "LLM 回應不是有效 JSON",
        "response": text[:500] + ('...' if len(text) > 500 else '')
    }
