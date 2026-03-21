"""Inline keyboard for the Copy Trading menu."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.callbacks.menu_callbacks import MAIN


def build_copy_trading_menu() -> InlineKeyboardMarkup:
    """Config buttons redirect to commands via an instruction message,
    because ConversationHandlers cannot be triggered from an inline callback.
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✏️ Set Wallet", callback_data="menu:ct:wallet"),
            InlineKeyboardButton("💰 Set Amount", callback_data="menu:ct:amount"),
        ],
        [
            InlineKeyboardButton("📊 Set TP", callback_data="menu:ct:tp"),
            InlineKeyboardButton("📉 Market Cap", callback_data="menu:ct:mc"),
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data=MAIN),
        ],
    ])
