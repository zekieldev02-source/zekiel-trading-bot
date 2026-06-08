"""Handlers for trading wallet commands.

/generatewallet — generates (or shows existing) AUTO mode trading wallet.
/depositinfo    — shows the trading wallet address for funding.
/importwallet   — import the user's own Solana wallet by private key.
"""

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.bot.messages.config_messages import (
    ASK_IMPORT_WALLET_MESSAGE,
    DEPOSIT_INFO_MESSAGE,
    DEPOSIT_INFO_NO_WALLET_MESSAGE,
    IMPORT_WALLET_ERROR_MESSAGE,
    IMPORT_WALLET_SUCCESS_MESSAGE,
    WALLET_GENERATE_ERROR_MESSAGE,
    WALLET_GENERATE_SUCCESS_MESSAGE,
)
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE, CANCEL_MESSAGE
from app.client.backend import config_client
from app.core.enums.conversation_state import ConversationState
from app.services.telegram import config_service


async def generate_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/generatewallet — creates a dedicated Solana wallet for AUTO mode."""
    telegram_id = update.effective_user.id

    result = await config_service.generate_wallet(telegram_id)
    if result is None:
        await update.message.reply_text(WALLET_GENERATE_ERROR_MESSAGE)
        return

    public_key = result.get("public_key", "")
    await update.message.reply_text(
        WALLET_GENERATE_SUCCESS_MESSAGE.format(public_key=public_key),
        parse_mode="Markdown",
    )


async def import_wallet_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """/importwallet — ask the user for their private key."""
    await update.message.reply_text(ASK_IMPORT_WALLET_MESSAGE, parse_mode="Markdown")
    return ConversationState.ASK_PRIVATE_KEY


async def import_wallet_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Receive private key, delete the message immediately, import to backend."""
    telegram_id = update.effective_user.id
    private_key = update.message.text.strip()

    # Delete user's message immediately to avoid key exposure in chat history
    try:
        await update.message.delete()
    except Exception:
        pass

    try:
        result = await config_client.import_trading_wallet(telegram_id, private_key)
    except ValueError as exc:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=IMPORT_WALLET_ERROR_MESSAGE.format(detail=str(exc)),
            parse_mode="Markdown",
        )
        return ConversationState.ASK_PRIVATE_KEY

    if result is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=BACKEND_UNAVAILABLE_MESSAGE,
        )
        return ConversationHandler.END

    public_key = result.get("public_key", "")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=IMPORT_WALLET_SUCCESS_MESSAGE.format(public_key=public_key),
        parse_mode="Markdown",
    )
    return ConversationHandler.END


async def import_wallet_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(CANCEL_MESSAGE)
    return ConversationHandler.END


import_wallet_handler = ConversationHandler(
    entry_points=[CommandHandler("importwallet", import_wallet_start)],
    states={
        ConversationState.ASK_PRIVATE_KEY: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, import_wallet_receive),
        ],
    },
    fallbacks=[CommandHandler("cancel", import_wallet_cancel)],
)


async def deposit_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """/depositinfo — shows the trading wallet address."""
    telegram_id = update.effective_user.id

    config = await config_service.get_config(telegram_id)
    if config is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return

    if not config.trading_wallet_public_key:
        await update.message.reply_text(DEPOSIT_INFO_NO_WALLET_MESSAGE, parse_mode="Markdown")
        return

    await update.message.reply_text(
        DEPOSIT_INFO_MESSAGE.format(public_key=config.trading_wallet_public_key),
        parse_mode="Markdown",
    )
