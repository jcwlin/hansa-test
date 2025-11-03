from typing import Any, Tuple, Optional
from analyzers.services.base_service import analyze_text_with_prompt_with_gemini as _analyze


def analyze_calendar(text: str, lang: str, custom_prompt: Optional[str] = None) -> Tuple[Any, int]:
    return _analyze(text, 'Calendar', lang, custom_prompt)
