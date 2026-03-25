"""Telegram service for managing paper positions."""

import uuid

from app.client.backend import position_client
from app.client.backend import trading_client
from app.client import dexscreener_client


async def get_positions_summary(telegram_id: int) -> dict | None:
    """Returns positions summary enriched with current market caps from DexScreener."""
    data = await position_client.get_positions_summary(telegram_id)
    if data is None:
        return None

    open_positions: list[dict] = data.get("open_positions", [])
    if not open_positions:
        return data

    addresses = [p["token_address"] for p in open_positions if p.get("token_address")]
    market_data = await dexscreener_client.get_tokens_market_data(addresses)

    for position in open_positions:
        addr = position.get("token_address", "")
        token_data = market_data.get(addr)
        if token_data and token_data.market_cap is not None:
            position["current_market_cap"] = float(token_data.market_cap)

    return data


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

    Fetches the current price from DexScreener and uses it as exit_price.
    Falls back to entry_price if DexScreener is unavailable.

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

    token_address: str = position.get("token_address", "")
    entry_price = float(position.get("entry_price", 0))

    current_price = await dexscreener_client.get_token_price(token_address)
    exit_price = float(current_price) if current_price else entry_price

    return await trading_client.close_position(
        position_id=position_id,
        exit_price=exit_price,
        close_reason="manual_close",
    )


async def delete_positions(telegram_id: int) -> bool:
    return await position_client.delete_positions(telegram_id)
