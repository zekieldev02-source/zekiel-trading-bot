"""Handler pour la commande /positions."""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE
from app.bot.messages.position_messages import NO_POSITIONS_MESSAGE, get_positions_message
from app.services.telegram import position_service


async def positions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Affiche les positions paper ouvertes et un résumé des positions fermées."""
    telegram_id = update.effective_user.id

    data = await position_service.get_positions_summary(telegram_id)

    if data is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return

    summary = data.get("summary", {})
    has_positions = summary.get("open_count", 0) > 0 or summary.get("closed_count", 0) > 0

    if not has_positions:
        await update.message.reply_text(NO_POSITIONS_MESSAGE, parse_mode="Markdown")
        return

    message = get_positions_message(data)
    await update.message.reply_text(message, parse_mode="Markdown")
