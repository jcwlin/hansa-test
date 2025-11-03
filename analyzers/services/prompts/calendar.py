PROMPTS = {
    'en': """You are a professional calendar event extractor. Your task is to extract all events from the provided text, including date, time, event name, and location if available.
Return the result as a JSON array of objects.
{text}
""",
    'zh': """你是一位專業的行事曆事件擷取專家，請從下方文字中擷取所有事件，包括日期、時間、事件名稱與地點（如有）。
結果請以 JSON 陣列回傳。
{text}
""",
    'nor': """Du er en profesjonell kalenderhendelsesuttrekker. Din oppgave er å trekke ut alle hendelser fra teksten, inkludert dato, tid, hendelsesnavn og sted hvis tilgjengelig.
Returner resultatet som et JSON-array av objekter.
{text}
""",
}