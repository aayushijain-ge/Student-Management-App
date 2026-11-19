import os

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
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

settings = Settings()