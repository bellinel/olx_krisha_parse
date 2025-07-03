# 🏠 Парсер недвижимости

Автоматизированный парсер для сбора данных о недвижимости с сайтов **Krisha.kz** и **OLX.kz** с автоматической загрузкой в **Google Sheets**.

## ✨ Возможности

- 🔍 **Парсинг данных** с Krisha.kz и OLX.kz
- 📊 **Автоматическая загрузка** в Google Sheets
- ⏰ **Планировщик задач** для автоматической очистки базы данных
- 🔄 **Обработка ошибок** с автоматическим перезапуском
- 📝 **Логирование** всех операций

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/bellinel/olx_krisha_parse.git
cd olx_krisha_parse
```

### 2. Установка зависимостей

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Установка браузеров для Playwright
playwright install
```

### 3. Настройка конфигурации

```bash
# Копирование файла с переменными окружения
cp .env.example .env

# Редактирование файла .env
notepad .env  # Windows
# или
nano .env     # Linux/Mac
```

### 4. Настройка Google Sheets API

1. **Создайте проект в Google Cloud Console:**
   - Перейдите на [Google Cloud Console](https://console.cloud.google.com/)
   - Создайте новый проект или выберите существующий

2. **Включите Google Sheets API:**
   - В меню слева выберите "APIs & Services" → "Library"
   - Найдите "Google Sheets API" и включите его

3. **Создайте Service Account:**
   - Перейдите в "APIs & Services" → "Credentials"
   - Нажмите "Create Credentials" → "Service Account"
   - Заполните форму и создайте аккаунт

4. **Скачайте ключ:**
   - Нажмите на созданный Service Account
   - Перейдите на вкладку "Keys"
   - Нажмите "Add Key" → "Create new key" → "JSON"
   - Скачайте файл и переименуйте в `creds.json`

5. **Разместите файл:**
   ```bash
   # Поместите creds.json в корневую папку проекта
   mv ~/Downloads/your-project-credentials.json creds.json
   ```

### 5. Настройка Google Sheets

1. **Создайте Google таблицу**
2. **Поделитесь таблицей** с email из Service Account
3. **Скопируйте URL** таблицы в файл `.env`
4. **Обязательно создайте в таблице два листа:**
   - `KRISHA` — для данных с Krisha.kz
   - `OLX` — для данных с OLX.kz

## ⚙️ Конфигурация

### Файл .env

Скопируйте `.env.example` в `.env` и заполните переменные:

```env
# Данные для входа на Krisha.kz
ID_KRISHA=your_krisha_login
PASSWORD_KRISHA=your_krisha_password

# URL вашей Google таблицы
SPREADSHEET_URL=https://docs.google.com/spreadsheets/d/your-spreadsheet-id/edit
```

### Структура Google Sheets

В вашей Google-таблице обязательно должны быть два листа:
- **KRISHA** — для данных с Krisha.kz
- **OLX** — для данных с OLX.kz

## 🎯 Использование

### Запуск парсера

```bash
python main.py
```

### Что происходит при запуске:

1. ✅ Инициализация базы данных
2. ✅ Запуск планировщика задач
3. 🔄 Периодический парсинг данных:
   - Krisha.kz → Google Sheets (лист "KRISHA")
   - OLX.kz → Google Sheets (лист "OLX")
4. 🧹 Автоматическая очистка базы каждые 2 недели

## 📁 Структура проекта

```
olx_krisha_parse/
├── main.py              # 🚀 Основной файл приложения
├── database/            # 🗄️ Модули для работы с БД
│   ├── engine.py        # Настройка подключения к БД
│   └── orm.py           # Модели данных
├── krisha_req.py        # 🔍 Парсер Krisha.kz
├── olx_req.py           # 🔍 Парсер OLX.kz
├── google_table.py      # 📊 Модуль для Google Sheets
├── requirements.txt     # 📦 Зависимости проекта
├── .env.example         # 📝 Пример конфигурации
├── .gitignore           # 🚫 Исключения для Git
├── README.md            # 📖 Документация
├── creds.json           # 🔑 Google API ключи (не в Git)
└── .env                 # ⚙️ Конфигурация (не в Git)
```

## 🛠️ Требования

- **Python** 3.8+
- **Google Sheets API** (бесплатно)
- **Интернет соединение**
- **Playwright** (устанавливается автоматически)

## 🔧 Устранение неполадок

### Ошибка "Playwright browsers not found"

```bash
# Переустановка браузеров
playwright install --force
```

### Ошибка "Google Sheets API"

1. Проверьте, что `creds.json` находится в корневой папке
2. Убедитесь, что Google Sheets API включен
3. Проверьте права доступа к таблице

### Ошибка "Database connection"

```bash
# Удалите старую базу данных
rm real_estate.db
# Перезапустите приложение
python main.py
```

### Ошибка авторизации на Krisha.kz

1. Проверьте правильность логина и пароля в `.env`
2. Убедитесь, что аккаунт не заблокирован
3. Попробуйте войти вручную на сайте

## 📊 Мониторинг

### Проверка работы

```bash
# Проверка логов
grep "KRISHA" parser.log
grep "OLX" parser.log

# Проверка ошибок
grep "ERROR" parser.log
```

## 🤝 Поддержка

- 📧 **Issues:** Создайте Issue в репозитории
- 📖 **Документация:** Читайте комментарии в коде
- 🔧 **Настройка:** Проверьте файл `.env`

## 📄 Лицензия

MIT License - используйте свободно!

## 🔄 Обновления

```bash
# Обновление кода
git pull origin main

# Обновление зависимостей
pip install -r requirements.txt --upgrade

# Обновление браузеров
playwright install --force
```

---

⭐ **Если проект полезен, поставьте звезду на GitHub!** 