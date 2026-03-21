"""Handlers for reset commands.

/resetwallet  — Remove the tracked wallet
/resetamount  — Remove the trade amount
/resettp      — Remove the take-profit multiplier
/resetentrymc — Remove the max entry market cap
/resetexitmc  — Remove the target exit market cap
/resetall     — Reset all configuration fields
"""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE
from app.bot.messages.reset_messages import (
    RESET_ALL_MESSAGE,
    RESET_AMOUNT_MESSAGE,
    RESET_ENTRY_MC_MESSAGE,
    RESET_EXIT_MC_MESSAGE,
    RESET_NOTHING_MESSAGE,
    RESET_TP_MESSAGE,
    RESET_WALLET_BOT_STOPPED_MESSAGE,
    RESET_WALLET_MESSAGE,
)
from app.services.telegram import config_service


async def reset_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the tracked wallet. Also stops the bot if active."""
    telegram_id = update.effective_user.id
    result = await config_service.reset_wallet(telegram_id)

    if result == "already_empty":
        await update.message.reply_text(RESET_NOTHING_MESSAGE.format(param="wallet"))
    elif result == "success_was_active":
        await update.message.reply_text(RESET_WALLET_BOT_STOPPED_MESSAGE, parse_mode="Markdown")
    elif result == "success":
        await update.message.reply_text(RESET_WALLET_MESSAGE, parse_mode="Markdown")
    else:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)


async def reset_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the trade amount. Also stops the bot if active."""
    telegram_id = update.effective_user.id
    result = await config_service.reset_amount(telegram_id)

    if result == "already_empty":
        await update.message.reply_text(RESET_NOTHING_MESSAGE.format(param="trade amount"))
    elif result == "success":
        await update.message.reply_text(RESET_AMOUNT_MESSAGE, parse_mode="Markdown")
    else:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)


async def reset_tp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the take-profit multiplier."""
    telegram_id = update.effective_user.id
    result = await config_service.reset_tp(telegram_id)

    if result == "already_empty":
        await update.message.reply_text(RESET_NOTHING_MESSAGE.format(param="take-profit"))
    elif result == "success":
        await update.message.reply_text(RESET_TP_MESSAGE, parse_mode="Markdown")
    else:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)


async def reset_entry_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the entry market cap threshold."""
    telegram_id = update.effective_user.id
    result = await config_service.reset_entry_mc(telegram_id)

    if result == "already_empty":
        await update.message.reply_text(RESET_NOTHING_MESSAGE.format(param="entry MC"))
    elif result == "success":
        await update.message.reply_text(RESET_ENTRY_MC_MESSAGE, parse_mode="Markdown")
    else:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)


async def reset_exit_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the exit market cap threshold."""
    telegram_id = update.effective_user.id
    result = await config_service.reset_exit_mc(telegram_id)

    if result == "already_empty":
        await update.message.reply_text(RESET_NOTHING_MESSAGE.format(param="exit MC"))
    elif result == "success":
        await update.message.reply_text(RESET_EXIT_MC_MESSAGE, parse_mode="Markdown")
    else:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)


async def reset_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reset all configuration fields to defaults. Positions are preserved."""
    telegram_id = update.effective_user.id
    result = await config_service.reset_all_fields(telegram_id)

    if result == "success":
        await update.message.reply_text(RESET_ALL_MESSAGE, parse_mode="Markdown")
    else:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
