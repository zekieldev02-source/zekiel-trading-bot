"""ConversationHandler for /setwallet command."""

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.bot.messages.config_messages import (
    ASK_WALLET_MESSAGE,
    WALLET_CONFIRM_MESSAGE,
    WALLET_UPDATED_MESSAGE,
)
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE, CANCEL_MESSAGE
from app.core.enums.conversation_state import ConversationState
from app.services.telegram import config_service
from app.services.user_config_service import UserConfigService


async def setwallet_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point: ask the user for a wallet address."""
    await update.message.reply_text(ASK_WALLET_MESSAGE, parse_mode="Markdown")
    return ConversationState.ASK_VALUE


async def setwallet_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate and persist the wallet address via the backend."""
    address = update.message.text.strip()
    telegram_id = update.effective_user.id

    is_valid, error = UserConfigService.validate_wallet(address)
    if not is_valid:
        await update.message.reply_text(f"⚠️ {error}\n\nRéessaie ou tape /cancel.")
        return ConversationState.ASK_VALUE

    # Récupère l'ancien wallet pour adapter le message de confirmation
    current_config = await config_service.get_config(telegram_id)
    old_wallet = current_config.wallet_address if current_config else None

    updated = await config_service.update_wallet(telegram_id, address)
    if updated is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return ConversationHandler.END

    if old_wallet and old_wallet != address:
        message = WALLET_UPDATED_MESSAGE.format(address=address)
    else:
        message = WALLET_CONFIRM_MESSAGE.format(address=address)

    await update.message.reply_text(message, parse_mode="Markdown")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(CANCEL_MESSAGE)
    return ConversationHandler.END


setwallet_handler = ConversationHandler(
    entry_points=[CommandHandler("setwallet", setwallet_start)],
    states={
        ConversationState.ASK_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, setwallet_receive),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
