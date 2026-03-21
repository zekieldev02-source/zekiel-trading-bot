"""Inline keyboard for paper position actions."""

import uuid

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

_CLOSE_PREFIX = "close_position:"


def make_close_callback(position_id: uuid.UUID) -> str:
    """Generates the callback data for closing a position.

    Format: close_position:<uuid>
    Max length: 15 + 36 = 51 chars (Telegram limit: 64).
    """
    return f"{_CLOSE_PREFIX}{position_id}"


def parse_close_callback(data: str) -> uuid.UUID | None:
    """Parses callback data and returns the position_id. Returns None if format is invalid."""
    if not data or not data.startswith(_CLOSE_PREFIX):
        return None
    try:
        return uuid.UUID(data[len(_CLOSE_PREFIX):])
    except ValueError:
        return None


def build_positions_keyboard(open_positions: list[dict]) -> InlineKeyboardMarkup | None:
    """Builds the inline keyboard with one Close button per open position.

    Each button is on its own row for readability. Returns None if no open positions.
    """
    if not open_positions:
        return None

    buttons: list[list[InlineKeyboardButton]] = []
    for pos in open_positions:
        raw_id = pos.get("id")
        if not raw_id:
            continue
        symbol = pos.get("token_symbol") or f"{str(pos.get('token_address', '?'))[:8]}..."
        buttons.append([
            InlineKeyboardButton(
                text=f"🔴 Fermer {symbol}",
                callback_data=make_close_callback(uuid.UUID(str(raw_id))),
            )
        ])

    return InlineKeyboardMarkup(buttons) if buttons else None
