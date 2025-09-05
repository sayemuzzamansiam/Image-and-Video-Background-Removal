# app/core/config.py

from pydantic_settings import BaseSettings # <-- THE ONLY CHANGE NEEDED

class Settings(BaseSettings): 
    CLIPDROP_API_KEY: str
    CLIPDROP_API_BASE_URL: str
    
    class Config: 
        env_file = ".env"
        
settings = Settings()