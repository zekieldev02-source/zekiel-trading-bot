from telegram.ext import ApplicationBuilder, CommandHandler
from app.bot.handlers.start import start
from app.bot.handlers.help import help
from app.bot.handlers.status import status

from app.core.config import settings


def run_bot():
    app = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("status", status))

    app.run_polling()
