"""Reusable confirmation keyboard for critical actions."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.callbacks.menu_callbacks import CANCEL


def build_confirm_keyboard(action_execute: str) -> InlineKeyboardMarkup:
    """Returns a [✅ Confirm] [❌ Cancel] keyboard.

    Args:
        action_execute: callback_data to trigger if the user confirms.
    """
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Confirmer", callback_data=action_execute),
            InlineKeyboardButton("❌ Annuler", callback_data=CANCEL),
        ]
    ])
