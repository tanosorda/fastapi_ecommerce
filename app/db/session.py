import os
import re
import asyncpg
import asyncio
from logging import getLogger

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text  # <-- Добавлено для обертывания SQL-строк

from app.models.base import Base
from app.config import Config

logger = getLogger(__name__)

# Парсим переменные окружения
POSTGRES_URL = "postgresql+asyncpg://postgres:qwerty123@localhost:5432/cbdShop"

# Целевая БД
TARGET_DB_NAME = POSTGRES_URL.rsplit('/', 1)[-1]
ADMIN_DB_URL = re.sub(r"/[^/]+$", "/postgres", POSTGRES_URL.replace("postgresql+asyncpg", "postgresql"))

# Async SQLAlchemy engine
ASYNC_DB_URL = POSTGRES_URL
SYNC_DB_URL = POSTGRES_URL.replace("postgresql+asyncpg", "postgresql")  # для alembic

async def create_database():
    """Создает БД, если она не существует"""
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            logger.info(f"Connecting to admin DB: {ADMIN_DB_URL}")
            conn = await asyncpg.connect(ADMIN_DB_URL)

            exists = await conn.fetchval(
                "SELECT 1 FROM pg_database WHERE datname = $1",
                TARGET_DB_NAME
            )

            if not exists:
                await conn.execute(f'CREATE DATABASE "{TARGET_DB_NAME}"')
                logger.info(f"Database {TARGET_DB_NAME} created")

            await conn.close()
            return
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                logger.error("Failed to create database after retries")
                raise
            await asyncio.sleep(retry_delay)

async def init_db():
    """Инициализация БД и создание таблиц"""
    global engine, AsyncSessionLocal

    try:
        await create_database()

        engine = create_async_engine(
            ASYNC_DB_URL,
            echo=True,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30
        )

        # Проверка подключения
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))  # <-- Исправлено здесь

        # Создание таблиц
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Session factory
        AsyncSessionLocal = sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=AsyncSession,
            autoflush=False
        )

        return engine

    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

async def shutdown_db():
    """Корректное завершение соединений"""
    try:
        if 'AsyncSessionLocal' in globals() and AsyncSessionLocal:
            await AsyncSessionLocal().close_all()
        if 'engine' in globals() and engine:
            await engine.dispose()
    except Exception as e:
        logger.error(f"Error during shutdown: {e}")

# Глобальные переменные
AsyncSessionLocal = None
engine = None
