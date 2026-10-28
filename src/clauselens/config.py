
"""Application settings loaded from environment variables and .env."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Required Gemini API key
    gemini_api_key: SecretStr

    # Gemini models
    primary_model: str = "gemini-3.1-flash-lite"
    backup_model: str = "gemini-3.5-flash-lite"

    # Retry settings (used in a later step)
    max_retries: int = Field(default=4, ge=0)
    retry_base_wait_s: float = Field(default=2.0, gt=0)
    retry_max_wait_s: float = Field(default=60.0, gt=0)
    request_timeout_s: float = Field(default=60.0, gt=0)

    # Cache and call-log directory (used in later steps)
    cache_dir: Path = Path(".cache")


@lru_cache
def get_settings() -> Settings:
    """Load settings once and reuse them."""
    return Settings()
