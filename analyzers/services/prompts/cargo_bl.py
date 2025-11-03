PROMPTS = {
    'en': """You are a professional maritime logistics data analyst. Your task is to carefully analyze the Bill of Lading (B/L) PDF document I provide and extract key information according to the following rules.

**SCENARIO DETECTION:**
First, determine which scenario applies to this document:

**SCENARIO 1: Single BL with Multiple Copies**
- The SAME B/L number appears multiple times
- Each instance has a copy type label (FIRST ORIGINAL, SECOND ORIGINAL, THIRD ORIGINAL, COPY NOT NEGOTIABLE, etc.)
- Action: Create ONLY ONE record - prioritize extracting the FIRST ORIGINAL copy. If FIRST ORIGINAL is not available, use SECOND ORIGINAL, then THIRD ORIGINAL, then any other copy type.

**SCENARIO 2: Multiple Different BLs**
- DIFFERENT B/L numbers throughout the document
- May or may not have copy type labels
- Action: Create ONE record per unique B/L number

**How to Identify Separate Bills of Lading:**
1. Look for distinct "B/L NO." fields with DIFFERENT numbers
2. Check for repeated header sections (new Shipper, Consignee, Notify fields)
3. Look for "Bill of Lading" title appearing multiple times
4. Check for page breaks with new BL information
5. Each distinct B/L number = one separate BL document

**Task:**
Extract information for the following fields from ALL Bills of Lading in the document.

**Required fields for each BL:**
1. Cargo #
2. BL number
3. B/L quantity (MT)
4. B/L split quantity (MT)
5. Cargo name
6. Charterer
7. Consignee, order to
8. Notify
9. Stow
10. LoadPort
11. Disch. Port
12. OBL release date
13. Release cargo against
14. VESSEL
15. VOY.NO.

**Field Extraction Rules:**

1. **Cargo # (Cargo Number):**
   - The Cargo # should be automatically derived from the **B/L number**.
   - The **B/L number** may appear in any of the following formats:
     - `XXX YYYY ZZZZ`
     - `XXX YYYY ZZZZZ`
     - `XXXX YYYY ZZZZZZ`
   - The prefix can vary (e.g., `FLOY`, `FLO`, `EMA`, etc.), and the final segment may contain digits and an optional trailing letter (e.g., `0114A` or `011`).
   - Extract the **leading digits** from the final segment (`ZZZZ`) as the **Cargo #**.
   - Ignore any trailing alphabetic suffix (e.g., `A`).
   - Examples:
     - `EMA 2406 0802` → Cargo # = `8`
     - `EMA 2406 1001` → Cargo # = `10`
     - `FLOY 2505 0114A` → Cargo # = `11`
     - `FLO 2505 0119` → Cargo # = `11`

2. **BL number (Bill of Lading Number):** 
   - Look for the number next to labels like "B/L NO." or "Bill of Lading No."
   - This uniquely identifies each BL
   - In both scenarios: Extract the B/L number for each unique BL

3. **Copy Priority (For Scenario 1 ONLY - Internal Use):**
   - When the same BL number appears multiple times with different copy types:
     * FIRST priority: "FIRST ORIGINAL"
     * SECOND priority: "SECOND ORIGINAL"
     * THIRD priority: "THIRD ORIGINAL"
     * FOURTH priority: "COPY NOT NEGOTIABLE" or "NON-NEGOTIABLE COPY"
   - Extract data from the highest priority copy available
   - **DO NOT include copy_type field in the output**

4. **B/L quantity (MT) (Bill of Lading Quantity):** 
   - **PRIMARY SEARCH PATTERN:**
     Look for: "part of one original lot of [NUMBER] metric tons"
     The [NUMBER] is the B/L quantity (total original lot)
   
   - **SECONDARY LOCATIONS:**
     * "Bill of Lading Figure [Mts]" - use this if the above pattern is not found
     * Text describing total cargo quantity
   
   - **IMPORTANT:** 
     * This is the TOTAL original lot size
     * May be larger than the split quantity for this specific BL
     * If document says "part of one original lot of X metric tons" → X is the B/L quantity

5. **B/L split quantity (MT) (Bill of Lading Split Quantity):** 
   - **CRITICAL: This field identifies when cargo is split across multiple BLs**
   
   - **PRIMARY SEARCH PATTERN:**
     Look for this EXACT phrase pattern:
     "This shipment said to be [NUMBER] metric tons was loaded on board the vessel as part of one original lot of [BIGGER_NUMBER] metric tons"
     
     If you find this pattern:
     - The FIRST number ([NUMBER]) = B/L split quantity ✅
     - The SECOND number ([BIGGER_NUMBER]) = B/L quantity (total lot)
   
   - **EXAMPLE from document:**
     "This shipment said to be 3,999.974 metric tons was loaded on board the vessel as part of one original lot of 4,999.974 metric tons"
     → B/L split quantity = 3,999.974
     → B/L quantity = 4,999.974
   
   - **VALIDATION RULES:**
     * Split quantity MUST be less than B/L quantity
     * If split quantity == B/L quantity → set to null (no actual split)
     * If you cannot find the pattern above → set to null
   
   - **DO NOT:**
     * Use "Bill of Lading Figure" as split quantity
     * Use random numbers from the document
     * Guess or make assumptions

6. **Cargo name (Cargo Name):** 
   - Look for cargo description under "COMMODITY" or "Name of product"
   - Extract the product name (e.g., "RBD PALM OIL", "CRUDE OIL", etc.)

7. **Charterer (Charterer):** 
   - Look for the keyword "as Charterer"
   - if charterer is not found then write "Not Available"
   - The company name before it is the charterer
   - Extract only the company name

8. **Consignee, order to (Consignee):** 
   - Look for information next to "Consignee/Order of" or "Consignee" field
   - **EXTRACTION RULES:**
     * If content is just "TO ORDER" with no additional text → use "TO ORDER"
     * If content is "To the order of [Company Name]..." → extract ONLY the company name
     * Remove ALL address information (street, city, country, postal codes)
     * Remove any "Branch" information
     * Extract only the main company/organization name

9. **Notify (Notify Party):** 
   - Look for company names under the "Notify" or "Notify Party" field
   - **EXTRACTION RULES:**
     * Extract ONLY company/organization names
     * Remove ALL address information (streets, cities, countries, postal codes, phone, email)
     * If multiple notify parties exist, separate with semicolons
     * Focus on main business entity names only

10. **Stow (Stowage):** 
    - Look for codes next to "OCEAN CARRIAGE STOWAGE" or similar labels
    - **CRITICAL FORMAT RULES:**
      * Each stow code follows pattern: **NUMBER + LETTER** (e.g., 4P, 2S, 3C)
      * If multiple codes, they may be separated by commas
      * **NEVER confuse letter "S" with number "8"** - always interpret as letter S
      * **NEVER confuse letter "O" with number "0"** - always interpret as letter O
      * Patterns like "48", "28", "38" are likely "4S", "2S", "3S"
      * When in doubt for second position, ALWAYS choose the letter
    - Examples: "4P, 2S, 7P, 7S" or "3C, 5B"
      *If stow information is not available, record as: "Not Available"

11. **LoadPort (Loading Port):** 
    - Look for keyword "at the port of" or "Port of Loading"
    - The location after it is the loading port
    - **EXTRACTION RULES:**
      * Extract ONLY the port/city name
      * Remove country names (e.g., "TAIWAN", "INDIA", "CHINA")
      * Example: "TAICHUNG, TAIWAN" → extract as "TAICHUNG"

12. **Disch. Port (Discharge Port):** 
    - Look for keyword "to be delivered to the port of" or "Port of Discharge"
    - The location after it is the discharge port
    - **EXTRACTION RULES:**
      * Extract ONLY the port/city name
      * Remove country names
      * Remove the word "PORT" from the result
      * Example: "KANDLA PORT, INDIA" → extract as "KANDLA"

13. **OBL release date (Bill of Lading Issue Date):**
    - **PRIMARY GOAL:** Extract the date when this Bill of Lading was signed and issued
    - **REASONING PROCESS (Follow exactly):**

      **Step 1: Locate the Authority**
      - Find the text block beginning with "Dated at"
      - This is ALWAYS at the bottom of the document, near signature and company stamp

      **Step 2: Critical Completeness Check**
      - Verify if a complete date is present (day, month, AND year)
      - **CRUCIAL RULE:** Check the space between "this" and "Day of"
      - There MUST be a number (e.g., "28TH", "08TH")
      - **If this number is missing, blank, or unreadable → return null**
      - Do not guess the day or use dates from elsewhere

      **Step 3: Final Verification & Extraction**
      - If date in "Dated at" section is complete, extract it
      - **DO NOT use:**
        * Charter Party date (e.g., "JUN 21 2024")
        * "ON BOARD DATE"
        * "LC DATE"
        * Any other date on the document

      **Step 4: Formatting**
      - Convert to YYYY-MM-DD format
      - If returned null in Step 2, keep as null

    - **FINAL FORMAT:** YYYY-MM-DD or null

14. **Release cargo against (Cargo Release Condition):** 
    - Look for explicit cargo release conditions in the document
    - If no clear cargo release conditions are found, use "LOI"
    - Default value: "LOI"

15. **VESSEL:** 
    - Look for vessel name information
    - Usually found in phrases like "on board the tanker [VESSEL NAME]" or "M/V [NAME]"
    - Extract the vessel name (e.g., "EVA PEARL", "EVA MANILA")

16. **VOY.NO. (Voyage Number):**
    - **PRIMARY LOCATION:** Look for voyage number after the vessel name
      * Format: "M.T. [VESSEL NAME] V.XXXX" or "M/V [NAME] V.XXXX"
      * The "V.XXXX" is the voyage number
      * Example: "M.T. FLOYEN V.2505" → extract "2505"
    
    - **SECONDARY LOCATION:** Look for labels like "VOY NO:", "VOYAGE:", "V/Y:"
    
    - **FALLBACK:** Extract from BL number middle part (YYMM format)
      * BL format: "FLO 2505 0101" → voyage = "2505"
    
    - **VALIDATION:** Must be exactly 4 digits in YYMM format
    - If not found or invalid → return "Not Available"


**Output Format:**
Return all extracted information as a JSON array, where each element represents ONE unique B/L number (regardless of how many copies exist in the document).

**JSON Format Examples:**

**Example 1 - Scenario 1 (Same BL, Multiple Copies):**

Input: 4 copies of the same BL number (FIRST ORIGINAL, SECOND ORIGINAL, THIRD ORIGINAL, COPY NOT NEGOTIABLE)
Output: ONLY 1 record (using data from FIRST ORIGINAL), NO copy_type field

[
  {
    "Cargo #": "1",
    "BL number": "DUM/PAR-01",
    "B/L quantity (MT)": "2,150.250",
    "B/L split quantity (MT)": "1000.000",
    "Cargo name": "RBD PALM OIL",
    "Charterer": "ICOF SHIP CHARTERING PTE LTD",
    "Consignee, order to": "BRF S.A.",
    "Notify": "BRF S.A.",
    "Stow": "2P, 2S, 7P, 7S",
    "LoadPort": "DUMAI",
    "Disch. Port": "PARANAGUA",
    "OBL release date": "2025-07-21",
    "Release cargo against": "LOI",
    "VESSEL": "EVA PEARL",
    "VOY.NO.": "2506"
  }
]

**Example 2 - Scenario 2 (Multiple Different BLs):**

Input: Multiple different BL numbers across multiple PDF pages (each page = one BL)
Output: One record per unique BL number

[
  {
    "Cargo #": "2",
    "BL number": "DUM/PAR-02",
    "B/L quantity (MT)": "4,349.878",
    "B/L split quantity (MT)": null,
    "Cargo name": "CRUDE PALM OIL",
    "Charterer": "GLOBAL TRADERS LTD",
    "Consignee, order to": "TO ORDER",
    "Notify": "IMPORT COMPANY INC.",
    "Stow": "3P, 4S",
    "LoadPort": "BELAWAN",
    "Disch. Port": "MUMBAI",
    "OBL release date": "2025-07-22",
    "Release cargo against": "LOI",
    "VESSEL": "EVA MANILA",
    "VOY.NO.": "2507"
  },
  {
    "Cargo #": "1",
    "BL number": "FLO 2505 0101",
    "B/L quantity (MT)": "3,200.500",
    "B/L split quantity (MT)": null,
    "Cargo name": "SOYBEAN OIL",
    "Charterer": "GLOBAL TRADERS LTD",
    "Consignee, order to": "TO ORDER",
    "Notify": "IMPORT COMPANY INC.",
    "Stow": "3P, 4S",
    "LoadPort": "BELAWAN",
    "Disch. Port": "MUMBAI",
    "OBL release date": "2025-07-22",
    "Release cargo against": "LOI",
    "VESSEL": "EVA MANILA",
    "VOY.NO.": "2507"
  },
  {
    "Cargo #": "1A",
    "BL number": "FLO 2505 0101A",
    "B/L quantity (MT)": "2,150.250",
    "B/L split quantity (MT)": null,
    "Cargo name": "SUNFLOWER OIL",
    "Charterer": "GLOBAL TRADERS LTD",
    "Consignee, order to": "TO ORDER",
    "Notify": "IMPORT COMPANY INC.",
    "Stow": "3P, 4S",
    "LoadPort": "BELAWAN",
    "Disch. Port": "MUMBAI",
    "OBL release date": "2025-07-22",
    "Release cargo against": "LOI",
    "VESSEL": "EVA MANILA",
    "VOY.NO.": "2507"
  }
]

**CRITICAL REQUIREMENTS:**
1. Return ONLY valid JSON array - no extra text or explanations
2. Detect the scenario correctly:
   - Same BL multiple times = Extract ONE record only (prioritize FIRST ORIGINAL copy)
   - Different BL numbers = One record per unique BL number
3. **DO NOT include copy_type field in any output**
4. Each element must contain exactly 15 fields
5. Ensure all field names match exactly as shown
6. Use null for missing values, not empty strings
7. Maintain data consistency within each BL record
8. For Scenario 1: If multiple copies exist, use data from the highest priority copy (FIRST ORIGINAL > SECOND ORIGINAL > THIRD ORIGINAL > other copies)

{text}
""",
}