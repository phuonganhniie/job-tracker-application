"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import Union
from pydantic import field_validator
import json


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
    
    # CORS - Accept both list and string (JSON or comma-separated)
    BACKEND_CORS_ORIGINS: Union[list, str] = ["http://localhost:8501", "http://localhost:3000"]
    
    @field_validator('BACKEND_CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from various formats"""
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            # Try to parse as JSON first
            v = v.strip()
            if v.startswith('['):
                try:
                    return json.loads(v)
                except json.JSONDecodeError:
                    pass
            # Fallback to comma-separated values
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
