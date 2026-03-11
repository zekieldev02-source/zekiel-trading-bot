"""Handlers for reset commands.

/resetwallet  — Supprimer le wallet suivi
/resetamount  — Supprimer le montant d'entrée
/resettp      — Supprimer le take-profit
/resetentrymc — Supprimer le MC max d'entrée
/resetexitmc  — Supprimer le MC cible de sortie
/resetall     — Réinitialiser toute la configuration
"""

from telegram import Update
from telegram.ext import ContextTypes

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
from app.core.constants import UserDataKeys
from app.services.user_config_service import UserConfigService


async def reset_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the tracked wallet. Also stops the bot if active."""
    UserConfigService.init_user_data(context.user_data)

    if not context.user_data.get(UserDataKeys.WALLET_ADDRESS):
        await update.message.reply_text(RESET_NOTHING_MESSAGE.format(param="wallet"))
        return

    was_active = context.user_data.get(UserDataKeys.BOT_ACTIVE, False)
    UserConfigService.reset_wallet(context.user_data)

    if was_active:
        await update.message.reply_text(RESET_WALLET_BOT_STOPPED_MESSAGE, parse_mode="Markdown")
    else:
        await update.message.reply_text(RESET_WALLET_MESSAGE, parse_mode="Markdown")


async def reset_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the trade amount. Also stops the bot if active."""
    UserConfigService.init_user_data(context.user_data)

    if not context.user_data.get(UserDataKeys.TRADE_AMOUNT):
        await update.message.reply_text(RESET_NOTHING_MESSAGE.format(param="montant"))
        return

    UserConfigService.reset_amount(context.user_data)
    await update.message.reply_text(RESET_AMOUNT_MESSAGE, parse_mode="Markdown")


async def reset_tp(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the take-profit multiplier."""
    UserConfigService.init_user_data(context.user_data)

    if not context.user_data.get(UserDataKeys.TP_MULTIPLIER):
        await update.message.reply_text(RESET_NOTHING_MESSAGE.format(param="take-profit"))
        return

    UserConfigService.reset_take_profit(context.user_data)
    await update.message.reply_text(RESET_TP_MESSAGE, parse_mode="Markdown")


async def reset_entry_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the entry market cap threshold."""
    UserConfigService.init_user_data(context.user_data)

    if not context.user_data.get(UserDataKeys.ENTRY_MARKET_CAP):
        await update.message.reply_text(RESET_NOTHING_MESSAGE.format(param="MC d'entrée"))
        return

    UserConfigService.reset_entry_market_cap(context.user_data)
    await update.message.reply_text(RESET_ENTRY_MC_MESSAGE, parse_mode="Markdown")


async def reset_exit_mc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the exit market cap threshold."""
    UserConfigService.init_user_data(context.user_data)

    if not context.user_data.get(UserDataKeys.EXIT_MARKET_CAP):
        await update.message.reply_text(RESET_NOTHING_MESSAGE.format(param="MC de sortie"))
        return

    UserConfigService.reset_exit_market_cap(context.user_data)
    await update.message.reply_text(RESET_EXIT_MC_MESSAGE, parse_mode="Markdown")


async def reset_all(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reset all configuration to defaults."""
    UserConfigService.reset_all(context.user_data)
    await update.message.reply_text(RESET_ALL_MESSAGE, parse_mode="Markdown")
