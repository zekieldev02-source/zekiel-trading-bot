"""Handlers for /startbot and /stopbot."""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.bot_messages import (
    BOT_ALREADY_ACTIVE_MESSAGE,
    BOT_ALREADY_STOPPED_MESSAGE,
    BOT_STARTED_MESSAGE,
    BOT_STOPPED_MESSAGE,
)
from app.core.constants import UserDataKeys
from app.services.user_config_service import UserConfigService


async def start_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Activate copy trading."""
    UserConfigService.init_user_data(context.user_data)

    if context.user_data.get(UserDataKeys.BOT_ACTIVE):
        await update.message.reply_text(BOT_ALREADY_ACTIVE_MESSAGE)
        return

    success, error = UserConfigService.activate(context.user_data)
    if not success:
        await update.message.reply_text(error, parse_mode="Markdown")
        return

    await update.message.reply_text(BOT_STARTED_MESSAGE, parse_mode="Markdown")


async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Deactivate copy trading."""
    UserConfigService.init_user_data(context.user_data)

    if not context.user_data.get(UserDataKeys.BOT_ACTIVE):
        await update.message.reply_text(BOT_ALREADY_STOPPED_MESSAGE)
        return

    UserConfigService.deactivate(context.user_data)
    await update.message.reply_text(BOT_STOPPED_MESSAGE, parse_mode="Markdown")
