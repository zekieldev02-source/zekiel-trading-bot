"""ConversationHandler for /settp command."""

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.bot.messages.config_messages import ASK_TP_MESSAGE, TP_CONFIRM_MESSAGE
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE, CANCEL_MESSAGE
from app.core.enums.conversation_state import ConversationState
from app.services.telegram import config_service
from app.services.user_config_service import UserConfigService


async def settp_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point: ask the user for a take-profit multiplier."""
    await update.message.reply_text(ASK_TP_MESSAGE, parse_mode="Markdown")
    return ConversationState.ASK_VALUE


async def settp_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate and persist the take-profit multiplier via the backend."""
    raw = update.message.text
    telegram_id = update.effective_user.id

    is_valid, multiplier, error = UserConfigService.validate_tp_multiplier(raw)
    if not is_valid:
        await update.message.reply_text(f"⚠️ {error}\n\nRéessaie ou tape /cancel.")
        return ConversationState.ASK_VALUE

    updated = await config_service.update_tp_multiplier(telegram_id, multiplier)
    if updated is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return ConversationHandler.END

    message = TP_CONFIRM_MESSAGE.format(multiplier=multiplier)
    await update.message.reply_text(message, parse_mode="Markdown")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(CANCEL_MESSAGE)
    return ConversationHandler.END


settp_handler = ConversationHandler(
    entry_points=[CommandHandler("settp", settp_start)],
    states={
        ConversationState.ASK_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, settp_receive),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
