# app/core/config.py

from pydantic import BaseSettings

class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    debug: bool = True

settings = Settings()