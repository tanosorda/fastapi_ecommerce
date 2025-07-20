import os
import sys
from logging.config import fileConfig
from alembic import context

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import Base
from app.models.models import *  # Импорт всех моделей

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    from app.db.database import engine
    connectable = engine

    if connectable.is_async:
        from sqlalchemy.ext.asyncio import async_engine_from_config
        connectable = async_engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
        )

    if connectable.is_async:
        async def run_async_migrations():
            async with connectable.connect() as connection:
                await connection.run_sync(do_run_migrations)
        import asyncio
        asyncio.run(run_async_migrations())
    else:
        with connectable.connect() as connection:
            do_run_migrations(connection)

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()