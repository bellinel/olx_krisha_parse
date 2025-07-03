import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def append_data_to_gsheet_by_url(flat_data: dict, site: str, spreadsheet_url: str, worksheet_index: int = 0, json_keyfile: str = 'creds.json'):


    match = re.search(r'/d/([a-zA-Z0-9-_]+)', spreadsheet_url)
    if not match:
        raise ValueError("❌ Неверная ссылка на таблицу.")
    spreadsheet_id = match.group(1)

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(spreadsheet_id)
    sheet = spreadsheet.get_worksheet(worksheet_index)

    headers = sheet.row_values(1)
    if not headers:
        headers = list(flat_data.keys())
        sheet.append_row(headers)

    # Приводим всё к строкам
    row = [', '.join(v) if isinstance(v, list) else str(v) for v in [flat_data.get(col, '') for col in headers]]
    sheet.append_row(row)

    print(f"{site}✅ Объявление добавлено в таблицу.")
