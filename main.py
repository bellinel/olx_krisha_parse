import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import asyncio
from dotenv import load_dotenv

load_dotenv()

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from database.engine import Database
from database.orm import clear_olx_table
from google_table import  append_data_to_gsheet_by_url
from krisha_req import get_data_krisha
from olx_req import olx_get_data

db = Database()
#

SERVICE_ACCOUNT_FILE = 'creds.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_URL = os.getenv('SPREADSHEET_URL')

creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()





async def upload_to_sheets_krisha():
    try:
        data = await get_data_krisha()
        if data:
            print("KRISHA:Добавляем в таблицу")
            append_data_to_gsheet_by_url(data, "KRISHA", SPREADSHEET_URL, 0)
            
    except Exception as e:
        print("Ошибка в krisha:", e)


async def upload_to_sheets_olx():
    try:
        data = await olx_get_data()
        if data:
            print("OLX:Добавляем в таблицу")
            append_data_to_gsheet_by_url(data, "OLX", SPREADSHEET_URL, 1)
            
    except Exception as e:
        print("Ошибка в olx:", e)



async def main():
    await db.init()
    schedule_jobs()
    while True:
        await upload_to_sheets_krisha()
        await upload_to_sheets_olx()
        await asyncio.sleep(5)


def schedule_jobs():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(clear_olx_table, IntervalTrigger(weeks=2))
    print("Планировщик запущен очистка OLX будет происходить каждые 2 недели")
    scheduler.start()

if __name__ == "__main__":
    asyncio.run(main())