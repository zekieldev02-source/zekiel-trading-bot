"""Service Telegram pour la gestion des positions paper."""

import uuid

from app.client.backend import position_client


async def get_positions_summary(telegram_id: int) -> dict | None:
    """Retourne le résumé des positions (ouvertes, fermées, PnL agrégé).

    Retourne None si le backend est indisponible.
    """
    return await position_client.get_positions_summary(telegram_id)


async def get_positions(telegram_id: int) -> list[dict] | None:
    """Récupère toutes les positions paper de l'utilisateur.

    Retourne None si le backend est indisponible.
    """
    return await position_client.get_positions(telegram_id)


async def create_position(telegram_id: int, **fields) -> dict | None:
    """Ouvre une nouvelle position paper.

    Retourne les données de la position créée, ou None en cas d'erreur.
    """
    return await position_client.create_position(telegram_id, **fields)


async def close_position(
    telegram_id: int,
    position_id: uuid.UUID,
    **fields,
) -> dict | None:
    """Ferme une position paper et déclenche le calcul du PnL.

    Retourne les données de la position mise à jour, ou None en cas d'erreur.
    """
    return await position_client.close_position(telegram_id, position_id, **fields)


async def delete_positions(telegram_id: int) -> bool:
    """Supprime toutes les positions paper de l'utilisateur.

    Retourne True si la suppression a réussi.
    """
    return await position_client.delete_positions(telegram_id)
