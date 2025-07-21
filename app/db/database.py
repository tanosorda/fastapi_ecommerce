import os
import re
import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from app.db.initial_data import create_initial_data

from app.db.base import Base  # Импортируем общий Base, не создаём заново!

# Загружаем переменные окружения
load_dotenv()

# Получаем строку подключения из .env
DATABASE_URL = os.getenv("POSTGRES_URL")
if not DATABASE_URL:
    raise ValueError("❌ Переменная POSTGRES_URL не найдена в .env")

# Создаём async engine и сессию
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Асинхронный контекстный менеджер для получения сессии
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


# ---------------------------------------
# Поддержка автоматического создания БД
# ---------------------------------------

# Парсим DATABASE_URL для подключения к системной БД (postgres)
def parse_postgres_url(database_url: str):
    match = re.match(r"postgresql\+asyncpg://(.*?):(.*?)@(.*?):(\d+)/(.*)", database_url)
    if not match:
        raise ValueError("❌ Невалидный формат POSTGRES_URL")

    user, password, host, port, dbname = match.groups()
    return {
        "user": user,
        "password": password,
        "host": host,
        "port": int(port),
        "dbname": dbname
    }

# Создание базы данных, если она отсутствует
async def ensure_database_exists():
    config = parse_postgres_url(DATABASE_URL)
    target_db = config.pop("dbname")  # Имя создаваемой БД

    # Подключаемся к системной БД postgres
    conn = await asyncpg.connect(**config, database="postgres")

    db_exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", target_db)

    if not db_exists:
        await conn.execute(f'CREATE DATABASE "{target_db}"')
        print(f"✅ База данных '{target_db}' успешно создана.")
    else:
        print(f"✅ База данных '{target_db}' уже существует.")
    
    await conn.close()


# ---------------------------------------
# Создание таблиц и тестовых данных
# ---------------------------------------

async def create_schema_and_data(create_test_data: bool = False):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


