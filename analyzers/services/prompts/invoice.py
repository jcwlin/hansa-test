PROMPTS = {
    'en': """You are a professional invoice data analyst. Your task is to accurately extract structured information from the provided invoice text.
Please extract the following fields:
- invoice_id (Invoice Number)
- issue_date (Issue Date, format: YYYY-MM-DD)
- customer_name (Customer Name)
- total_amount (Total Amount, numbers only)
Strictly return the result in the following JSON format. If a field cannot be found, please fill in null.
Return only JSON, no extra explanation or text.
{text}
""",
    'zh': """你是一位專業的發票資料分析師，請從下方發票文字中精確萃取結構化資訊。
請擷取以下欄位：
- invoice_id（發票號碼）
- issue_date（開立日期，格式：YYYY-MM-DD）
- customer_name（客戶名稱）
- total_amount（總金額，僅數字）
嚴格以下方 JSON 格式回傳，若無法取得請填 null。
僅回傳 JSON，不要有多餘說明或文字。
{text}
""",
    'nor': """Du er en profesjonell fakturaanalytiker. Din oppgave er å nøyaktig trekke ut strukturert informasjon fra den oppgitte fakturateksten.
Vennligst trekk ut følgende felt:
- invoice_id (Fakturanummer)
- issue_date (Utstedelsesdato, format: ÅÅÅÅ-MM-DD)
- customer_name (Kundenavn)
- total_amount (Totalt beløp, kun tall)
Returner strengt resultatet i følgende JSON-format. Hvis et felt ikke finnes, vennligst fyll inn null.
Returner kun JSON, ingen ekstra forklaring eller tekst.
{text}
""",
}