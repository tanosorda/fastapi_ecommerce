import os
import sys
import asyncio
from logging.config import fileConfig
from alembic import context
from dotenv import load_dotenv

# 🔁 Сначала грузим переменные окружения и sys.path
load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ⬇️ Только теперь можно импортировать своё приложение
from app.db.database import Base, engine
from app.models import models  # Убедись, что здесь есть твои SQLAlchemy-модели

# Alembic config
config = context.config
fileConfig(config.config_file_name)

# Преобразуем asyncpg URI в sync
raw = os.getenv("POSTGRES_URL")
if not raw:
    raise RuntimeError("POSTGRES_URL is not set in .env")
sync_url = raw.replace("+asyncpg", "")
config.set_main_option("sqlalchemy.url", sync_url)

# Мета-информация для Alembic
target_metadata = Base.metadata

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations)

def run_migrations_online():
    asyncio.run(run_async_migrations())

# 🚀 Запуск миграции
run_migrations_online()
