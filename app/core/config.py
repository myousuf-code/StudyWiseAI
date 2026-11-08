"""
Application Configuration
Centralized settings management
"""
import sys
from decouple import config, UndefinedValueError
from typing import List

class Settings:
    # Application settings
    DEBUG: bool = config("DEBUG", default=False, cast=bool)
    HOST: str = config("HOST", default="127.0.0.1")
    PORT: int = config("PORT", default=8000, cast=int)

    # Security — SECRET_KEY MUST be set via environment variable. No default allowed.
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./studywiseai.db")
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379")

    # Local AI Configuration (GPT4All — used only if Groq key not set)
    LOCAL_AI_MODEL: str = config("LOCAL_AI_MODEL", default="orca-mini-3b-gguf2-q4_0.gguf")
    LOCAL_AI_FALLBACK_MODEL: str = config("LOCAL_AI_FALLBACK_MODEL", default="Phi-3-mini-4k-instruct.Q4_0.gguf")
    # Groq API (primary AI provider — fast, free tier, no local model needed)
    GROQ_API_KEY: str = config("GROQ_API_KEY", default="")
    GROQ_MODEL: str = config("GROQ_MODEL", default="llama-3.1-8b-instant")

    # CORS — production origins only; dev origins injected via CORS_EXTRA_ORIGINS env var
    ALLOWED_HOSTS: List[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]
    _cors_extra: str = config("CORS_EXTRA_ORIGINS", default="")
    CORS_EXTRA_ORIGINS: List[str] = [o.strip() for o in _cors_extra.split(",") if o.strip()]

    # Email Configuration (for notifications)
    MAIL_USERNAME: str = config("MAIL_USERNAME", default="")
    MAIL_PASSWORD: str = config("MAIL_PASSWORD", default="")
    MAIL_FROM: str = config("MAIL_FROM", default="studywiseai@example.com")
    MAIL_PORT: int = config("MAIL_PORT", default=587, cast=int)
    MAIL_SERVER: str = config("MAIL_SERVER", default="smtp.gmail.com")

    # File upload settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIRECTORY: str = "uploads"

try:
    settings = Settings()
except UndefinedValueError:
    print(
        "FATAL: SECRET_KEY environment variable is not set. "
        "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\" "
        "and add it to your .env file or environment before starting the server.",
        file=sys.stderr,
    )
    sys.exit(1)