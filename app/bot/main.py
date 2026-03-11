from telegram.ext import ApplicationBuilder

from app.bot.register_handlers import register_all_handlers
from app.core.config import settings


def run_bot() -> None:
    """Build the Telegram application and start polling."""
    app = ApplicationBuilder().token(settings.BOT_TOKEN).build()
    register_all_handlers(app)
    app.run_polling()
