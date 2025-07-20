from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product import Product
from app.models.category import Category

class ProductRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_categories(self) -> list[Category]:
        result = await self.session.execute(select(Category))
        return result.scalars().all()

    async def list_products_by_category(self, category_id: int) -> list[Product]:
        result = await self.session.execute(select(Product).where(Product.category_id == category_id))
        return result.scalars().all()