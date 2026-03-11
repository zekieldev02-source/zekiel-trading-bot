"""ConversationHandler for /setwallet command."""

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
    ASK_WALLET_MESSAGE,
    WALLET_CONFIRM_MESSAGE,
    WALLET_UPDATED_MESSAGE,
)
from app.core.enums.conversation_state import ConversationState
from app.services.user_config_service import UserConfigService


async def setwallet_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point: ask the user for a wallet address."""
    UserConfigService.init_user_data(context.user_data)
    await update.message.reply_text(ASK_WALLET_MESSAGE, parse_mode="Markdown")
    return ConversationState.ASK_VALUE


async def setwallet_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate and store the wallet address."""
    address = update.message.text.strip()

    is_valid, error = UserConfigService.validate_wallet(address)
    if not is_valid:
        await update.message.reply_text(f"⚠️ {error}\n\nRéessaie ou tape /cancel.")
        return ConversationState.ASK_VALUE

    old_wallet = context.user_data.get("wallet_address")
    UserConfigService.set_wallet(context.user_data, address)

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
