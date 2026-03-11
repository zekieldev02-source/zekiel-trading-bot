"""Handler for /start command."""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.bot_messages import START_MESSAGE
from app.services.user_config_service import UserConfigService


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome the user and initialize their config with defaults."""
    telegram_id = update.effective_user.id
    UserConfigService.init_user_data(context.user_data, telegram_id=telegram_id)
    await update.message.reply_text(START_MESSAGE, parse_mode="Markdown")
