from app.bot.enums.status import BotStatus
from app.bot.messages.status_messages import get_status_message
from telegram import Update
from telegram.ext import ContextTypes


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = get_status_message(BotStatus.RUNNING)
    await update.message.reply_text(
        message,
        parse_mode="Markdown"
    )
