import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def run_async_migrations():
    # Получаем URL из конфига и заменяем на asyncpg
    url = config.get_main_option("sqlalchemy.url")
    async_url = url.replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(async_url)
    
    async with engine.connect() as connection:
        await connection.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata
            )
        )
        
        async with engine.begin() as connection:
            await connection.run_sync(context.run_migrations)

if not context.is_offline_mode():
    asyncio.run(run_async_migrations())
else:
    run_migrations_offline()