"""Telegram service for displaying bot status and settings."""

from app.client.backend import config_client
from app.schemas.user_config import UserConfig


async def get_status(telegram_id: int) -> UserConfig | None:
    """Returns None if the backend is unavailable."""
    return await config_client.get_config(telegram_id)
