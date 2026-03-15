"""ConversationHandler for /reset command (full reset with confirmation)."""

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE, CANCEL_MESSAGE
from app.bot.messages.reset_messages import (
    RESET_CANCELLED_MESSAGE,
    RESET_CONFIRM_ASK_MESSAGE,
    RESET_DONE_MESSAGE,
)
from app.core.enums.conversation_state import ConversationState
from app.services.telegram import reset_service


async def reset_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point: ask the user to confirm the full reset."""
    await update.message.reply_text(RESET_CONFIRM_ASK_MESSAGE, parse_mode="Markdown")
    return ConversationState.CONFIRM


async def reset_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the confirmation response and trigger full reset on the backend."""
    raw = update.message.text.strip().lower()

    if raw == "oui":
        telegram_id = update.effective_user.id
        success = await reset_service.full_reset(telegram_id)
        if not success:
            await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
            return ConversationHandler.END
        await update.message.reply_text(RESET_DONE_MESSAGE, parse_mode="Markdown")
        return ConversationHandler.END

    await update.message.reply_text(RESET_CANCELLED_MESSAGE)
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(CANCEL_MESSAGE)
    return ConversationHandler.END


full_reset_handler = ConversationHandler(
    entry_points=[CommandHandler("reset", reset_start)],
    states={
        ConversationState.CONFIRM: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, reset_confirm),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
