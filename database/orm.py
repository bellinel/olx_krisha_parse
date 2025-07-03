


from sqlalchemy import select, delete
from database.engine import Database, OlxId, KrishaId




async def update_site_olx(title: str):
    db = Database()

    async with db.session_factory() as session:
        # Проверяем, существует ли уже такой card_id
        query = select(OlxId).where(OlxId.title == title)
        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            print("OLX:Такое объявление уже существует")
            return None
        else:
            # Добавляем новую запись
            session.add(OlxId(title=title))
            await session.commit()
            print("OLX: Новое объявление добавлено.")
            return True


async def update_site_krisha(card_id: str):
    db = Database()

    async with db.session_factory() as session:
        # Получаем первую (или любую) запись
        query = select(KrishaId).order_by(KrishaId.id.asc()).limit(1)
        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            # Обновляем site_url
            if existing.card_id == card_id:
                print("KRISHA:ID совпадает — новая квартира не найдена")
                return None
            else:
                existing.card_id = card_id
                await session.commit()
                print("KRISHA:Найдена новая квартира")
                return True
        else:
            # Если записей ещё нет — создаём новую
            session.add(KrishaId(card_id=card_id))
            await session.commit()
            print("KRISHA:Найдена новая квартира")
            return True
            

           

async def clear_olx_table():
    db = Database()
    async with db.session_factory() as session:
        await session.execute(delete(OlxId))
        await session.commit()
        print("🧹 Таблица OlxId очищена.")
        