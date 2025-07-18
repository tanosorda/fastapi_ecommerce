from pydantic import BaseSettings

class Settings(BaseSettings):
    TG_BOT_TOKEN: str
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"

settings = Settings()