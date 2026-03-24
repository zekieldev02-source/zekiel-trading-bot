"""ConversationHandler for /setstoploss command."""

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.bot.messages.config_messages import ASK_STOP_LOSS_MESSAGE, STOP_LOSS_CONFIRM_MESSAGE
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE, CANCEL_MESSAGE
from app.core.enums.conversation_state import ConversationState
from app.services.telegram import config_service
from app.services.validators.input_validator import validate_stop_loss


async def setstoploss_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(ASK_STOP_LOSS_MESSAGE, parse_mode="Markdown")
    return ConversationState.ASK_VALUE


async def setstoploss_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    raw = update.message.text
    telegram_id = update.effective_user.id

    is_valid, multiplier, error = validate_stop_loss(raw)
    if not is_valid:
        await update.message.reply_text(f"⚠️ {error}\n\nRéessaie ou tape /cancel.")
        return ConversationState.ASK_VALUE

    updated = await config_service.update_stop_loss(telegram_id, multiplier)
    if updated is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return ConversationHandler.END

    percent = f"{multiplier * 100:.0f}"
    message = STOP_LOSS_CONFIRM_MESSAGE.format(percent=percent)
    await update.message.reply_text(message, parse_mode="Markdown")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(CANCEL_MESSAGE)
    return ConversationHandler.END


setstoploss_handler = ConversationHandler(
    entry_points=[CommandHandler("setstoploss", setstoploss_start)],
    states={
        ConversationState.ASK_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, setstoploss_receive),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
