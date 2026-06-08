"""Inline keyboard for trading mode selection."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.callbacks.menu_callbacks import (
    MODE_AUTO_CONFIRM,
    MODE_MANUAL,
    MODE_PAPER,
    SETTINGS,
)
from app.core.enums.trading_mode import TradingMode


def build_mode_menu(current_mode: TradingMode) -> InlineKeyboardMarkup:
    """Shows 3 mode buttons. The active mode gets a ✅ prefix."""

    def _label(mode: TradingMode, emoji: str, name: str) -> str:
        return f"✅ {emoji} {name}" if mode == current_mode else f"{emoji} {name}"

    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                _label(TradingMode.PAPER, "📝", "Paper"),
                callback_data=MODE_PAPER,
            ),
            InlineKeyboardButton(
                _label(TradingMode.AUTO, "🤖", "Auto"),
                callback_data=MODE_AUTO_CONFIRM,
            ),
            InlineKeyboardButton(
                _label(TradingMode.MANUAL, "🖐", "Manual"),
                callback_data=MODE_MANUAL,
            ),
        ],
        [
            InlineKeyboardButton("⬅️ Back", callback_data=SETTINGS),
        ],
    ])
