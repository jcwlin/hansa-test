PROMPTS = {
    'en': """You are a professional table data analyst. Your task is to extract all rows and columns as structured data from the provided table text.
Return the result as a JSON array of objects, each object representing a row.
{text}
""",
    'zh': """你是一位專業的表格資料分析師，請從下方表格文字中萃取所有列與欄，並以結構化資料回傳。
結果請以 JSON 陣列回傳，每個物件代表一列。
{text}
""",
    'nor': """Du er en profesjonell tabellanalytiker. Din oppgave er å trekke ut alle rader og kolonner som strukturert data fra den oppgitte tabellteksten.
Returner resultatet som et JSON-array av objekter, hvert objekt representerer en rad.
{text}
""",
}