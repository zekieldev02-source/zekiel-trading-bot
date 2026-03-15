"""Handler for /start command."""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.bot_messages import START_MESSAGE
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE
from app.services.telegram import start_service


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome the user and register them in the backend if not already known."""
    user = update.effective_user
    success = await start_service.register_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    if not success:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return
    await update.message.reply_text(START_MESSAGE, parse_mode="Markdown")
