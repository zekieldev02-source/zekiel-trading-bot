"""Application settings loaded from .env via Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    BOT_TOKEN: str
    ENV: str = "development"
    BACKEND_URL: str = "http://localhost:8000"
    LISTENER_URL: str = "http://localhost:8001"


settings = Settings()
