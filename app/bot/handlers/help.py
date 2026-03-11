"""Handler for /help command."""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.bot_messages import HELP_MESSAGE


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show available commands."""
    await update.message.reply_text(HELP_MESSAGE, parse_mode="Markdown")
