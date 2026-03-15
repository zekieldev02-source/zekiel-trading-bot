"""HTTP client asynchrone vers le backend Zekiel Trading Bot.

Toutes les interactions avec l'API backend passent par cette classe.
Les méthodes retournent des objets UserConfig compatibles avec les fonctions
de message existantes, ou None si la requête échoue.
"""

import httpx

from app.core.config import settings
from app.core.enums.trading_mode import TradingMode
from app.schemas.user_config import UserConfig


class BackendClient:
    """Client HTTP async vers le backend FastAPI."""

    def __init__(self, base_url: str) -> None:
        self._client = httpx.AsyncClient(base_url=base_url, timeout=10.0)

    async def create_user(
        self,
        telegram_id: int,
        username: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
    ) -> bool:
        """Crée un utilisateur et initialise sa config par défaut.

        Retourne True si créé, False si déjà existant (409) ou en cas d'erreur.
        Un 409 n'est pas une erreur : l'utilisateur existe déjà, on continue normalement.
        """
        try:
            resp = await self._client.post(
                "/users",
                json={
                    "telegram_id": telegram_id,
                    "telegram_username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )
            return resp.status_code == 201
        except httpx.RequestError:
            return False

    async def get_config(self, telegram_id: int) -> UserConfig | None:
        """Récupère la configuration de trading et la mappe en UserConfig.

        Retourne None si l'utilisateur n'existe pas ou en cas d'erreur réseau.
        """
        try:
            resp = await self._client.get(f"/users/{telegram_id}/config")
            if resp.status_code != 200:
                return None
            data = resp.json().get("data", {})
            return _map_to_user_config(telegram_id, data)
        except httpx.RequestError:
            return None

    async def update_config(self, telegram_id: int, **fields) -> UserConfig | None:
        """Met à jour les champs fournis dans la configuration.

        Seuls les champs passés en kwargs sont envoyés au backend (patch partiel).
        Les champs explicitement passés à None effacent la valeur en base.
        Retourne le UserConfig mis à jour, ou None en cas d'erreur.
        """
        try:
            resp = await self._client.put(
                f"/users/{telegram_id}/config",
                json=fields,
            )
            if resp.status_code != 200:
                return None
            data = resp.json().get("data", {})
            return _map_to_user_config(telegram_id, data)
        except httpx.RequestError:
            return None

    async def reset_user(self, telegram_id: int) -> bool:
        """Reset complet : config par défaut + positions supprimées + log enregistré.

        Retourne True si le reset a réussi.
        """
        try:
            resp = await self._client.post(f"/users/{telegram_id}/reset")
            return resp.status_code == 200
        except httpx.RequestError:
            return False


def _map_to_user_config(telegram_id: int, data: dict) -> UserConfig:
    """Convertit la réponse API en UserConfig compatible avec les fonctions de message."""
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


# Instance singleton utilisée par tous les handlers
backend_client = BackendClient(base_url=settings.BACKEND_URL)
