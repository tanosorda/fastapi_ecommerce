import os
from typing import Optional
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class Config:
    @staticmethod
    def get_bot_token() -> str:
        token = os.getenv("BOT_TOKEN")
        if not token:
            raise ValueError("BOT_TOKEN не найден в .env файле")
        return token

    @staticmethod
    def get_postgres_url() -> str:
        url = os.getenv("POSTGRES_URL")
        if not url:
            raise ValueError("POSTGRES_URL не найден в .env файле")
        return url

    @staticmethod
    def get_api_base_url() -> str:
        return os.getenv("API_BASE_URL", "")