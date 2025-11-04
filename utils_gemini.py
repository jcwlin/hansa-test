import os
import json
import time
import threading
import google.generativeai as genai
from PIL import Image
from pdf2image import convert_from_path
import logging

MODEL = "gemini-2.5-pro"

# Global model instance to avoid repeated initialization
_model_instance = None
_lock = threading.Lock()


def get_model():
    """
    Get singleton model instance, avoiding repeated initialization
    Uses API key authentication (simpler than OAuth)
    """
    global _model_instance

    if _model_instance is None:
        with _lock:
            if _model_instance is None:
                try:
                    # Configure with API key (can be overridden by GEMINI_API_KEY env var)
                    api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDnqwyH_n_anNMTQQRwHxFWMvdt1wJRC28')
                    genai.configure(api_key=api_key)
                    logging.info("✅ Configured Gemini with API key")
                    _model_instance = genai.GenerativeModel(MODEL)
                except Exception as e:
                    logging.error(f"❌ Failed to configure Gemini: {e}")
                    raise

    return _model_instance


def call_gemini_api(prompt: str, image_path: str = None, max_retries: int = 3) -> tuple:
    """Call Gemini API, supports Vision LLM image processing, PDFs auto-convert to first page image"""
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

            # Log warning if OBL release date extraction fails
            if 'OBL release date' in prompt and (
                    not result or result.strip() == '' or result.strip().lower() == 'null'):
                logging.warning(f"VLM API failed to extract OBL release date: {image_path}")

            # Get token usage correctly
            tokens_used = 0
            try:
                if hasattr(response, 'usage_metadata'):
                    usage_metadata = response.usage_metadata
                    if hasattr(usage_metadata, 'total_token_count'):
                        tokens_used = usage_metadata.total_token_count
                    elif hasattr(usage_metadata, 'total_tokens'):
                        tokens_used = usage_metadata.total_tokens
            except Exception as e:
                logging.debug(f"Unable to get token usage: {e}")
                tokens_used = 0
            return result, tokens_used
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            continue
    return '', 0


def analyze_with_gemini(content, prompt_template):
    """Analyze content with Gemini and return structured data"""
    try:
        # Build complete prompt
        full_prompt = f"{prompt_template}\n\n文件內容：\n{content}"

        # Call API
        response_text, tokens_used = call_gemini_api(full_prompt)

        # Parse JSON response
        from app import extract_json_from_response
        result = extract_json_from_response(response_text)

        if isinstance(result, dict) and 'error' in result:
            print(f"Gemini response parsing error: {result['error']}")
            return None

        # Ensure return format is a list
        if isinstance(result, dict):
            result = [result]
        elif not isinstance(result, list):
            print(f"Gemini response format error, expected list or dict, got: {type(result)}")
            return None

        return result

    except Exception as e:
        print(f"Gemini analysis error: {str(e)}")
        return None