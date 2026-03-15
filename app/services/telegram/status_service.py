"""Service Telegram pour l'affichage du statut et des paramètres."""

from app.client.backend import config_client
from app.schemas.user_config import UserConfig


async def get_status(telegram_id: int) -> UserConfig | None:
    """Récupère la configuration complète pour l'affichage du statut et des paramètres.

    Retourne None si le backend est indisponible.
    """
    return await config_client.get_config(telegram_id)
