from fastapi import APIRouter, Request, HTTPException
from app.config import Config
from app.bot.router import process_update
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/{token}")
async def webhook(request: Request, token: str):
    """Обработчик вебхука от Telegram"""
    try:
        # Проверяем валидность токена
        if token != Config.get_bot_token():
            logger.warning(f"Invalid token received: {token}")
            raise HTTPException(status_code=403, detail="Invalid token")
        
        # Получаем и обрабатываем обновление
        update = await request.json()
        logger.debug(f"Received update: {update}")
        await process_update(update)
        
        return {"ok": True}
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")