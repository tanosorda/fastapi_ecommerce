import logging
import os
import httpx
from fastapi import FastAPI
from alembic.config import Config as AlembicConfig
from alembic import command

from app.config import Config
from app.db.session import init_db, shutdown_db, AsyncSessionLocal
from app.models.category import Category
from app.models.product import Product
from app.services.catalog_service import CatalogService
from app.utils.ngrok import start_ngrok

app = FastAPI()
logger = logging.getLogger(__name__)

async def seed_database():
    """Заполнение БД тестовыми данными"""
    try:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                service = CatalogService(session)
                if not await service.get_categories():
                    cat = Category(name='Default')
                    session.add(cat)
                    await session.flush()
                    session.add_all([
                        Product(name='Товар 1', description='Описание', price=10.0, image_url='...', category_id=cat.id),
                        Product(name='Товар 2', description='Описание 2', price=20.0, image_url='...', category_id=cat.id),
                    ])
                    logger.info("Database seeded successfully")
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")
        raise

def run_alembic_revision():
    alembic_cfg = AlembicConfig("alembic.ini")
    command.revision(alembic_cfg, message="Auto-generated migration", autogenerate=True)

def run_alembic_upgrade():
    alembic_cfg = AlembicConfig("alembic.ini")
    command.upgrade(alembic_cfg, "head")

@app.on_event("startup")
async def startup_event():
    """Запуск приложения"""
    try:
        # 1. Инициализация БД
        await init_db()

        # 2. Применение миграций
        if os.environ.get("ENV") == "dev":
            run_alembic_revision()
        run_alembic_upgrade()

        # 3. Запуск ngrok
        public_url = start_ngrok()
        logger.info(f"Ngrok started at: {public_url}")

        # 4. Установка webhook
        async with httpx.AsyncClient() as client:
            webhook_url = f"{public_url}/webhook/{Config.get_bot_token()}"
            response = await client.post(
                f"https://api.telegram.org/bot{Config.get_bot_token()}/setWebhook",
                json={"url": webhook_url}
            )
            response.raise_for_status()
            logger.info(f"Webhook set to: {webhook_url}")

        # 5. Заполнение БД тестовыми данными
        await seed_database()

        logger.info("Application startup completed")
    except Exception as e:
        logger.critical(f"Application startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Завершение работы приложения"""
    try:
        await shutdown_db()
        from pyngrok import ngrok
        ngrok.kill()
        logger.info("Application shutdown completed")
    except Exception as e:
        logger.error(f"Shutdown error: {e}")

@app.get("/")
async def root():
    return {"message": "Hello World"}