import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

DB_URL = os.getenv("POSTGRES_URL", "postgresql+asyncpg://tanosorda:qwerty123@localhost/CBD_shop")

# Для Alembic нужно создать синхронный движок
SYNC_DB_URL = DB_URL.replace("postgresql+asyncpg://", "postgresql://")

engine = create_async_engine(DB_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)