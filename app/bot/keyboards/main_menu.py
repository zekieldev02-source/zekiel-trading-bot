"""Inline keyboard for the main menu."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.callbacks.menu_callbacks import (
    COPY_TRADING,
    MAIN,
    POSITIONS,
    START_BOT_CONFIRM,
    STOP_BOT_CONFIRM,
)


def build_main_menu(bot_active: bool) -> InlineKeyboardMarkup:
    """Shows Start Bot or Stop Bot depending on the current bot state."""
    if bot_active:
        control_button = InlineKeyboardButton("🔴 Stop Bot", callback_data=STOP_BOT_CONFIRM)
    else:
        control_button = InlineKeyboardButton("🟢 Start Bot", callback_data=START_BOT_CONFIRM)

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📈 Positions", callback_data=POSITIONS),
            InlineKeyboardButton("🔁 Copy Trading", callback_data=COPY_TRADING),
        ],
        [control_button],
        [
            InlineKeyboardButton("🔄 Refresh", callback_data=MAIN),
        ],
    ])
