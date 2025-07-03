# Парсер недвижимости

Автоматизированный парсер для сбора данных о недвижимости с сайтов Krisha.kz и OLX.kz с автоматической загрузкой в Google Sheets.

## Возможности

- Парсинг данных о недвижимости с Krisha.kz
- Парсинг данных о недвижимости с OLX.kz
- Автоматическая загрузка данных в Google Sheets
- Планировщик задач для автоматической очистки базы данных
- Обработка ошибок с автоматическим перезапуском

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/pars-master.git
cd pars-master
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

4. Настройте переменные окружения в файле `.env`

5. Добавьте файл `creds.json` с учетными данными Google Service Account

6. Добавьте файл `cookies.txt` с cookies для авторизации на сайтах

## Настройка

### Google Sheets API

1. Создайте проект в Google Cloud Console
2. Включите Google Sheets API
3. Создайте Service Account и скачайте JSON файл
4. Переименуйте файл в `creds.json` и поместите в корневую папку проекта

### Переменные окружения

Создайте файл `.env` со следующими переменными:

```
SPREADSHEET_URL=https://docs.google.com/spreadsheets/d/your-spreadsheet-id
```

## Использование

Запустите основной скрипт:

```bash
python main.py
```

Программа будет:
- Инициализировать базу данных
- Запускать планировщик задач
- Периодически парсить данные с Krisha.kz и OLX.kz
- Загружать данные в Google Sheets
- Автоматически очищать базу данных каждые 2 недели

## Структура проекта

```
pars-master/
├── main.py              # Основной файл приложения
├── database/            # Модули для работы с базой данных
├── krisha_req.py       # Парсер Krisha.kz
├── olx_req.py          # Парсер OLX.kz
├── google_table.py     # Модуль для работы с Google Sheets
├── requirements.txt    # Зависимости проекта
├── .env.example        # Пример файла с переменными окружения
├── .gitignore          # Исключения для Git
└── README.md           # Документация
```

## Требования

- Python 3.8+
- Google Sheets API
- Доступ к интернету

## Лицензия

MIT License

## Поддержка

При возникновении проблем создайте Issue в репозитории. 