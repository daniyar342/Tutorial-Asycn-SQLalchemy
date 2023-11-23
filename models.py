
from sqlalchemy import Column, BigInteger, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

POSTGRES_URL = 'postgresql+asyncpg://_user:9900@localhost:5432/_db'
engine = create_async_engine(POSTGRES_URL, echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    products = relationship('Product', back_populates='category')

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(100))
    price = Column(Integer())
    image = Column(String(100))
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship('Category', back_populates='products')

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Insert a user
        user = User(tg_id=123456749)  # Replace with an actual Telegram ID
        session.add(user)

        # Insert a category
        category = Category(name='Electronics')
        session.add(category)

        # Insert a product
        product = Product(name='Iphone 13 pro',
                          description='Состояние Идеал',
                          price=1000,
                          image='/home/erko/Desktop/telegram_bot/images/Iphone15.jpg',
                          category=category)
        session.add(product)

        # Commit the changes
        await session.commit()

# Run the async_main function
import asyncio
asyncio.run(async_main())
