import os
from functools import lru_cache
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings loaded from environment variables."""
    APP_ENV: str = Field(default=os.getenv("APP_ENV", "development"), description="Application environment")
    PORT: int = Field(default=int(os.getenv("PORT", "3001")), description="Port to bind server on")
    MONGO_URI: str = Field(default=os.getenv("MONGO_URI", ""), description="MongoDB connection string (URI)")
    MONGO_DB_NAME: str = Field(default=os.getenv("MONGO_DB_NAME", ""), description="MongoDB database name")
    JWT_SECRET: str = Field(default=os.getenv("JWT_SECRET", ""), description="JWT secret key (placeholder)")
    JWT_ALGORITHM: str = Field(default=os.getenv("JWT_ALGORITHM", "HS256"), description="JWT algorithm")
    CORS_ORIGINS: str = Field(default=os.getenv("CORS_ORIGINS", "http://localhost:3000"), description="CSV of allowed CORS origins")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and validate settings from environment.

    Raises:
        ValueError: when required settings are missing.

    Returns:
        Settings: validated settings instance.
    """
    settings = Settings()
    missing = []
    if not settings.MONGO_URI:
        missing.append("MONGO_URI")
    if not settings.MONGO_DB_NAME:
        missing.append("MONGO_DB_NAME")
    if not settings.JWT_SECRET:
        missing.append("JWT_SECRET")
    if missing:
        # Provide a clear message; actual secrets are not logged.
        raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
    return settings
