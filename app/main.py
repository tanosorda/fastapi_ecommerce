from fastapi import FastAPI
from .database import engine, Base
from .routers import categories, cart, orders, support
import asyncio

app = FastAPI()

app.include_router(categories.router, prefix="/api")
app.include_router(cart.router, prefix="/api")
app.include_router(orders.router, prefix="/api")
app.include_router(support.router, prefix="/api")

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        # Для production используйте миграции вместо create_all!
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def read_root():
    return {"message": "Online Store API"}