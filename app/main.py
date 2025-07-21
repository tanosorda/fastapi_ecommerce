import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI

from app.db.database import check_db_exists, create_database
from app.db.initial_data import create_initial_data
from app.api import categories, cart, orders, support

# Загружаем .env
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Online Store API")

# Каждый модуль с собственным префиксом
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(cart.router,       prefix="/api/cart",       tags=["Cart"])
app.include_router(orders.router,     prefix="/api/orders",     tags=["Orders"])
app.include_router(support.router,    prefix="/api/support",    tags=["Support"])

@app.on_event("startup")
async def startup_event():
    # Проверяем, есть ли БД и таблицы
    exists = await check_db_exists()
    if not exists:
        logger.info("Database does not exist, creating schema...")
        await create_database()
        logger.info("Schema created successfully")
        if os.getenv("CREATE_TEST_DATA", "false").lower() == "true":
            await create_initial_data()
            logger.info("Test data generated successfully")
    else:
        logger.info("Database already exists, skipping initialization")

@app.get("/", tags=["Health"])
async def read_root():
    return {"message": "Online Store API is running."}
