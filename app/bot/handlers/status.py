"""Handler for /status command."""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.bot_messages import get_status_message
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE
from app.services.telegram import status_service


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the user's current bot status and configuration summary."""
    telegram_id = update.effective_user.id
    config = await status_service.get_status(telegram_id)
    if config is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return
    message = get_status_message(config)
    await update.message.reply_text(message, parse_mode="Markdown")
