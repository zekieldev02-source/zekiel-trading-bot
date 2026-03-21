"""HTTP client for user operations (POST/GET/DELETE /users)."""

import httpx

from app.client.backend.base_client import http_client


async def create_user(
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
) -> bool:
    """Returns True on 201 (created) or 409 (already exists). False on network error."""
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
    try:
        resp = await http_client.get(f"/users/{telegram_id}")
        if resp.status_code != 200:
            return None
        return resp.json().get("data")
    except httpx.RequestError:
        return None


async def delete_user(telegram_id: int) -> bool:
    try:
        resp = await http_client.delete(f"/users/{telegram_id}")
        return resp.status_code == 200
    except httpx.RequestError:
        return False
