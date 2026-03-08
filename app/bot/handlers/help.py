from app.bot.messages.help_messages import HELP_MESSAGE
from telegram import Update
from telegram.ext import ContextTypes


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        HELP_MESSAGE
    )
