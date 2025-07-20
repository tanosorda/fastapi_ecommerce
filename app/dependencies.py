from app.db.database import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Основная зависимость для получения сессии БД
async def get_db_session() -> AsyncSession:
    async with get_db() as session:
        yield session

# Пример дополнительной зависимости для аутентификации (заглушка)
async def get_current_user_id() -> int:
    # В реальном приложении здесь будет логика получения ID пользователя из JWT
    return 1  # Заглушка для примера