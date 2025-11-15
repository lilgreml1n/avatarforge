"""
Application Configuration
"""
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
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

    # Scheduled tasks settings
    ENABLE_SCHEDULER: bool = Field(
        default=True,
        description="Enable APScheduler for automated cleanup jobs"
    )
    CLEANUP_SCHEDULE_HOUR: int = Field(
        default=2,
        description="Hour (0-23) to run daily cleanup"
    )

    # ComfyUI settings
    COMFYUI_URL: str = Field(
        default="http://localhost:8188",
        description="ComfyUI API base URL"
    )

    # Model Configuration (SDXL Checkpoints)
    DEFAULT_CHECKPOINT: str = Field(
        default="RealVisXL_V5.0.safetensors",
        description="Default checkpoint model for generation"
    )
    REALISTIC_CHECKPOINT: str = Field(
        default="RealVisXL_V5.0.safetensors",
        description="Checkpoint for photorealistic generation (realism=true)"
    )
    ANIME_CHECKPOINT: str = Field(
        default="JuggernautXL_v10.safetensors",
        description="Checkpoint for anime/stylized generation (realism=false)"
    )

    # Upscaler Configuration
    PRIMARY_UPSCALER: str = Field(
        default="RealESRGAN_x4plus.pth",
        description="Primary upscaler model for 4K generation"
    )
    SECONDARY_UPSCALER: str = Field(
        default="4x-UltraSharp.pth",
        description="Secondary upscaler for extra sharpness (optional)"
    )
    ENABLE_UPSCALING: bool = Field(
        default=True,
        description="Enable 4K upscaling by default"
    )

    # Quality Settings for Photorealism
    DEFAULT_STEPS: int = Field(
        default=30,
        description="Default number of sampling steps"
    )
    REALISTIC_STEPS: int = Field(
        default=35,
        description="Steps for photorealistic generation (higher = better quality)"
    )
    DEFAULT_CFG: float = Field(
        default=7.0,
        description="Default CFG scale (guidance strength)"
    )
    DEFAULT_SAMPLER: str = Field(
        default="dpmpp_2m_sde_gpu",
        description="Default sampler for generation"
    )
    DEFAULT_SCHEDULER: str = Field(
        default="karras",
        description="Default scheduler for generation"
    )

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
