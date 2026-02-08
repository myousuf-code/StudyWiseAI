"""
Application Configuration
Centralized settings management
"""
from decouple import config
from typing import List

class Settings:
    # Application settings
    DEBUG: bool = config("DEBUG", default=True, cast=bool)
    HOST: str = config("HOST", default="127.0.0.1")
    PORT: int = config("PORT", default=8000, cast=int)
    
    # Security
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./studywiseai.db")
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379")
    
    # Local AI Configuration (GPT4All - Free!)
    LOCAL_AI_MODEL: str = config("LOCAL_AI_MODEL", default="orca-mini-3b-gguf2-q4_0.gguf")
    # Legacy OpenAI config (optional)
    OPENAI_API_KEY: str = config("OPENAI_API_KEY", default="")
    OPENAI_MODEL: str = config("OPENAI_MODEL", default="gpt-3.5-turbo")
    
    # CORS Settings
    ALLOWED_HOSTS: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    
    # Email Configuration (for notifications)
    MAIL_USERNAME: str = config("MAIL_USERNAME", default="")
    MAIL_PASSWORD: str = config("MAIL_PASSWORD", default="")
    MAIL_FROM: str = config("MAIL_FROM", default="studywiseai@example.com")
    MAIL_PORT: int = config("MAIL_PORT", default=587, cast=int)
    MAIL_SERVER: str = config("MAIL_SERVER", default="smtp.gmail.com")
    
    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIRECTORY: str = "uploads"

# Create settings instance
settings = Settings()