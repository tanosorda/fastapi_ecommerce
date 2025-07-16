from fastapi import FastAPI
from db.session import init_db
from api.products import router as products_router

app = FastAPI()
app.include_router(products_router)

@app.on_event("startup")
async def startup():
    await init_db()