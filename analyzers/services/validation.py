def validate_cargo_bl_data(data):
    """Validate and correct common OCR/AI interpretation errors"""

    # Rule 1: If B/L split quantity >= B/L quantity, it's wrong
    if data.get('B/L split quantity (MT)') and data.get('B/L quantity (MT)'):
        try:
            split = float(str(data['B/L split quantity (MT)']).replace(',', ''))
            full = float(str(data['B/L quantity (MT)']).replace(',', ''))

            if split >= full:
                data['B/L split quantity (MT)'] = None
        except:
            pass

    # Rule 2: Clean numeric fields
    numeric_fields = ['B/L quantity (MT)', 'B/L split quantity (MT)']
    for field in numeric_fields:
        if field in data:
            value = str(data[field]).replace(',', '').strip()
            if value.lower() in ['null', 'n/a', 'none', '']:
                data[field] = None

    return data