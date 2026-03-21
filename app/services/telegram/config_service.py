"""Telegram service for managing the trading configuration.

Each action method returns a result code (str) that the handler maps to the
appropriate Telegram message. This service has no knowledge of UI messages.

Common codes:
    "success"        — operation succeeded
    "backend_error"  — backend unavailable or network error
    "already_empty"  — field was already empty, nothing to do
"""

from app.client.backend import config_client
from app.client.listener import listener_client
from app.core.enums.trading_mode import TradingMode
from app.schemas.user_config import UserConfig


async def get_config(telegram_id: int) -> UserConfig | None:
    """Returns None if the backend is unavailable."""
    return await config_client.get_config(telegram_id)


async def update_wallet(
    telegram_id: int,
    address: str,
) -> tuple[UserConfig | None, str | None]:
    """Updates the tracked wallet address.

    Returns:
        (UserConfig, None)  : success.
        (None, message)     : invalid wallet — error message to show the user.
        (None, None)        : backend unavailable.
    """
    return await config_client.update_wallet_address(telegram_id, address)


async def update_trade_amount(telegram_id: int, amount: float) -> UserConfig | None:
    return await config_client.update_config(telegram_id, trade_amount=amount)


async def update_tp_multiplier(telegram_id: int, multiplier: float) -> UserConfig | None:
    return await config_client.update_config(telegram_id, tp_multiplier=multiplier)


async def update_entry_market_cap(telegram_id: int, value: float) -> UserConfig | None:
    return await config_client.update_config(telegram_id, entry_market_cap=value)


async def update_exit_market_cap(telegram_id: int, value: float) -> UserConfig | None:
    return await config_client.update_config(telegram_id, exit_market_cap=value)


async def update_mode(telegram_id: int, mode: TradingMode) -> UserConfig | None:
    """Changes the trading mode (paper / live). Always deactivates the bot to prevent unintended trades."""
    return await config_client.update_config(
        telegram_id,
        mode=mode.value,
        bot_active=False,
        bot_status="idle",
    )


async def activate_bot(telegram_id: int) -> str:
    """Validates prerequisites and activates the trading bot.

    Return codes:
        "success"         — bot activated
        "already_active"  — bot already running
        "missing_wallet"  — wallet not configured
        "missing_amount"  — trade amount not configured
        "backend_error"   — backend unavailable
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if config.bot_active:
        return "already_active"
    if not config.wallet_address:
        return "missing_wallet"
    if not config.trade_amount:
        return "missing_amount"

    updated = await config_client.update_config(telegram_id, bot_active=True, bot_status="active")
    if updated is None:
        return "backend_error"

    await listener_client.trigger_subscribe()
    return "success"


async def deactivate_bot(telegram_id: int) -> str:
    """Deactivates the trading bot.

    Return codes:
        "success"           — bot stopped
        "already_inactive"  — bot already inactive
        "backend_error"     — backend unavailable
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.bot_active:
        return "already_inactive"

    wallet_address = config.wallet_address

    updated = await config_client.update_config(telegram_id, bot_active=False, bot_status="idle")
    if updated is None:
        return "backend_error"

    if wallet_address:
        await listener_client.trigger_unsubscribe(wallet_address, telegram_id)

    return "success"


async def reset_wallet(telegram_id: int) -> str:
    """Clears the wallet and deactivates the bot.

    Return codes:
        "success"            — wallet cleared
        "success_was_active" — wallet cleared, bot also stopped
        "already_empty"      — no wallet configured
        "backend_error"      — backend unavailable
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.wallet_address:
        return "already_empty"

    was_active = config.bot_active
    updated = await config_client.update_config(
        telegram_id,
        wallet_address=None,
        bot_active=False,
        bot_status="idle",
    )
    if updated is None:
        return "backend_error"
    return "success_was_active" if was_active else "success"


async def reset_amount(telegram_id: int) -> str:
    """Clears the trade amount and deactivates the bot.

    Return codes:
        "success"        — amount cleared
        "already_empty"  — no amount configured
        "backend_error"  — backend unavailable
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.trade_amount:
        return "already_empty"

    updated = await config_client.update_config(
        telegram_id,
        trade_amount=None,
        bot_active=False,
        bot_status="idle",
    )
    return "success" if updated is not None else "backend_error"


async def reset_tp(telegram_id: int) -> str:
    """Clears the take-profit multiplier.

    Return codes:
        "success"        — TP cleared
        "already_empty"  — no TP configured
        "backend_error"  — backend unavailable
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.tp_multiplier:
        return "already_empty"

    updated = await config_client.update_config(telegram_id, tp_multiplier=None)
    return "success" if updated is not None else "backend_error"


async def reset_entry_mc(telegram_id: int) -> str:
    """Clears the entry market cap.

    Return codes:
        "success"        — entry MC cleared
        "already_empty"  — not configured
        "backend_error"  — backend unavailable
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.entry_market_cap:
        return "already_empty"

    updated = await config_client.update_config(telegram_id, entry_market_cap=None)
    return "success" if updated is not None else "backend_error"


async def reset_exit_mc(telegram_id: int) -> str:
    """Clears the exit market cap.

    Return codes:
        "success"        — exit MC cleared
        "already_empty"  — not configured
        "backend_error"  — backend unavailable
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.exit_market_cap:
        return "already_empty"

    updated = await config_client.update_config(telegram_id, exit_market_cap=None)
    return "success" if updated is not None else "backend_error"


async def reset_all_fields(telegram_id: int) -> str:
    """Resets all config fields to None and deactivates the bot. Paper positions are kept.

    Return codes:
        "success"       — config reset
        "backend_error" — backend unavailable
    """
    updated = await config_client.update_config(
        telegram_id,
        wallet_address=None,
        trading_wallet_public_key=None,
        trade_amount=None,
        tp_multiplier=None,
        entry_market_cap=None,
        exit_market_cap=None,
        bot_active=False,
        bot_status="idle",
    )
    return "success" if updated is not None else "backend_error"
