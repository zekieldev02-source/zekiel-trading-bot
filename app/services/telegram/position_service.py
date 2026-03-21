"""Telegram service for managing paper positions."""

import uuid

from app.client.backend import position_client
from app.client.backend import trading_client


async def get_positions_summary(telegram_id: int) -> dict | None:
    """Returns None if the backend is unavailable."""
    return await position_client.get_positions_summary(telegram_id)


async def get_positions(telegram_id: int) -> list[dict] | None:
    return await position_client.get_positions(telegram_id)


async def create_position(telegram_id: int, **fields) -> dict | None:
    return await position_client.create_position(telegram_id, **fields)


async def close_position(
    telegram_id: int,
    position_id: uuid.UUID,
    **fields,
) -> dict | None:
    return await position_client.close_position(telegram_id, position_id, **fields)


async def manual_close_position(
    telegram_id: int,
    position_id: uuid.UUID,
) -> dict | str | None:
    """Closes a position manually from a Telegram inline button.

    Reads entry_price from the open-positions snapshot and calls the backend
    with close_reason="manual_close". MVP: exit_price = entry_price (no
    real-time price in paper trading); replace with Birdeye price once
    zekiel-market-stream is live.

    Returns:
        dict: closed position data.
        "already_closed": position already closed or absent from open positions.
        "not_found": position not found on backend.
        None: backend unavailable.
    """
    data = await position_client.get_positions_summary(telegram_id)
    if data is None:
        return None

    open_positions: list[dict] = data.get("open_positions", [])
    position = next(
        (p for p in open_positions if str(p.get("id")) == str(position_id)),
        None,
    )
    if position is None:
        return "already_closed"

    entry_price = float(position.get("entry_price", 0))
    return await trading_client.close_position(
        position_id=position_id,
        exit_price=entry_price,
        close_reason="manual_close",
    )


async def delete_positions(telegram_id: int) -> bool:
    return await position_client.delete_positions(telegram_id)
