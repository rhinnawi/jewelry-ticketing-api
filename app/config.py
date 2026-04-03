"""
Application configuration module.

Handles all environment-based configuration using Pydantic settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Attributes:
        DATABASE_URL: PostgreSQL connection string.
        CORS_ORIGINS: List of allowed CORS origins.
        JWT_SECRET: Secret key for JWT token signing.
        DEBUG: Debug mode flag.
        API_V1_STR: API v1 prefix path.
    """

    DATABASE_URL: str = "postgresql://jewelry_user:dev_password@db:5432/jewelry_db"
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]
    JWT_SECRET: str = "your-secret-key-change-in-production"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()