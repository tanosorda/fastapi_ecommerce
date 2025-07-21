import os
import logging
from dotenv import load_dotenv
from fastapi import FastAPI, Depends

load_dotenv()

from app.api import categories, cart, orders, support
from app.db.database import get_db, create_schema_and_data, ensure_database_exists
from app.db.initial_data import create_initial_data  # импорт здесь, в основном модуле

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Ozzo.lv")

app.include_router(categories.router, prefix="/api/categories", tags=["Categories"], dependencies=[Depends(get_db)])
app.include_router(cart.router, prefix="/api/cart", tags=["Cart"], dependencies=[Depends(get_db)])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"], dependencies=[Depends(get_db)])
app.include_router(support.router, prefix="/api/support", tags=["Support"], dependencies=[Depends(get_db)])

@app.on_event("startup")
async def on_startup():
    await ensure_database_exists()

    create_test = os.getenv("CREATE_TEST_DATA", "false").lower() == "true"
    logger.info("Initializing database schema (test data = %s)", create_test)

    await create_schema_and_data(create_test_data=create_test)

    if create_test:
        logger.info("Inserting initial test data...")
        await create_initial_data()


    logger.info("Database ready.")
