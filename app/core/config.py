# config.py
# app/core/config.py
from pydantic import field_validator
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "SUEPR Legal AI"
    DEBUG: bool = True
    GROQ_API_KEY: str
    MAX_FILE_SIZE: int = 10485760

    @field_validator('MAX_FILE_SIZE', mode='before')
    @classmethod
    def clean_max_file_size(cls, v):
        if isinstance(v, str):
            return int(v.split('#')[0].strip())
        return v
    
    class Config:
        env_file = ".env"

settings = Settings()