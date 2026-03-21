import logging

import httpx

from app.core.config import settings

_logger = logging.getLogger(__name__)


async def trigger_subscribe() -> None:
    """Notifies the wallet-listener to immediately refresh its subscriptions.

    Called after /startbot. Best-effort: failure does not block activation.
    The periodic refresh (60s) takes over if the listener is unavailable.
    """
    await _post("/subscribe", {})


async def trigger_unsubscribe(wallet_address: str, telegram_id: int) -> None:
    """Notifies the wallet-listener to immediately stop tracking the wallet.

    Called after /stopbot. Best-effort: failure does not block deactivation.
    The periodic refresh (60s) will clean up subscriptions if needed.
    """
    await _post("/unsubscribe", {"wallet_address": wallet_address, "telegram_id": telegram_id})


async def _post(path: str, body: dict) -> None:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.post(f"{settings.LISTENER_URL}{path}", json=body)
            resp.raise_for_status()
            _logger.debug("Wallet-listener %s — OK.", path)
    except httpx.RequestError as exc:
        _logger.warning("Listener unavailable (%s) — falling back to polling: %s", path, exc)
    except httpx.HTTPStatusError as exc:
        _logger.warning(
            "Listener %s — HTTP %s : %s",
            path, exc.response.status_code, exc.response.text[:80],
        )
