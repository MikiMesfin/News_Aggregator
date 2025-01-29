from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    NEWS_API_KEY: str  # If you plan to use NewsAPI
    
    class Config:
        env_file = ".env"

settings = Settings()
    