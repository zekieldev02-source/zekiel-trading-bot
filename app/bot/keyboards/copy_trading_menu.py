"""Inline keyboard for the Copy Trading menu."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.callbacks.menu_callbacks import MAIN


def build_copy_trading_menu() -> InlineKeyboardMarkup:
    """Config buttons redirect to commands via an instruction message,
    because ConversationHandlers cannot be triggered from an inline callback.
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✏️ Wallet", callback_data="menu:ct:wallet"),
            InlineKeyboardButton("💰 Montant", callback_data="menu:ct:amount"),
        ],
        [
            InlineKeyboardButton("📊 Take-profit", callback_data="menu:ct:tp"),
            InlineKeyboardButton("📉 Market Cap", callback_data="menu:ct:mc"),
        ],
        [
            InlineKeyboardButton("⬅️ Retour", callback_data=MAIN),
        ],
    ])
