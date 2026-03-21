"""Telegram service for performing a full user reset."""

from app.client.backend import config_client


async def full_reset(telegram_id: int) -> bool:
    """Triggers a full reset via the backend: resets config to defaults, deletes all paper
    positions, and records a reset log and event. Returns True on success.
    """
    return await config_client.reset_user(telegram_id)
