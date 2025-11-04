import threading
import logging
import os
from typing import Tuple, Optional
import google.generativeai as genai
import google.auth
from PIL import Image
from pdf2image import convert_from_path

MODEL = "gemini-2.5-pro"

_model_instance = None
_credentials = None
_lock = threading.Lock()


def get_model():
    """
    取得 Gemini 模型實例
    優先使用 Cloud Run 的默認憑證（透過環境變數或服務帳戶）
    如果沒有默認憑證，則嘗試從文件載入
    """
    global _model_instance, _credentials
    if _model_instance is None:
        with _lock:
            if _model_instance is None:
                try:
                    # 優先使用 Cloud Run 的默認憑證（Application Default Credentials）
                    # 在 Cloud Run 上，服務帳戶會自動透過環境變數提供
                    credentials, project = google.auth.default()
                    logging.info("✅ 使用 Application Default Credentials (Cloud Run)")
                    genai.configure(credentials=credentials)
                except google.auth.exceptions.DefaultCredentialsError:
                    # 如果沒有默認憑證，嘗試從文件載入（本地開發用）
                    service_account_file = os.environ.get(
                        'GOOGLE_APPLICATION_CREDENTIALS',
                        'fileanalyzer-463911-e71c7f7288ad.json'
                    )
                    if os.path.exists(service_account_file):
                        logging.info(f"✅ 從文件載入憑證: {service_account_file}")
                        _credentials, project = google.auth.load_credentials_from_file(service_account_file)
                        genai.configure(credentials=_credentials)
                    else:
                        logging.error("❌ 無法找到 Google 憑證，請設置 GOOGLE_APPLICATION_CREDENTIALS 環境變數")
                        raise
                
                _model_instance = genai.GenerativeModel(MODEL)
    return _model_instance


def call_gemini(prompt: str, image_path: Optional[str] = None, max_retries: int = 3) -> Tuple[str, int]:
    model = get_model()
    generation_config = {
        "temperature": 0.1,
        "top_p": 0.8,
        "top_k": 40,
        "max_output_tokens": 30000,
    }

    for attempt in range(max_retries):
        try:
            # --- Image handling ---
            if image_path:
                ext = os.path.splitext(image_path)[1].lower()
                if ext == ".pdf":
                    images = convert_from_path(image_path, first_page=1, last_page=1)
                    img = images[0]
                else:
                    img = Image.open(image_path)
                response = model.generate_content([prompt, img], generation_config=generation_config)
            else:
                response = model.generate_content(prompt, generation_config=generation_config)

            # --- Defensive checks ---
            if not response or not hasattr(response, "candidates") or not response.candidates:
                logging.warning("⚠️ Gemini returned an empty or invalid response object.")
                return "NO_RESPONSE", 0

            candidate = response.candidates[0]
            finish_reason = getattr(candidate, "finish_reason", None)

            # --- Handle safety stop (finish_reason = 2) ---
            if finish_reason == 2:
                logging.warning("⚠️ Gemini response blocked by safety filters (finish_reason=2).")
                return "SAFETY_BLOCKED", 0

            # --- Extract text safely ---
            result = getattr(response, "text", None)
            if not result:
                # fallback: extract manually
                try:
                    if candidate.content.parts:
                        result = "".join(part.text for part in candidate.content.parts if hasattr(part, "text"))
                    else:
                        result = ""
                except Exception as e:
                    logging.error(f"Error extracting text from response: {e}")
                    result = ""

            result = result.strip()

            # --- Token usage ---
            tokens_used = 0
            if hasattr(response, "usage_metadata"):
                usage_metadata = response.usage_metadata
                if hasattr(usage_metadata, "total_token_count"):
                    tokens_used = usage_metadata.total_token_count
                elif hasattr(usage_metadata, "total_tokens"):
                    tokens_used = usage_metadata.total_tokens
            else:
                text_length = len(prompt) + len(result)
                tokens_used = max(1, text_length // 4)

            return result, tokens_used

        except Exception as e:
            logging.error(f"Attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt == max_retries - 1:
                raise
            continue

    return "", 0
