from fastapi import FastAPI
from .database import engine, Base, check_db_exists, create_database
from .initial_data import create_initial_data
from .routers import categories, cart, orders, support
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(categories.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(support.router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    # Проверяем существует ли БД
    if not await check_db_exists():
        logger.info("Database does not exist, creating...")
        try:
            # Создаем структуру БД
            await create_database()
            logger.info("Database created successfully")
            
            # Заполняем тестовыми данными
            await create_initial_data()
            logger.info("Test data generated successfully")
        except Exception as e:
            logger.error(f"Error during database initialization: {e}")
            raise
    else:
        logger.info("Database already exists, skipping initialization")

@app.get("/")
async def read_root():
    return {"message": "Online Store API"}