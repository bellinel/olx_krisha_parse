# 🏠 Парсер недвижимости

Автоматизированный парсер для сбора данных о недвижимости с сайтов **Krisha.kz** и **OLX.kz** с автоматической загрузкой в **Google Sheets**.

## ✨ Возможности

- 🔍 **Парсинг данных** с Krisha.kz и OLX.kz
- 📊 **Автоматическая загрузка** в Google Sheets
- ⏰ **Планировщик задач** для автоматической очистки базы данных
- 🔄 **Обработка ошибок** с автоматическим перезапуском
- 📝 **Логирование** всех операций
- 🎯 **Фильтрация** по заданным параметрам

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/pars-master.git
cd pars-master
```

### 2. Установка Python зависимостей

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
```

### 3. Установка Playwright

```bash
# Установка браузеров для Playwright
playwright install

# Или установка конкретных браузеров
playwright install chromium
playwright install firefox
playwright install webkit
```

### 4. Настройка конфигурации

```bash
# Копирование файла с переменными окружения
cp env.example .env

# Редактирование файла .env
notepad .env  # Windows
# или
nano .env     # Linux/Mac
```

### 5. Настройка Google Sheets API

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

### 6. Настройка Google Sheets

1. **Создайте Google таблицу**
2. **Поделитесь таблицей** с email из Service Account
3. **Скопируйте URL** таблицы в файл `.env`

### 7. Настройка cookies (опционально)

```bash
# Создайте файл cookies.json или cookies.txt с cookies для авторизации на сайтах
# Формат cookies.txt: domain.com	TRUE	/	FALSE	1735689600	cookie_name	cookie_value
# Формат cookies.json: {"domain": "example.com", "name": "cookie_name", "value": "cookie_value"}
touch cookies.json
# или
touch cookies.txt
```

**Примечание:** Файлы cookies содержат конфиденциальные данные и не загружаются в репозиторий. Создайте их локально после клонирования проекта.

### 8. Проверка безопасности

Убедитесь, что конфиденциальные файлы не отслеживаются Git:

```bash
# Проверка статуса файлов
git status

# Должны быть в списке "Untracked files":
# - creds.json
# - cookies.json
# - cookies.txt
# - .env
```

## ⚙️ Конфигурация

### Файл .env

Скопируйте `env.example` в `.env` и настройте переменные:

```env
# URL вашей Google таблицы
SPREADSHEET_URL=https://docs.google.com/spreadsheets/d/your-spreadsheet-id/edit

# Настройки парсинга
PARSING_INTERVAL=300  # 5 минут между запусками
HEADLESS=true         # Запуск браузера в фоне
BROWSER_TIMEOUT=30    # Таймаут загрузки страницы
```

### Структура Google Sheets

Создайте в таблице два листа:
- **KRISHA** - для данных с Krisha.kz
- **OLX** - для данных с OLX.kz

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
5. 📝 Логирование всех операций

### Логи

```bash
# Просмотр логов в реальном времени
tail -f parser.log

# Просмотр последних 100 строк
tail -n 100 parser.log
```

## 📁 Структура проекта

```
pars-master/
├── main.py              # 🚀 Основной файл приложения
├── database/            # 🗄️ Модули для работы с БД
│   ├── engine.py        # Настройка подключения к БД
│   └── orm.py           # Модели данных
├── krisha_req.py        # 🔍 Парсер Krisha.kz
├── olx_req.py           # 🔍 Парсер OLX.kz
├── google_table.py      # 📊 Модуль для Google Sheets
├── requirements.txt     # 📦 Зависимости проекта
├── env.example          # 📝 Пример конфигурации
├── .gitignore           # 🚫 Исключения для Git
├── README.md            # 📖 Документация
├── creds.json           # 🔑 Google API ключи (не в Git)
├── cookies.json         # 🍪 Cookies для авторизации (не в Git)
├── cookies.txt          # 🍪 Cookies для авторизации (не в Git)
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

### Медленная работа

1. Увеличьте `BROWSER_TIMEOUT` в `.env`
2. Установите `HEADLESS=true`
3. Используйте прокси (настройте в `.env`)

## 📊 Мониторинг

### Проверка работы

```bash
# Проверка логов
grep "KRISHA" parser.log
grep "OLX" parser.log

# Проверка ошибок
grep "ERROR" parser.log
```

### Статистика

- 📈 Данные сохраняются в Google Sheets
- 📊 База данных очищается каждые 2 недели
- 🔄 Парсинг происходит каждые 5 минут

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