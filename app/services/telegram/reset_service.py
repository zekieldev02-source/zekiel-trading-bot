"""Service Telegram pour le reset complet d'un utilisateur."""

from app.client.backend import config_client


async def full_reset(telegram_id: int) -> bool:
    """Déclenche un reset complet via le backend :
    - remet la config aux valeurs par défaut
    - supprime toutes les positions paper
    - enregistre un log de reset et un événement

    Retourne True si le reset a réussi, False sinon.
    """
    return await config_client.reset_user(telegram_id)
