from typing import Tuple, Any, Optional
from analyzers.clients.gemini_client import call_gemini
from analyzers.common.json_utils import extract_json_from_response_text
from analyzers.common.prompt_utils import select_prompt

from typing import Any, Optional, Tuple
import logging


def analyze_text_with_prompt_with_gemini(
        text: str,
        analysis_type: str,
        lang: str,
        custom_prompt: Optional[str] = None
) -> Tuple[Any, int]:
    """
    Analyze text using Gemini LLM with a specific prompt.

    Returns:
        Tuple[result, tokens_used]
        - result: parsed JSON if valid, otherwise a dict with error info
        - tokens_used: token count for this call
    """
    try:
        # Select the appropriate prompt
        prompt_template = select_prompt(analysis_type, lang, custom_prompt)
        print("=== ARJ in analyze_text_with_prompt_with_gemini===")

        # Fill in {text} placeholder if needed
        if '{text}' not in prompt_template:
            prompt_str = f"{prompt_template}\n\n檔案內容：\n{text}"
           # print("==ARJ in IF  prompt_template===", prompt_template)
            print("=== ARJ in analyze_text_with_prompt_with_gemini===")
        else:
            prompt_str = prompt_template.replace('{text}', text)
            #print("=== ARJ in ELSE prompt_str===", prompt_str)

        # Call Gemini
        response_text, tokens_used = call_gemini(prompt_str)

        #print(f"DEBUG → Tokens used: {tokens_used}")
        #print("DEBUG → Raw response_text:", repr(response_text))

        # Handle safety block or empty response
        if response_text in ["SAFETY_BLOCKED", "NO_RESPONSE", None, ""]:
            logging.warning("⚠️ Gemini response blocked or empty.")
            result = {
                "error": "LLM response blocked or empty",
                "response": response_text
            }
            return result, tokens_used

        # Try to parse JSON
        try:
            result = extract_json_from_response_text(response_text)
            print("DEBUG → Raw result type:", type(result))
            print("DEBUG → Raw result value:", repr(result))
            if isinstance(result, dict):
                print("DEBUG → Result keys:", list(result.keys()))
        except Exception as e:
            logging.warning(f"⚠️ Failed to parse JSON: {e}")
            result = {
                "error": "LLM 回應不是有效 JSON",
                "response": response_text
            }

        return result, tokens_used

    except Exception as e:
        logging.error(f"⚠️ ERROR in analyze_text_with_prompt_with_gemini: {e}")
        return {
            "error": "Exception during analysis",
            "exception": str(e)
        }, 0