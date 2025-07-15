import asyncio
import json
import os
import random
from fake_useragent import UserAgent
from playwright.async_api import async_playwright
from dotenv import load_dotenv

from google_table import upload_all_json_to_gsheet

#
load_dotenv()
ID_KRISHA = os.getenv('ID_KRISHA')
PASSWORD_KRISHA = os.getenv('PASSWORD_KRISHA')
SPREADSHEET_URL = os.getenv('SPREADSHEET_URL')
login_data = {
    'ID': ID_KRISHA,
    'password': PASSWORD_KRISHA
}


#Конфигурация

#Начальная и конечная страница
START_PAGE = 57
END_PAGE = 58
#Ссылка по которой парсим
BASE_URL = 'https://krisha.kz/prodazha/kvartiry/taldykorgan/?das[who]=1'
#Папка для сохранения JSON-файлов
JSON_DATA_PATH = 'data_kvartiri'
#Название листа в Google Таблице
WORKSHEET_TITLE = 'квартиры'



#Создаем папку для сохранения JSON-файлов
os.makedirs(JSON_DATA_PATH, exist_ok=True)



async def get_cookies():
    """Авторизация и сохранение cookies в файл (асинхронно)."""
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://id.kolesa.kz/login')

        await page.fill('input[name="login"]', login_data['ID'])
        await page.click('button[type="button"]')

        await page.fill('input[name="password"]', login_data['password'])
        await page.click('button[type="button"]')

        await page.wait_for_timeout(5000)
        await page.goto('https://krisha.kz/my')
        await page.wait_for_url('https://krisha.kz/my', timeout=100000)

        cookies = await page.context.cookies("https://krisha.kz")
        with open("cookies.json", "w") as f:
            json.dump(cookies, f)

        print("✅ Куки сохранены в cookies.json")
        await browser.close()


async def safe_get_text(page, selector, default="Не найдено"):
    try:
        el = await page.query_selector(selector)
        return await el.text_content() if el else default
    except Exception:
        return default


async def get_all_data_krisha():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        fake_useragent = UserAgent()
        context = await browser.new_context(
            
            user_agent=fake_useragent.firefox,
            locale="ru-RU",
            
        )

        # Загружаем куки
        try:
            print('KRISHA:Загружаем куки')
            with open("cookies.json") as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
        except FileNotFoundError:
            print("KRISHA:Файл cookies.json не найден, запускаем авторизацию")
            await get_cookies()
            await browser.close()
            return
        
        page = await context.new_page()
        await page.add_init_script("""Object.defineProperty(navigator, 'webdriver', {get: () => undefined})""")
        print('KRISHA:Загружаем страницу')
        try:
            await page.goto(BASE_URL, wait_until="networkidle")
        except:
            print('KRISHA:Ошибка при загрузке страницы')
            
        
        
        for _ in range(2):
            await page.mouse.wheel(0, 1000)
            await page.wait_for_timeout(1000)
        try:
            btn = page.get_by_role("button", name="")
            if btn:
                await btn.click()
        except:
            pass
        
        for i in range(START_PAGE, END_PAGE):
            # Навигация на страницу
            print(i)
            all_data = []
            
            

        # Проверяем наличие ссылки на личный кабинет (значит пользователь авторизован)
            login_link = await page.query_selector('li.cabinet-link-item > a.cabinet-link')
            if login_link:
                print("KRISHA:Не авторизован — пробуем получить куки заново")
                await browser.close()
                await get_cookies()  # Запускаем авторизацию и сохраняем куки
                return  # После авторизации перезапускай скрипт

            # Ждем появления карточек
            await page.goto(f'{BASE_URL}&page={i}')
            await page.wait_for_selector('div.a-card.a-storage-live.ddl_product', timeout=10000)

            
            
           
            await page.wait_for_selector("section.a-list")
            section = await page.query_selector("section.a-list")

            urls = await section.query_selector_all("div.a-card__header-left a")
            urls_list = []
            for url in urls:
                cur_url = await url.get_attribute("href")
                urls_list.append(cur_url)
            

            for url in urls_list:
                try:

                    await page.goto("https://krisha.kz" + url)
                    full_url = "https://krisha.kz" + url
                    await page.wait_for_timeout(random.randint(2000, 5000))
                except:
                    print('KRISHA:Ошибка при переходе на страницу')
                    continue




                print('KRISHA:Переходим на страницу')
                await page.wait_for_selector('div.offer__advert-title h1')
            
                # Основные поля
                title = (await safe_get_text(page, 'div.offer__advert-title h1')).strip()
                price = (await safe_get_text(page, 'div.offer__price')).replace(' ', '').replace('\n', '')
                description = (await safe_get_text(page, 'div.js-description.a-text.a-text-white-spaces')).strip().replace('\n',
                                                                                                                        '')

                # Парсинг заголовка
                try:
                    parts = [part.strip() for part in title.replace('\n', '·').split("·")]

                    rooms = parts[0]
                    floor, address = parts[2].split(",", 1)
                    floor, address = floor.strip(), address.strip()
                except:
                    rooms, floor, address = "Не найдено", "Не найдено", "Не найдено"

                # Телефон
                phone = "Не найдено"
                try:
                    btn = await page.query_selector('button.show-phones')
                    if btn:
                        await btn.click()
                        await page.wait_for_timeout(random.randint(2000, 5000))
                       
                      
                        
                        phones_el = await page.query_selector('div.offer__contacts-phones')
                        phones = (await phones_el.text_content()).strip().split('\n')
                        phone = ', '.join([p.strip() for p in phones if p.strip()])
                        
                except:
                    input('Пройдите капчу и нажмите Enter')
                    await page.reload()
                    btn = await page.query_selector('button.show-phones')
                    await page.evaluate("""element => {
        element.scrollIntoView({ behavior: "smooth", block: "center" });
    }""", btn)
                    await page.wait_for_timeout(1000)
                    if btn:
                        await btn.click()
                        await page.wait_for_timeout(random.randint(2000, 5000))
                        try:
                            phones_el = await page.query_selector('div.offer__contacts-phones')
                            phones = (await phones_el.text_content()).strip().split('\n')
                            
                            phone = ', '.join([p.strip() for p in phones if p.strip()])
                        except:
                            phone = "Не найдено"
                    else:
                        phone = "Не найдено"

                # Характеристики
                type_of_house = await safe_get_text(page,
                                                    'div.offer__info-item[data-name="flat.building"] div.offer__advert-short-info')
                renovation = await safe_get_text(page,
                                                'div.offer__info-item[data-name="flat.renovation"] div.offer__advert-short-info')
                house_year = await safe_get_text(page,
                                                'div.offer__info-item[data-name="house.year"] div.offer__advert-short-info')
                square = await safe_get_text(page, 'div.offer__info-item[data-name="live.square"] div.offer__advert-short-info')

                # Параметры
                params = {}
                try:
                    dl_elements = await page.query_selector_all('div.offer__parameters dl')
                    for dl in dl_elements:
                        dt = await dl.query_selector('dt')
                        dd = await dl.query_selector('dd')
                        if dt and dd:
                            dt_text = await dt.text_content()
                            dd_text = await dd.text_content()
                            params[dt_text.strip()] = dd_text.strip()
                except:
                    pass

                # Фото
                photos = []
                try:
                    
                    small_con = await page.query_selector_all('ul.gallery__small-list li')
                    for small in small_con:
                        small_src = await small.query_selector('div.gallery__small-item[data-photo-url]')
                        if small_src:
                            small_src = await small_src.get_attribute('data-photo-url')
                            photos.append(small_src)
                except:
                    pass
                data = {
                    'url': full_url,
                    'цена': price.replace('\xa0', ''),
                    'телефон': f'"{phone}"',
                    'комнаты': rooms,
                    'этаж': floor,
                    'адрес': address,
                    'тип дома': type_of_house,
                    'ремонт': renovation,
                    'год постройки': house_year,
                    'площадь': square,
                    'описание': description,
                    'доп. детали': [f'{k}: {v}' for k, v in params.items()],
                    'фото': ', '.join(photos),
                }


                print(data)
                all_data.append(data)
                await page.wait_for_timeout(random.randint(2000, 5000))
            with open(f'{JSON_DATA_PATH}/data_{i}.json', 'w', encoding='utf-8') as f:
                json.dump(all_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    asyncio.run(get_all_data_krisha())
    upload_all_json_to_gsheet(SPREADSHEET_URL, WORKSHEET_TITLE)
    