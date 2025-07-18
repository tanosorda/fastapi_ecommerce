from sqlalchemy import select
from app.db.session import async_session
from app.models.product import Product

class ProductRepository:
    @staticmethod
    async def create(product_data: dict):
        async with async_session() as session:
            product = Product(**product_data)
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product

    @staticmethod
    async def get_all():
        async with async_session() as session:
            result = await session.execute(select(Product))
            return result.scalars().all()

    @staticmethod
    async def get_by_id(product_id: int):
        async with async_session() as session:
            result = await session.execute(
                select(Product).where(Product.id == product_id)
            return result.scalar_one_or_none()

    @staticmethod
    async def update(product_id: int, product_data: dict):
        async with async_session() as session:
            product = await session.get(Product, product_id)
            if product:
                for key, value in product_data.items():
                    setattr(product, key, value)
                await session.commit()
                return product
            return None

    @staticmethod
    async def delete(product_id: int):
        async with async_session() as session:
            product = await session.get(Product, product_id)
            if product:
                await session.delete(product)
                await session.commit()
                return True
            return False