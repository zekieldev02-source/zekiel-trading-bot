"""Telegram service for registering a user on startup."""

from app.client.backend import user_client


async def register_user(
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> bool:
    """Registers the user in the backend. Idempotent: silent on 409. Returns True on 201/409."""
    return await user_client.create_user(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
