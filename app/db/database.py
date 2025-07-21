import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

# Берём асинхронный URL из .env
DATABASE_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/dbname"
)

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def check_db_exists() -> bool:
    """
    Пробуем выполнить простую выборку,
    чтобы понять, подключена ли БД и есть ли хотя бы одна таблица.
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False

async def create_database():
    """
    Создаёт все таблицы по metadata моделей.
    """
    from app.models.models import Base as ModelsBase
    async with engine.begin() as conn:
        await conn.run_sync(ModelsBase.metadata.create_all)
