from models import User, Category, Product, async_session

from sqlalchemy import select


async def get_categories():
    async with async_session() as session:
        result = await session.scalars(select(Category))
        print(result)


async def get_products(category_id):
    async with async_session() as session:
        result = await session.scalars(select(Product).where(
            Product.category_id == category_id))
        print(result)


async def get_product(product_id):
    async with async_session() as session:
        result = await session.scalar(select(Product).where(
            Product.id == product_id))
        print(result)