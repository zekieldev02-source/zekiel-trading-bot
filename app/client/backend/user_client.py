"""Client HTTP pour les opérations sur les utilisateurs (POST/GET/DELETE /users)."""

import httpx

from app.client.backend.base_client import http_client


async def create_user(
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> bool:
    """Crée un utilisateur en base.

    Retourne True si créé (201) ou déjà existant (409).
    Retourne False en cas d'erreur réseau.
    """
    try:
        resp = await http_client.post(
            "/users",
            json={
                "telegram_id": telegram_id,
                "telegram_username": username,
                "first_name": first_name,
                "last_name": last_name,
            },
        )
        return resp.status_code in (201, 409)
    except httpx.RequestError:
        return False


async def get_user(telegram_id: int) -> dict | None:
    """Récupère les données brutes d'un utilisateur.

    Retourne None si introuvable ou en cas d'erreur réseau.
    """
    try:
        resp = await http_client.get(f"/users/{telegram_id}")
        if resp.status_code != 200:
            return None
        return resp.json().get("data")
    except httpx.RequestError:
        return None


async def delete_user(telegram_id: int) -> bool:
    """Supprime un utilisateur et toutes ses données liées.

    Retourne True si la suppression a réussi.
    """
    try:
        resp = await http_client.delete(f"/users/{telegram_id}")
        return resp.status_code == 200
    except httpx.RequestError:
        return False
