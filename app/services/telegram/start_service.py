"""Service Telegram pour l'enregistrement d'un utilisateur au démarrage."""

from app.client.backend import user_client


async def register_user(
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> bool:
    """Enregistre l'utilisateur dans le backend.

    Idempotent : silencieux si l'utilisateur existe déjà (409).
    Retourne True si l'enregistrement a réussi (201 ou 409).
    Retourne False si le backend est indisponible.
    """
    return await user_client.create_user(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
