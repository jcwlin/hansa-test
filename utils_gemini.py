import os
import json
import time
import threading
from google.cloud import aiplatform
from google.oauth2 import service_account
import google.generativeai as genai
import google.auth
from PIL import Image
from pdf2image import convert_from_path
import logging

PROJECT_ID = "fileanalyzer-463911"
LOCATION = "us-central1"
MODEL = "gemini-2.5-pro"

# 全域模型實例，避免重複初始化
_model_instance = None
_credentials = None
_lock = threading.Lock()

def get_model():
    """
    取得單例模型實例，避免重複初始化
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

def call_gemini_api(prompt: str, image_path: str = None, max_retries: int = 3) -> tuple:
    """呼叫 Gemini API，支援 Vision LLM 圖片處理，PDF 會自動轉第一頁圖片"""
    model = get_model()
    for attempt in range(max_retries):
        try:
            generation_config = {
                "temperature": 0.1,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
            if image_path:
                ext = os.path.splitext(image_path)[1].lower()
                if ext == ".pdf":
                    images = convert_from_path(image_path, first_page=1, last_page=1)
                    img = images[0]
                else:
                    img = Image.open(image_path)
                response = model.generate_content(
                    [prompt, img],
                    generation_config=generation_config
                )
            else:
                response = model.generate_content(
                    prompt,
                    generation_config=generation_config
                )
            result = response.text.strip() if hasattr(response, 'text') else str(response)
            # 若 prompt 是 OBL release date 且結果為空/null，log 警告
            if 'OBL release date' in prompt and (not result or result.strip() == '' or result.strip().lower() == 'null'):
                logging.warning(f"VLM API 補救 OBL release date 失敗: {image_path}")
            
            # 正確獲取 token 使用量
            tokens_used = 0
            try:
                if hasattr(response, 'usage_metadata'):
                    usage_metadata = response.usage_metadata
                    if hasattr(usage_metadata, 'total_token_count'):
                        tokens_used = usage_metadata.total_token_count
                    elif hasattr(usage_metadata, 'total_tokens'):
                        tokens_used = usage_metadata.total_tokens
            except Exception as e:
                logging.debug(f"無法獲取 token 使用量: {e}")
                tokens_used = 0
            return result, tokens_used
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            continue
    return '', 0

def analyze_with_gemini(content, prompt_template):
    """使用 Gemini 分析內容並返回結構化資料"""
    try:
        # 構建完整提示詞
        full_prompt = f"{prompt_template}\n\n文件內容：\n{content}"
        
        # 呼叫 API
        response_text, tokens_used = call_gemini_api(full_prompt)
        
        # 解析 JSON 回應
        from app import extract_json_from_response
        result = extract_json_from_response(response_text)
        
        if isinstance(result, dict) and 'error' in result:
            print(f"Gemini 回應解析錯誤: {result['error']}")
            return None
        
        # 確保回傳格式是列表
        if isinstance(result, dict):
            result = [result]
        elif not isinstance(result, list):
            print(f"Gemini 回應格式錯誤，期望列表或字典，實際: {type(result)}")
            return None
        
        return result
        
    except Exception as e:
        print(f"Gemini 分析錯誤: {str(e)}")
        return None 