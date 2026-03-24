"""Inline keyboard for the settings menu."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.callbacks.menu_callbacks import MAIN


def build_settings_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✏️ Wallet", callback_data="menu:settings:wallet"),
            InlineKeyboardButton("🗑 Reset wallet", callback_data="menu:settings:reset:wallet"),
        ],
        [
            InlineKeyboardButton("💰 Amount", callback_data="menu:settings:amount"),
            InlineKeyboardButton("🗑 Reset amount", callback_data="menu:settings:reset:amount"),
        ],
        [
            InlineKeyboardButton("📈 Take-profit", callback_data="menu:settings:tp"),
            InlineKeyboardButton("🗑 Reset TP", callback_data="menu:settings:reset:tp"),
        ],
        [
            InlineKeyboardButton("🛑 Stop-loss", callback_data="menu:settings:sl"),
            InlineKeyboardButton("🗑 Reset SL", callback_data="menu:settings:reset:sl"),
        ],
        [
            InlineKeyboardButton("📉 Entry MC", callback_data="menu:settings:entrymc"),
            InlineKeyboardButton("🗑 Reset entry MC", callback_data="menu:settings:reset:entrymc"),
        ],
        [
            InlineKeyboardButton("📈 Exit MC", callback_data="menu:settings:exitmc"),
            InlineKeyboardButton("🗑 Reset exit MC", callback_data="menu:settings:reset:exitmc"),
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data=MAIN),
        ],
    ])
