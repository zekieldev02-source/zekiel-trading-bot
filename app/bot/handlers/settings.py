"""Handler for /settings command."""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.bot_messages import get_settings_message
from app.services.user_config_service import UserConfigService


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the user's current configuration."""
    UserConfigService.init_user_data(context.user_data)
    config = UserConfigService.get_config(context.user_data)
    message = get_settings_message(config)
    await update.message.reply_text(message, parse_mode="Markdown")
