"""HTTP client for paper position operations."""

import uuid

import httpx

from app.client.backend.base_client import http_client


async def get_positions_summary(telegram_id: int) -> dict | None:
    try:
        resp = await http_client.get(f"/users/{telegram_id}/positions/summary")
        if resp.status_code != 200:
            return None
        return resp.json().get("data")
    except httpx.RequestError:
        return None


async def get_positions(telegram_id: int) -> list[dict] | None:
    try:
        resp = await http_client.get(f"/users/{telegram_id}/positions")
        if resp.status_code != 200:
            return None
        return resp.json().get("data", [])
    except httpx.RequestError:
        return None


async def create_position(telegram_id: int, **fields) -> dict | None:
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
    try:
        resp = await http_client.delete(f"/users/{telegram_id}/positions")
        return resp.status_code == 200
    except httpx.RequestError:
        return False
