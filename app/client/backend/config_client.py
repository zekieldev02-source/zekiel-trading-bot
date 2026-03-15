"""Client HTTP pour les opérations sur la configuration et les resets."""

import httpx

from app.client.backend.base_client import http_client
from app.core.enums.trading_mode import TradingMode
from app.schemas.user_config import UserConfig


async def get_config(telegram_id: int) -> UserConfig | None:
    """Récupère la configuration de trading et la convertit en UserConfig.

    Retourne None si introuvable ou en cas d'erreur réseau.
    """
    try:
        resp = await http_client.get(f"/users/{telegram_id}/config")
        if resp.status_code != 200:
            return None
        return _map_to_user_config(telegram_id, resp.json().get("data", {}))
    except httpx.RequestError:
        return None


async def update_config(telegram_id: int, **fields) -> UserConfig | None:
    """Met à jour les champs fournis dans la configuration.

    Seuls les champs passés en kwargs sont envoyés au backend.
    Les champs passés à None effacent la valeur en base.
    Retourne None en cas d'erreur réseau ou de réponse non-200.
    """
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


async def reset_user(telegram_id: int) -> bool:
    """Déclenche un reset complet : config par défaut + positions supprimées + log.

    Retourne True si le reset a réussi.
    """
    try:
        resp = await http_client.post(f"/users/{telegram_id}/reset")
        return resp.status_code == 200
    except httpx.RequestError:
        return False


def _map_to_user_config(telegram_id: int, data: dict) -> UserConfig:
    """Convertit la réponse brute de l'API en UserConfig Pydantic."""
    return UserConfig(
        telegram_id=telegram_id,
        wallet_address=data.get("wallet_address"),
        trading_wallet_public_key=data.get("trading_wallet_public_key"),
        trade_amount=float(data["trade_amount"]) if data.get("trade_amount") else None,
        tp_multiplier=float(data["tp_multiplier"]) if data.get("tp_multiplier") else None,
        entry_market_cap=float(data["entry_market_cap"]) if data.get("entry_market_cap") else None,
        exit_market_cap=float(data["exit_market_cap"]) if data.get("exit_market_cap") else None,
        mode=TradingMode(data.get("mode", TradingMode.PAPER.value)),
        bot_active=data.get("bot_active", False),
        positions=[],
    )
