"""ConversationHandler for /setamount command."""

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.bot.messages.error_messages import CANCEL_MESSAGE
from app.bot.messages.config_messages import (
    AMOUNT_CONFIRM_MESSAGE,
    ASK_AMOUNT_MESSAGE,
)
from app.core.enums.conversation_state import ConversationState
from app.services.user_config_service import UserConfigService


async def setamount_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point: ask the user for a trade amount."""
    UserConfigService.init_user_data(context.user_data)
    await update.message.reply_text(ASK_AMOUNT_MESSAGE, parse_mode="Markdown")
    return ConversationState.ASK_VALUE


async def setamount_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate and store the trade amount."""
    raw = update.message.text

    is_valid, amount, error = UserConfigService.validate_amount(raw)
    if not is_valid:
        await update.message.reply_text(f"⚠️ {error}\n\nRéessaie ou tape /cancel.")
        return ConversationState.ASK_VALUE

    UserConfigService.set_amount(context.user_data, amount)
    message = AMOUNT_CONFIRM_MESSAGE.format(amount=amount)
    await update.message.reply_text(message, parse_mode="Markdown")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(CANCEL_MESSAGE)
    return ConversationHandler.END


setamount_handler = ConversationHandler(
    entry_points=[CommandHandler("setamount", setamount_start)],
    states={
        ConversationState.ASK_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, setamount_receive),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
