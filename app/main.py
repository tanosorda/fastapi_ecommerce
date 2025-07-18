from fastapi import FastAPI, Request, HTTPException
from .config import settings
from .api.webhook import router as webhook_router
from .bot.router import process_update

app = FastAPI()
app.include_router(webhook_router, prefix="/webhook")

@app.on_event("startup")
async def on_startup():
    # Инициализация БД, подключение к Redis и т.д.
    pass

@app.post("/webhook/{token}")
async def telegram_webhook(request: Request, token: str):
    if token != settings.TG_BOT_TOKEN:
        raise HTTPException(status_code=400, detail="Invalid token")
    update = await request.json()
    # Передаём данные в router.handlers

    await process_update(update)
    return {"ok": True}