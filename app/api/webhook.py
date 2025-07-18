from fastapi import APIRouter, Request, HTTPException
from ..config import settings
from ..bot.router import process_update

router = APIRouter()

@router.post("/{token}")
async def webhook(request: Request, token: str):
    if token != settings.TG_BOT_TOKEN:
        raise HTTPException(400)
    update = await request.json()
    await process_update(update)
    return {"ok": True}