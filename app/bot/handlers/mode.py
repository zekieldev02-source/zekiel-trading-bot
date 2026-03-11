"""Simple handler for /mode command.

Usage: /mode paper | /mode live
No argument → shows current mode with usage hint.
"""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.config_messages import (
    MODE_ALREADY_MESSAGE,
    MODE_INVALID_MESSAGE,
    MODE_SET_LIVE_MESSAGE,
    MODE_SET_PAPER_MESSAGE,
    MODE_USAGE_MESSAGE,
)
from app.core.enums.trading_mode import TradingMode
from app.services.user_config_service import UserConfigService


async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set trading mode via /mode paper or /mode live."""
    UserConfigService.init_user_data(context.user_data)
    current_mode = UserConfigService.get_mode(context.user_data)

    # No argument → show current mode + usage
    if not context.args:
        await update.message.reply_text(
            MODE_USAGE_MESSAGE.format(current_mode=current_mode.display),
            parse_mode="Markdown",
        )
        return

    raw = context.args[0].strip().lower()

    if raw not in ("paper", "live"):
        await update.message.reply_text(MODE_INVALID_MESSAGE, parse_mode="Markdown")
        return

    new_mode = TradingMode(raw)

    if new_mode == current_mode:
        await update.message.reply_text(
            MODE_ALREADY_MESSAGE.format(mode=current_mode.display),
            parse_mode="Markdown",
        )
        return

    UserConfigService.set_mode(context.user_data, new_mode)

    if new_mode == TradingMode.PAPER:
        await update.message.reply_text(MODE_SET_PAPER_MESSAGE, parse_mode="Markdown")
    else:
        await update.message.reply_text(MODE_SET_LIVE_MESSAGE, parse_mode="Markdown")
