"""Client HTTP pour les opérations sur les positions paper."""

import uuid

import httpx

from app.client.backend.base_client import http_client


async def get_positions_summary(telegram_id: int) -> dict | None:
    """Récupère le résumé des positions paper (ouvertes, fermées, PnL agrégé).

    Retourne None en cas d'erreur réseau ou de réponse inattendue.
    """
    try:
        resp = await http_client.get(f"/users/{telegram_id}/positions/summary")
        if resp.status_code != 200:
            return None
        return resp.json().get("data")
    except httpx.RequestError:
        return None


async def get_positions(telegram_id: int) -> list[dict] | None:
    """Récupère toutes les positions paper d'un utilisateur.

    Retourne None en cas d'erreur réseau.
    """
    try:
        resp = await http_client.get(f"/users/{telegram_id}/positions")
        if resp.status_code != 200:
            return None
        return resp.json().get("data", [])
    except httpx.RequestError:
        return None


async def create_position(telegram_id: int, **fields) -> dict | None:
    """Ouvre une nouvelle position paper.

    Retourne les données de la position créée, ou None en cas d'erreur.
    """
    try:
        resp = await http_client.post(f"/users/{telegram_id}/positions", json=fields)
        if resp.status_code not in (200, 201):
            return None
        return resp.json().get("data")
    except httpx.RequestError:
        return None


async def close_position(
    telegram_id: int,
    position_id: uuid.UUID,
    **fields,
) -> dict | None:
    """Ferme une position paper existante.

    Retourne les données de la position mise à jour, ou None en cas d'erreur.
    """
    try:
        resp = await http_client.patch(
            f"/users/{telegram_id}/positions/{position_id}/close",
            json=fields,
        )
        if resp.status_code != 200:
            return None
        return resp.json().get("data")
    except httpx.RequestError:
        return None


async def delete_positions(telegram_id: int) -> bool:
    """Supprime toutes les positions paper d'un utilisateur.

    Retourne True si la suppression a réussi.
    """
    try:
        resp = await http_client.delete(f"/users/{telegram_id}/positions")
        return resp.status_code == 200
    except httpx.RequestError:
        return False
