import asyncio
from alembic.config import Config
from alembic import command
from sqlalchemy import text
from app.db.database import engine, Base, AsyncSessionLocal
import logging

logger = logging.getLogger(__name__)

async def ensure_database():
    """Проверяет существование БД и базовых таблиц"""
    try:
        async with engine.connect() as conn:
            # Проверяем существование нужной таблицы
            await conn.execute(text("SELECT 1 FROM alembic_version LIMIT 1"))
            logger.info("Database and alembic_version table exist")
    except Exception as e:
        logger.info("Database or tables don't exist, creating...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tables created")

async def run_migrations():
    """Асинхронно применяет миграции Alembic"""
    try:
        # Создаем синхронный engine для Alembic
        from sqlalchemy import create_engine
        sync_engine = create_engine(Config.get_main_option("sqlalchemy.url"))
        
        with sync_engine.connect() as connection:
            alembic_cfg = Config("alembic.ini")
            alembic_cfg.attributes['connection'] = connection
            command.upgrade(alembic_cfg, "head")
            logger.info("Migrations applied successfully")
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise