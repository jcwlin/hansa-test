import os
import io
import base64
import logging
from typing import Optional, Tuple
import requests
from PIL import Image
from pdf2image import convert_from_path


OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
DEFAULT_MODEL = os.environ.get('OLLAMA_VLM_MODEL', 'llava:latest')


def _image_to_base64(image: Image.Image) -> str:
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')


def _load_first_page_as_image(path: str) -> Image.Image:
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        images = convert_from_path(path, first_page=1, last_page=1)
        return images[0]
    return Image.open(path)


def call_ollama_vlm(file_path: str, field_name: str, lang: str = 'zh', model: Optional[str] = None) -> Tuple[str, int]:
    """呼叫 Ollama 視覺模型，回傳 (文字, tokens)。
    目標：依據欄位名稱 field_name，從 file_path 影像/PDF 中擷取對應資訊。
    """
    model_name = model or DEFAULT_MODEL
    try:
        image = _load_first_page_as_image(file_path)
        img_b64 = _image_to_base64(image)

        # CHANGE THIS SECTION - Add specific instructions for number formatting
        prompt = {
            'zh': f"""請依據文件擷取欄位「{field_name}」。
注意事項：
- 保留原始數字格式（包含逗號和小數點，例如：1,999.858）
- 不要改變數字格式或四捨五入
- 若無法判定請回傳空字串""",
            'en': f"""Extract the field '{field_name}' from the document.
Important:
- Preserve the original number format (including commas and decimals, e.g., 1,999.858)
- Do not reformat or round numbers
- If not found, return an empty string""",
        }.get(lang, f"""Extract the field '{field_name}' from the document.
Important: Preserve original number format including commas and decimals (e.g., 1,999.858).
If not found, return an empty string.""")

        payload = {
            'model': model_name,
            'prompt': prompt,
            'images': [img_b64],
            'stream': False
        }
        resp = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        text = (data.get('response') or '').strip()
        tokens = int(data.get('eval_count') or 0)
        return text, tokens
    except Exception as e:
        logging.error(f"Ollama 呼叫失敗: {e}")
        return '', 0


def get_ollama_models() -> list:
    """列出本機 Ollama 已安裝模型名稱清單"""
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=30)
        resp.raise_for_status()
        data = resp.json() or {}
        models = data.get('models') or []
        names = []
        for m in models:
            name = m.get('name') or m.get('model')
            if name:
                names.append(name)
        return sorted(list(dict.fromkeys(names)))
    except Exception as e:
        logging.error(f"取得 Ollama 模型清單失敗: {e}")
        return []


