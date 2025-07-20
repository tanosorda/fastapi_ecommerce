from app.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Основная зависимость для получения сессии БД
async def get_db_session() -> AsyncSession:
    async with get_db() as session:
        yield session

