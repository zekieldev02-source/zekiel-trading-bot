import uuid

import httpx

from app.client.backend.base_client import http_client


async def simulate_buy(
    telegram_id: int,
    token_address: str,
    entry_price: float,
    token_symbol: str | None = None,
    market_cap: float | None = None,
) -> dict | None:
    try:
        payload: dict = {
            "token_address": token_address,
            "entry_price": entry_price,
        }
        if token_symbol is not None:
            payload["token_symbol"] = token_symbol
        if market_cap is not None:
            payload["market_cap"] = market_cap

        resp = await http_client.post(
            f"/paper-trading/users/{telegram_id}/simulate-buy",
            json=payload,
        )
        if resp.status_code != 201:
            return None
        return resp.json().get("data")
    except httpx.RequestError:
        return None


async def execute_copy_trade(
    signal_id: str,
    telegram_id: int,
) -> dict | str | None:
    """Executes a copy trade from a pending signal.

    Returns:
        dict: opened position data (201).
        "already_open": position already open for this token (409).
        "signal_not_found": expired or already consumed signal (404).
        "expired": signal expired on the backend side (410).
        None: network error or unexpected response.
    """
    try:
        resp = await http_client.post(
            f"/paper-trading/signals/{signal_id}/execute",
            json={"telegram_id": telegram_id},
        )
        if resp.status_code == 201:
            return resp.json().get("data")
        if resp.status_code == 409:
            return "already_open"
        if resp.status_code == 404:
            return "signal_not_found"
        if resp.status_code == 410:
            return "expired"
        return None
    except httpx.RequestError:
        return None


async def close_position(
    position_id: uuid.UUID,
    exit_price: float,
    exit_market_cap: float | None = None,
    close_reason: str = "manual_close",
) -> dict | str | None:
    """Closes a paper position.

    Returns:
        dict: closed position data (200).
        "already_closed": position already closed (409).
        "not_found": position not found (404).
        None: network error or unexpected response.
    """
    try:
        payload: dict = {
            "exit_price": exit_price,
            "close_reason": close_reason,
        }
        if exit_market_cap is not None:
            payload["exit_market_cap"] = exit_market_cap

        resp = await http_client.patch(
            f"/paper-trading/positions/{position_id}/close",
            json=payload,
        )
        if resp.status_code == 200:
            return resp.json().get("data")
        if resp.status_code == 409:
            return "already_closed"
        if resp.status_code == 404:
            return "not_found"
        return None
    except httpx.RequestError:
        return None
