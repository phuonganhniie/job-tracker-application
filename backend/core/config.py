"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "Job Tracker API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./job_tracker.db"
    # For PostgreSQL in production:
    # DATABASE_URL: str = "postgresql://user:password@localhost/job_tracker"
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: list = ["http://localhost:8501", "http://localhost:3000"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
