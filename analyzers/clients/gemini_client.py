import threading
import logging
import os
from typing import Tuple, Optional
import google.generativeai as genai
from PIL import Image
from pdf2image import convert_from_path

# -------------------------------------------------------------------
# Gemini Configuration
# -------------------------------------------------------------------
GEMINI_CONFIG = {
    "api_key": os.getenv("GEMINI_API_KEY", "AIzaSyDnqwyH_n_anNMTQQRwHxFWMvdt1wJRC28"),
    "project_id": "hansa-tanker",
    "model": "gemini-2.5-pro",
    "location": "us-central1",
}

# -------------------------------------------------------------------
# Initialize Gemini
# -------------------------------------------------------------------
genai.configure(api_key=GEMINI_CONFIG["api_key"])

_model_instance = None
_lock = threading.Lock()

# Default retry + generation config
MAX_RETRIES = 3
GENERATION_CONFIG = {
    "temperature": 0.6,
    "top_p": 0.9,
    "top_k": 40,
}


# -------------------------------------------------------------------
# Model Loader
# -------------------------------------------------------------------
def get_model():
    """Singleton pattern to avoid reloading model multiple times."""
    global _model_instance
    if _model_instance is None:
        with _lock:
            if _model_instance is None:
                try:
                    logging.info("✅ Configured Gemini with provided API key")
                    _model_instance = genai.GenerativeModel(GEMINI_CONFIG["model"])
                except Exception as e:
                    logging.error(f"❌ Failed to configure Gemini: {e}")
                    raise
    return _model_instance


# -------------------------------------------------------------------
# Core Gemini Call
# -------------------------------------------------------------------
def call_gemini(prompt: str, image_path: Optional[str] = None) -> Tuple[str, int]:
    """
    Call Gemini model with text prompt and optional image/PDF.
    Returns (result_text, tokens_used).
    """
    model = get_model()

    for attempt in range(MAX_RETRIES):
        try:
            # -------------------------
            # Handle image or PDF input
            # -------------------------
            if image_path:
                ext = os.path.splitext(image_path)[1].lower()
                if ext == ".pdf":
                    # Convert first page of PDF to image
                    images = convert_from_path(image_path, first_page=1, last_page=1)
                    img = images[0]
                else:
                    img = Image.open(image_path)

                response = model.generate_content(
                    [prompt, img],
                    generation_config=GENERATION_CONFIG
                )
            else:
                response = model.generate_content(
                    prompt,
                    generation_config=GENERATION_CONFIG
                )

            # -------------------------
            # Validate and parse response
            # -------------------------
            if not response or not hasattr(response, "candidates") or not response.candidates:
                logging.warning("⚠️ Gemini returned an empty or invalid response object.")
                return "NO_RESPONSE", 0

            candidate = response.candidates[0]
            finish_reason = getattr(candidate, "finish_reason", None)

            if finish_reason == 2:
                logging.warning("⚠️ Gemini response blocked by safety filters (finish_reason=2).")
                return "SAFETY_BLOCKED", 0

            # Extract text safely
            result = getattr(response, "text", None)
            if not result:
                try:
                    if candidate.content.parts:
                        result = "".join(
                            part.text for part in candidate.content.parts if hasattr(part, "text")
                        )
                    else:
                        result = ""
                except Exception as e:
                    logging.error(f"Error extracting text from response: {e}")
                    result = ""

            result = result.strip()

            # Estimate token usage
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
            logging.error(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if attempt == MAX_RETRIES - 1:
                return f"Error after {MAX_RETRIES} attempts: {e}", 0
            continue

    return "", 0
