import asyncio
from playwright.async_api import async_playwright

from database.orm import update_site_olx
from krisha_req import safe_get_text


async def olx_get_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        print('OLX:Загружаем браузер')
        page = await context.new_page()

        await page.goto(
            'https://www.olx.kz/nedvizhimost/prodazha-kvartiry/taldykorgan/?search%5Bfilter_enum_tipsobstvennosti%5D%5B0%5D=ot_hozyaina&search%5Bfilter_enum_tip_zhilya%5D%5B0%5D=vtorichnyy_rynok'
        )
        await page.wait_for_selector('div[data-cy="l-card"]')
        await page.wait_for_timeout(2000)

        card = await page.query_selector('div[data-cy="l-card"]')
        url_el = await card.query_selector('div.css-1apmciz div[data-cy="ad-card-title"] a')
        title = await url_el.query_selector('h4')
        title = await title.text_content()
        
        url = await url_el.get_attribute('href')
        
        full_url = f"https://www.olx.kz{url}"   

        new_url = await update_site_olx(title)  # Убедись, что эта функция async
        if not new_url:
            return
        print('OLX:Переходим на страницу')
        await page.goto(full_url)
        await page.wait_for_timeout(2000)

        data = {}
        
        # Параметры
        param_container = await page.query_selector('div[data-testid="ad-parameters-container"]')
        if param_container:
            params = await param_container.query_selector_all('p')
            for param in params:
                span = await param.query_selector('span')
                if span:
                    continue
                text = await param.text_content()
                if ':' in text:
                    k, v = [s.strip() for s in text.split(':', 1)]
                    data[k] = v
        
        # Описание
        description = await safe_get_text(page, 'div[data-cy="ad_description"] div.css-19duwlz')
        

        # Телефон
        try:
            phone_button = await page.query_selector('button[data-testid="show-phone"]')
            if phone_button:
                await phone_button.click()
                await page.wait_for_timeout(3000)
                phone_el = await page.query_selector('div.css-1478ixo a[class="css-oexhm1"]')
                
                phone = await phone_el.text_content() if phone_el else 'Не найдено'
        except:
            phone = 'Не найдено'
        data['url'] = full_url
        data['телефон'] = phone
        data['описание'] = description

        

        await browser.close()
        return data

# Запуск    