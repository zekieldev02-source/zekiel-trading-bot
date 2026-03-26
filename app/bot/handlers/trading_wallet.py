"""Handlers for trading wallet commands.

/generatewallet — generates (or shows existing) AUTO mode trading wallet.
/depositinfo    — shows the trading wallet address for funding.
"""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.messages.config_messages import (
    DEPOSIT_INFO_MESSAGE,
    DEPOSIT_INFO_NO_WALLET_MESSAGE,
    WALLET_GENERATE_ERROR_MESSAGE,
    WALLET_GENERATE_SUCCESS_MESSAGE,
)
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE
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
