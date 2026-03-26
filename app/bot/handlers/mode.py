"""Handler for /mode command.

Usage: /mode paper | /mode auto | /mode manual
No argument → shows current mode with usage hint.
"""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.config_messages import (
    MODE_ALREADY_MESSAGE,
    MODE_INVALID_MESSAGE,
    MODE_SET_AUTO_MESSAGE,
    MODE_SET_MANUAL_MESSAGE,
    MODE_SET_PAPER_MESSAGE,
    MODE_USAGE_MESSAGE,
)
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE
from app.core.enums.trading_mode import TradingMode
from app.services.telegram import config_service

_VALID_MODES = {
    "paper": TradingMode.PAPER,
    "auto": TradingMode.AUTO,
    "manual": TradingMode.MANUAL,
}

_MODE_MESSAGES = {
    TradingMode.PAPER: MODE_SET_PAPER_MESSAGE,
    TradingMode.AUTO: MODE_SET_AUTO_MESSAGE,
    TradingMode.MANUAL: MODE_SET_MANUAL_MESSAGE,
}


async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_id = update.effective_user.id

    config = await config_service.get_config(telegram_id)
    if config is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return

    current_mode = config.mode

    if not context.args:
        await update.message.reply_text(
            MODE_USAGE_MESSAGE.format(current_mode=current_mode.display),
            parse_mode="Markdown",
        )
        return

    raw = context.args[0].strip().lower()
    new_mode = _VALID_MODES.get(raw)

    if new_mode is None:
        await update.message.reply_text(MODE_INVALID_MESSAGE, parse_mode="Markdown")
        return

    if new_mode == current_mode:
        await update.message.reply_text(
            MODE_ALREADY_MESSAGE.format(mode=current_mode.display),
            parse_mode="Markdown",
        )
        return

    updated = await config_service.update_mode(telegram_id, new_mode)
    if updated is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return

    await update.message.reply_text(_MODE_MESSAGES[new_mode], parse_mode="Markdown")
