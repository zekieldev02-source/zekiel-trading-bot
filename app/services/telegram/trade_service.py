from app.client.backend import trading_client


async def execute_copy_trade(telegram_id: int, signal_id: str) -> dict | str | None:
    """Executes a copy trade from a Telegram signal.

    Returns:
        dict: opened position data.
        "already_open": token already has an open position.
        "signal_not_found": unknown or already consumed signal.
        "expired": signal expired (> 10 min).
        None: backend unavailable.
    """
    return await trading_client.execute_copy_trade(signal_id, telegram_id)
