from sqlalchemy import BigInteger, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

URL = "postgresql+asyncpg://user:9900@localhost:5432/db_name"
engine = create_async_engine(url=URL, echo=True)
BASE = declarative_base()
class User(BASE):
    __tablename__ = "USER"

    id = Column(Integer,primary_key=True)
    tg_id = Column(BigInteger)

class Category(BASE):
    __tablename__ = "Category"

    id = Column(Integer,primary_key=True)
    name = Column(String(100))

    products= relationship('Products', back_populates='category')


class Products(BASE):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(String(100))
    price = Column(Integer())
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', back_populates='products')



# Создает таблицы и определят
async def run_main():
    async with engine.begin() as conn:
        await conn.run_sync(BASE.metadata.create_all)


# Вносит данные в эти таблицы которые были определены ранее
    async with AsyncSession(engine) as session:
        usertg = User(tg_id=123567894)
        session.add(usertg)

        category_add = Category(name="Technic")
        session.add(category_add)

        product_add = Products(
            name='Iphone 13 pro',
            description='Состояние Идеал',
            price=1000,
            image='/home/erko/Desktop/telegram_bot/images/Iphone15.jpg',
            category=category_add
        )
        session.add(product_add)

        # Завершает сессию
        await session.commit()

import asyncio
# Запускает асинхронный код выше через asyncio
asyncio.run(run_main())