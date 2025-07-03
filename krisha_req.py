import asyncio
import json
import os
from playwright.async_api import async_playwright
from dotenv import load_dotenv
from database.orm import update_site_krisha

load_dotenv()
ID_KRISHA = os.getenv('ID_KRISHA')
PASSWORD_KRISHA = os.getenv('PASSWORD_KRISHA')

login_data = {
    'ID': ID_KRISHA,
    'password': PASSWORD_KRISHA
}

async def get_cookies():
    """Авторизация и сохранение cookies в файл (асинхронно)."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://id.kolesa.kz/login')

        await page.fill('input[name="login"]', login_data['ID'])
        await page.click('button[type="button"]')

        await page.fill('input[name="password"]', login_data['password'])
        await page.click('button[type="button"]')

        await page.wait_for_timeout(5000)
        await page.goto('https://krisha.kz/my')
        await page.wait_for_url('https://krisha.kz/my', timeout=15000)

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


async def get_data_krisha():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ))

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
        print('KRISHA:Загружаем страницу')

        # Навигация на страницу
        await page.goto('https://krisha.kz/prodazha/kvartiry/taldykorgan/?das[who]=1')

        # Проверяем наличие ссылки на личный кабинет (значит пользователь авторизован)
        login_link = await page.query_selector('li.cabinet-link-item > a.cabinet-link')
        if login_link:
            print("KRISHA:Не найден личный кабинет — пробуем получить куки заново")
            await browser.close()
            await get_cookies()  # Запускаем авторизацию и сохраняем куки
            return # После авторизации перезапускай скрипт

        # Ждем появления карточек
        await page.wait_for_selector('div.a-card.a-storage-live.ddl_product', timeout=10000)


        # Получаем карточку и проверяем "хозяин"
        card = await page.query_selector('div.a-card.a-storage-live.ddl_product')
        owner = await card.query_selector('div.label.label--yellow.label-user-owner')
        card_id = await page.query_selector('div.a-card')
        card_id = await card_id.get_attribute('data-id')
        
        if not owner:
            print('KRISHA:Не от хозяина')
            await browser.close()
            return


        href = await card.query_selector('a.a-card__image')
        url = f"https://krisha.kz{await href.get_attribute('href')}"
        new_url = await update_site_krisha(card_id)
        if not new_url:
            await browser.close()
            return

        await page.goto(url)
        print('KRISHA:Переходим на страницу')
        await page.wait_for_selector('div.offer__advert-title h1')
        await page.wait_for_timeout(5000)

        # Имитация действий
        for x, y in [(100, 100), (300, 150), (500, 300)]:
            await page.mouse.move(x, y)
            await page.wait_for_timeout(500)
        await page.mouse.wheel(0, 200)
        await page.wait_for_timeout(500)
        await page.mouse.wheel(0, -200)
        await page.wait_for_timeout(500)

        # Основные поля
        title = (await safe_get_text(page, 'div.offer__advert-title h1')).strip()
        price = (await safe_get_text(page, 'div.offer__price')).replace(' ', '').replace('\n', '')
        description = (await safe_get_text(page, 'div.js-description.a-text.a-text-white-spaces')).strip().replace('\n', '')

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
                await page.wait_for_timeout(1000)
                phones_el = await page.query_selector('div.offer__contacts-phones')
                phones = (await phones_el.text_content()).strip().split('\n')
                phone = ', '.join([p.strip() for p in phones if p.strip()])
        except:
            pass

        # Характеристики
        type_of_house = await safe_get_text(page, 'div.offer__info-item[data-name="flat.building"] div.offer__advert-short-info')
        renovation = await safe_get_text(page, 'div.offer__info-item[data-name="flat.renovation"] div.offer__advert-short-info')
        house_year = await safe_get_text(page, 'div.offer__info-item[data-name="house.year"] div.offer__advert-short-info')
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
            sources = await page.query_selector_all('div.gallery__main source[type="image/jpeg"]')
            for src in sources:
                srcset = await src.get_attribute('srcset')
                if srcset:
                    photos.append(srcset.split()[0])
        except:
            pass
        data = {
            'url': url,
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
        

        await browser.close()
        return data


