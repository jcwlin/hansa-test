from typing import Any, Tuple, Optional
from analyzers.services.base_service import analyze_text_with_prompt_with_gemini


def analyze_table(text: str, lang: str, custom_prompt: Optional[str] = None) -> Tuple[Any, int]:
    return analyze_text_with_prompt_with_gemini(text, 'Table Analysis', lang, custom_prompt)
