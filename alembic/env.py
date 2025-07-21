import os
import sys
from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine

# Позволяет импортировать ваши модели
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.db.database import Base
from app.models.models import *  # noqa

config = context.config
fileConfig(config.config_file_name)

# Можно переопределять URL из переменной, если нужно:
env_url = os.getenv("POSTGRES_URL_SYNC")
if env_url:
    config.set_main_option("sqlalchemy.url", env_url)

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
    sync_url = config.get_main_option("sqlalchemy.url")
    sync_engine = create_engine(sync_url)
    with sync_engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
