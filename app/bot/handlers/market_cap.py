"""ConversationHandlers for /setentrymc and /setexitmc commands."""

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
    ASK_ENTRY_MC_MESSAGE,
    ASK_EXIT_MC_MESSAGE,
    ENTRY_MC_CONFIRM_MESSAGE,
    EXIT_MC_CONFIRM_MESSAGE,
)
from app.core.enums.conversation_state import ConversationState
from app.services.user_config_service import UserConfigService


# ------------------------------------------------------------------ #
#  /setentrymc
# ------------------------------------------------------------------ #

async def setentrymc_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point: ask for the maximum entry market cap."""
    UserConfigService.init_user_data(context.user_data)
    await update.message.reply_text(ASK_ENTRY_MC_MESSAGE, parse_mode="Markdown")
    return ConversationState.ASK_VALUE


async def setentrymc_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate and store the entry market cap."""
    raw = update.message.text

    is_valid, value, error = UserConfigService.validate_market_cap(raw, is_entry=True)
    if not is_valid:
        await update.message.reply_text(f"⚠️ {error}\n\nRéessaie ou tape /cancel.")
        return ConversationState.ASK_VALUE

    UserConfigService.set_entry_market_cap(context.user_data, value)
    formatted = _format_mc(value)
    message = ENTRY_MC_CONFIRM_MESSAGE.format(value=formatted)
    await update.message.reply_text(message, parse_mode="Markdown")
    return ConversationHandler.END


# ------------------------------------------------------------------ #
#  /setexitmc
# ------------------------------------------------------------------ #

async def setexitmc_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Entry point: ask for the target exit market cap."""
    UserConfigService.init_user_data(context.user_data)
    await update.message.reply_text(ASK_EXIT_MC_MESSAGE, parse_mode="Markdown")
    return ConversationState.ASK_VALUE


async def setexitmc_receive(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Validate and store the exit market cap."""
    raw = update.message.text

    is_valid, value, error = UserConfigService.validate_market_cap(raw, is_entry=False)
    if not is_valid:
        await update.message.reply_text(f"⚠️ {error}\n\nRéessaie ou tape /cancel.")
        return ConversationState.ASK_VALUE

    UserConfigService.set_exit_market_cap(context.user_data, value)
    formatted = _format_mc(value)
    message = EXIT_MC_CONFIRM_MESSAGE.format(value=formatted)
    await update.message.reply_text(message, parse_mode="Markdown")
    return ConversationHandler.END


# ------------------------------------------------------------------ #
#  Shared
# ------------------------------------------------------------------ #

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


# ------------------------------------------------------------------ #
#  Exported handlers
# ------------------------------------------------------------------ #

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
