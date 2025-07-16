import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
#
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

def upload_all_json_to_gsheet(data_dir : str, spreadsheet_url: str, worksheet_title: str, json_keyfile: str = 'creds.json'):
    """
    Загружает все квартиры из всех JSON-файлов в папке data_kvartiri в Google Таблицу на лист с названием 'квартиры'.
    Использует массовую запись для обхода лимитов Google API.
    Порядок столбцов соответствует порядку ключей первого объекта из JSON.
    """
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import os
    import json

    # Получаем ID таблицы
    match = re.search(r'/d/([a-zA-Z0-9-_]+)', spreadsheet_url)
    if not match:
        raise ValueError("❌ Неверная ссылка на таблицу.")
    spreadsheet_id = match.group(1)

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)

    spreadsheet = client.open_by_key(spreadsheet_id)

    # Проверяем, есть ли лист с нужным названием
    try:
        sheet = spreadsheet.worksheet(worksheet_title)
    except gspread.exceptions.WorksheetNotFound:
        sheet = spreadsheet.add_worksheet(title=worksheet_title, rows="1000", cols="30")

    # Собираем все данные
    all_data = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            with open(os.path.join(data_dir, filename), encoding='utf-8') as f:
                try:
                    items = json.load(f)
                    if isinstance(items, list):
                        all_data.extend(items)
                except Exception as e:
                    print(f"Ошибка чтения {filename}: {e}")

    if not all_data:
        print("Нет данных для загрузки.")
        return

    # Определяем порядок ключей по первому объекту
    first_keys = list(all_data[0].keys())
    # Собираем все возможные ключи
    all_keys = set(first_keys)
    for item in all_data:
        all_keys.update(item.keys())
    # Сохраняем порядок: сначала как в первом объекте, потом остальные
    headers = first_keys + [k for k in all_keys if k not in first_keys]

    # Очищаем лист и записываем заголовки одной операцией
    sheet.clear()
    sheet.append_row(headers)

    # Формируем все строки для массовой записи
    rows = []
    for item in all_data:
        row = [', '.join(v) if isinstance(v, list) else str(v) for v in [item.get(col, '') for col in headers]]
        rows.append(row)

    # Массовая запись
    if rows:
        sheet.append_rows(rows)
    print(f"✅ Загружено {len(all_data)} квартир в лист '{worksheet_title}'")