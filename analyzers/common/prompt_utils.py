import yaml
from functools import lru_cache
from analyzers.services.prompts import SERVICE_PROMPTS

CONFIG_PATH = 'config.yaml'

@lru_cache(maxsize=1)
def load_config():
    import yaml
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


from typing import Optional

def select_prompt(analysis_type: str, lang: str, custom_prompt: Optional[str] = None) -> str:
    if custom_prompt and custom_prompt.strip():
        print(f"🧠 custom_prompt (first 8 words) in prompt_utils: {' '.join(custom_prompt.split()[:8])}")
        return custom_prompt

    svc_prompts_code = SERVICE_PROMPTS.get(analysis_type, {})
    print("analysis_type:", analysis_type)
    print("lang:", lang)
    print("svc_prompts_code:", svc_prompts_code)  # shows the dict or empty {}

    if lang in svc_prompts_code and svc_prompts_code[lang]:
        print(f"svc_prompts_code[{lang}]:", svc_prompts_code[lang])
        return svc_prompts_code[lang]

    if custom_prompt and custom_prompt.strip():
        print("custom_prompt (second check):", repr(custom_prompt))
        return custom_prompt

    config = load_config()
    print("DEBUG → config keys:", config.keys())

    # 1) 優先讀 analyzers 專屬 prompts（檔案可覆蓋內建）
    analyzers = config.get('analyzers', {})
    print("DEBUG → analyzers keys:", analyzers.keys())

    svc = analyzers.get(analysis_type, {})
    print("DEBUG → analysis_type:", analysis_type)
    print("DEBUG → svc:", svc)

    svc_prompts = svc.get('prompts') or {}
    print("DEBUG → svc_prompts:", svc_prompts)

    if isinstance(svc_prompts, dict) and lang in svc_prompts and svc_prompts[lang]:
        print(f"DEBUG → svc_prompts[{lang}]:", svc_prompts[lang])
        return svc_prompts[lang]

    # 2) 退回全域 prompts
    prompts = config.get('prompts', {})
    print("DEBUG → prompts keys:", prompts.keys())

    if analysis_type in prompts and isinstance(prompts[analysis_type], dict):
        prompt_by_lang = prompts[analysis_type]
        print("DEBUG → prompt_by_lang:", prompt_by_lang)

        if lang in prompt_by_lang and prompt_by_lang[lang]:
            print(f"DEBUG → prompt_by_lang[{lang}]:", prompt_by_lang[lang])
            return prompt_by_lang[lang]

    # 3) 最後選任一類型中符合語言的模板
    for prompt_type_name, prompt_type in prompts.items():
        print(f"DEBUG → Checking prompt_type '{prompt_type_name}':", prompt_type)
        if isinstance(prompt_type, dict) and lang in prompt_type and prompt_type[lang]:
            print(f"DEBUG → Found fallback prompt for '{prompt_type_name}' [{lang}]:", prompt_type[lang])
            return prompt_type[lang]

    print("⚠️ DEBUG → No suitable prompt found. Returning empty string.")
    return ''
