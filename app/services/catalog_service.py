from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product_repo import ProductRepo

class CatalogService:
    def __init__(self, session: AsyncSession):
        self.repo = ProductRepo(session)

    async def get_categories(self):
        return await self.repo.list_categories()

    async def get_products(self, category_id: int):
        return await self.repo.list_products_by_category(category_id)