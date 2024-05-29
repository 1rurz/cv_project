import os
from pathlib import Path
from pydantic import BaseSettings
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    db_echo: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
