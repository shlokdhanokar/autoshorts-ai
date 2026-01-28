"""
Configuration management for AutoShorts AI system.
Loads settings from environment variables with validation.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import Literal
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # LLM Configuration
    openai_api_key: str = Field(..., description="OpenAI API key")
    anthropic_api_key: str | None = Field(None, description="Anthropic API key (optional)")
    llm_model: str = Field("gpt-4-turbo-preview", description="Default LLM model")
    llm_temperature: float = Field(0.7, ge=0.0, le=2.0)
    
    # TTS Configuration
    elevenlabs_api_key: str | None = Field(None, description="ElevenLabs API key")
    elevenlabs_voice_id: str | None = Field(None, description="Default voice ID")
    tts_provider: Literal["elevenlabs", "openai"] = Field("openai", description="TTS provider")
    
    # Media Generation
    stability_api_key: str | None = Field(None, description="Stability AI API key")
    pexels_api_key: str | None = Field(None, description="Pexels API key")
    pixabay_api_key: str | None = Field(None, description="Pixabay API key")
    
    # Social Media - YouTube
    youtube_client_id: str | None = None
    youtube_client_secret: str | None = None
    youtube_refresh_token: str | None = None
    
    # Social Media - Instagram
    instagram_access_token: str | None = None
    instagram_business_account_id: str | None = None
    
    # Database
    database_url: str = Field("sqlite:///autoshorts.db", description="Database connection URL")
    
    # Redis
    redis_url: str = Field("redis://localhost:6379/0", description="Redis connection URL")
    
    # System Configuration
    environment: Literal["development", "staging", "production"] = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    max_concurrent_videos: int = Field(3, ge=1, le=10)
    
    # Cost Controls
    max_daily_api_cost: float = Field(50.0, ge=0.0)
    enable_cost_tracking: bool = True
    
    # Content Settings
    default_niche: str = "self-improvement"
    posting_frequency: Literal["hourly", "daily", "weekly"] = "daily"
    auto_publish: bool = False
    
    # Content Moderation
    enable_content_moderation: bool = True
    require_human_review: bool = False
    
    # Paths
    data_dir: str = Field("data", description="Data directory path")
    videos_dir: str = Field("data/videos", description="Videos output directory")
    assets_dir: str = Field("data/assets", description="Assets cache directory")
    cache_dir: str = Field("data/cache", description="General cache directory")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @validator("data_dir", "videos_dir", "assets_dir", "cache_dir")
    def ensure_directory_exists(cls, v):
        """Ensure directories exist."""
        os.makedirs(v, exist_ok=True)
        return v


# Global settings instance
settings = Settings()
