# app/core/config.py

from pydantic_settings import BaseSettings # <-- THE ONLY CHANGE NEEDED

class Settings(BaseSettings): 
    SLAZZER_API_KEY: str
    
    class Config: 
        env_file = ".env"
        
settings = Settings()