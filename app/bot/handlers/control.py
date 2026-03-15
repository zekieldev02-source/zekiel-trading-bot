"""Handlers for /startbot and /stopbot."""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.bot_messages import (
    BOT_ALREADY_ACTIVE_MESSAGE,
    BOT_ALREADY_STOPPED_MESSAGE,
    BOT_STARTED_MESSAGE,
    BOT_STOPPED_MESSAGE,
)
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE
from app.services.telegram import config_service

_MISSING_WALLET_MESSAGE = "❌ Veuillez d'abord configurer un wallet avec /setwallet"
_MISSING_AMOUNT_MESSAGE = "❌ Veuillez d'abord configurer un montant avec /setamount"


async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Activate copy trading."""
    telegram_id = update.effective_user.id
    result = await config_service.activate_bot(telegram_id)

    messages = {
        "success": (BOT_STARTED_MESSAGE, "Markdown"),
        "already_active": (BOT_ALREADY_ACTIVE_MESSAGE, None),
        "missing_wallet": (_MISSING_WALLET_MESSAGE, "Markdown"),
        "missing_amount": (_MISSING_AMOUNT_MESSAGE, "Markdown"),
        "backend_error": (BACKEND_UNAVAILABLE_MESSAGE, None),
    }
    text, parse_mode = messages[result]
    await update.message.reply_text(text, parse_mode=parse_mode)


async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deactivate copy trading."""
    telegram_id = update.effective_user.id
    result = await config_service.deactivate_bot(telegram_id)

    messages = {
        "success": (BOT_STOPPED_MESSAGE, "Markdown"),
        "already_inactive": (BOT_ALREADY_STOPPED_MESSAGE, None),
        "backend_error": (BACKEND_UNAVAILABLE_MESSAGE, None),
    }
    text, parse_mode = messages[result]
    await update.message.reply_text(text, parse_mode=parse_mode)
