"""HTTP client for configuration and reset operations."""

import httpx

from app.client.backend.base_client import http_client
from app.core.enums.trading_mode import TradingMode
from app.schemas.user_config import UserConfig


async def get_config(telegram_id: int) -> UserConfig | None:
    """Returns None if not found or on network error."""
    try:
        resp = await http_client.get(f"/users/{telegram_id}/config")
        if resp.status_code != 200:
            return None
        return _map_to_user_config(telegram_id, resp.json().get("data", {}))
    except httpx.RequestError:
        return None


async def update_config(telegram_id: int, **fields) -> UserConfig | None:
    """Only the provided kwargs are sent to the backend. None values clear the field in the DB."""
    try:
        resp = await http_client.put(
            f"/users/{telegram_id}/config",
            json=fields,
        )
        if resp.status_code != 200:
            return None
        return _map_to_user_config(telegram_id, resp.json().get("data", {}))
    except httpx.RequestError:
        return None


async def update_wallet_address(
    telegram_id: int,
    address: str,
) -> tuple[UserConfig | None, str | None]:
    """Updates the tracked wallet address with fine-grained validation error handling.

    Returns:
        (UserConfig, None)  : success.
        (None, message)     : invalid wallet (400) — backend error message.
        (None, None)        : backend unavailable or unexpected error.
    """
    try:
        resp = await http_client.put(
            f"/users/{telegram_id}/config",
            json={"wallet_address": address},
        )
        if resp.status_code == 200:
            body = resp.json()
            config = _map_to_user_config(telegram_id, body.get("data", {}))
            warning: str | None = body.get("message")
            return config, warning
        if resp.status_code == 400:
            detail: str = resp.json().get("detail", "Invalid Solana wallet.")
            return None, detail
        return None, None
    except httpx.RequestError:
        return None, None


async def generate_trading_wallet(telegram_id: int) -> dict | None:
    """Generates (or retrieves existing) trading wallet for AUTO mode.

    Returns dict with public_key, or None on error.
    """
    try:
        resp = await http_client.post(f"/users/{telegram_id}/trading-wallet")
        if resp.status_code in (200, 201):
            return resp.json().get("data")
        return None
    except httpx.RequestError:
        return None


async def import_trading_wallet(telegram_id: int, private_key: str) -> dict | None:
    """Import an existing wallet by private key. Returns dict with public_key, or None on error."""
    try:
        resp = await http_client.post(
            f"/users/{telegram_id}/trading-wallet/import",
            json={"private_key": private_key},
        )
        if resp.status_code == 200:
            return resp.json().get("data")
        if resp.status_code == 400:
            detail = resp.json().get("detail", "Invalid private key format.")
            raise ValueError(detail)
        return None
    except httpx.RequestError:
        return None


async def export_trading_wallet(telegram_id: int) -> dict | None:
    """Returns dict with public_key and private_key_bytes, or None on error."""
    try:
        resp = await http_client.get(f"/users/{telegram_id}/trading-wallet/export")
        if resp.status_code == 200:
            return resp.json().get("data")
        return None
    except httpx.RequestError:
        return None


async def reset_user(telegram_id: int) -> bool:
    try:
        resp = await http_client.post(f"/users/{telegram_id}/reset")
        return resp.status_code == 200
    except httpx.RequestError:
        return False


def _map_to_user_config(telegram_id: int, data: dict) -> UserConfig:
    return UserConfig(
        telegram_id=telegram_id,
        wallet_address=data.get("wallet_address"),
        trading_wallet_public_key=data.get("trading_wallet_public_key"),
        trade_amount=float(data["trade_amount"]) if data.get("trade_amount") else None,
        tp_multiplier=float(data["tp_multiplier"]) if data.get("tp_multiplier") else None,
        stop_loss_multiplier=float(data["stop_loss_multiplier"]) if data.get("stop_loss_multiplier") else None,
        entry_market_cap=float(data["entry_market_cap"]) if data.get("entry_market_cap") else None,
        exit_market_cap=float(data["exit_market_cap"]) if data.get("exit_market_cap") else None,
        mode=TradingMode(data.get("mode", TradingMode.PAPER.value)),
        bot_active=data.get("bot_active", False),
        positions=[],
    )
