"""
Application Configuration
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings"""

    PROJECT_NAME: str = "AvatarForge API"
    VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Database settings
    DATABASE_URL: str = Field(
        default="sqlite:///./avatarforge.db",
        description="Database connection URL"
    )

    # Security settings
    SECRET_KEY: str = Field(
        default="your-secret-key-change-this-in-production",
        description="Secret key for JWT tokens"
    )
    API_KEY_NAME: str = "X-API-Key"

    # File storage settings
    STORAGE_PATH: str = Field(
        default="./storage",
        description="Root path for file storage"
    )
    MAX_FILE_SIZE: int = Field(
        default=50 * 1024 * 1024,  # 50MB
        description="Maximum file size in bytes"
    )
    MAX_IMAGE_DIMENSION: int = Field(
        default=4096,
        description="Maximum image dimension (width or height) in pixels"
    )
    MIN_IMAGE_DIMENSION: int = Field(
        default=64,
        description="Minimum image dimension (width or height) in pixels"
    )
    FILE_CLEANUP_DAYS: int = Field(
        default=30,
        description="Delete orphaned files after this many days of no use"
    )

    # ComfyUI settings
    COMFYUI_URL: str = Field(
        default="http://localhost:8188",
        description="ComfyUI API base URL"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
