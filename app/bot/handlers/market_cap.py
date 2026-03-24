"""ConversationHandlers for /setentrymc and /setexitmc commands."""

from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.bot.messages.config_messages import (
    ASK_ENTRY_MC_MESSAGE,
    ASK_EXIT_MC_MESSAGE,
    ENTRY_MC_CONFIRM_MESSAGE,
    EXIT_MC_CONFIRM_MESSAGE,
)
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE, CANCEL_MESSAGE
from app.core.enums.conversation_state import ConversationState
from app.services.telegram import config_service
from app.services.validators.input_validator import validate_market_cap


async def setentrymc_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point: ask for the maximum entry market cap."""
    await update.message.reply_text(ASK_ENTRY_MC_MESSAGE, parse_mode="Markdown")
    return ConversationState.ASK_VALUE


async def setentrymc_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate and persist the entry market cap via the backend."""
    raw = update.message.text
    telegram_id = update.effective_user.id

    is_valid, value, error = validate_market_cap(raw, is_entry=True)
    if not is_valid:
        await update.message.reply_text(f"⚠️ {error}\n\nTry again or type /cancel.")
        return ConversationState.ASK_VALUE

    updated = await config_service.update_entry_market_cap(telegram_id, value)
    if updated is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return ConversationHandler.END

    formatted = _format_mc(value)
    message = ENTRY_MC_CONFIRM_MESSAGE.format(value=formatted)
    await update.message.reply_text(message, parse_mode="Markdown")
    return ConversationHandler.END


async def setexitmc_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point: ask for the target exit market cap."""
    await update.message.reply_text(ASK_EXIT_MC_MESSAGE, parse_mode="Markdown")
    return ConversationState.ASK_VALUE


async def setexitmc_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate and persist the exit market cap via the backend."""
    raw = update.message.text
    telegram_id = update.effective_user.id

    is_valid, value, error = validate_market_cap(raw, is_entry=False)
    if not is_valid:
        await update.message.reply_text(f"⚠️ {error}\n\nTry again or type /cancel.")
        return ConversationState.ASK_VALUE

    updated = await config_service.update_exit_market_cap(telegram_id, value)
    if updated is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return ConversationHandler.END

    formatted = _format_mc(value)
    message = EXIT_MC_CONFIRM_MESSAGE.format(value=formatted)
    await update.message.reply_text(message, parse_mode="Markdown")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text(CANCEL_MESSAGE)
    return ConversationHandler.END


def _format_mc(value: float) -> str:
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.0f}K"
    return f"{value:,.0f}"


setentrymc_handler = ConversationHandler(
    entry_points=[CommandHandler("setentrymc", setentrymc_start)],
    states={
        ConversationState.ASK_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, setentrymc_receive),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

setexitmc_handler = ConversationHandler(
    entry_points=[CommandHandler("setexitmc", setexitmc_start)],
    states={
        ConversationState.ASK_VALUE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, setexitmc_receive),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
