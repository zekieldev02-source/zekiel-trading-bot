"""Handler for /settings command."""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.bot_messages import get_settings_message
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE
from app.services.telegram import status_service


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the user's current configuration."""
    telegram_id = update.effective_user.id
    config = await status_service.get_status(telegram_id)
    if config is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return
    message = get_settings_message(config)
    await update.message.reply_text(message, parse_mode="Markdown")
