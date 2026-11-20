import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = "Student Management API"
    APP_DESCRIPTION = "FastAPI CRUD for students"
    APP_VERSION = "1.0.0"
    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-secret-change-me")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 100

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "")

settings = Settings()