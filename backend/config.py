import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    _raw_db_url = os.environ.get("DATABASE_URL", "")
    if _raw_db_url.startswith("postgres://"):
        _raw_db_url = _raw_db_url.replace("postgres://", "postgresql+psycopg://", 1)
    elif _raw_db_url.startswith("postgresql://"):
        _raw_db_url = _raw_db_url.replace("postgresql://", "postgresql+psycopg://", 1)

    SQLALCHEMY_DATABASE_URI = _raw_db_url
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  
        "pool_recycle": 280,   
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET = os.environ.get("JWT_SECRET", "dev-secret-change-me")
    JWT_EXPIRY_DAYS = 7

    GOOGLE_AI_STUDIO_KEY = os.environ.get("GOOGLE_AI_STUDIO_KEY", "")
    GEMMA_MODEL = "gemma-4-26b-a4b-it"

    FRONTEND_ORIGINS = os.environ.get("FRONTEND_ORIGINS", "*").split(",")