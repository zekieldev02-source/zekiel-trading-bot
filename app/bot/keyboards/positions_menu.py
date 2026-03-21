"""Clavier inline du menu Positions.

Combine les boutons de fermeture par position (existants)
avec les boutons de navigation du menu.
"""

import uuid

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.bot.callbacks.menu_callbacks import MAIN, POSITIONS
from app.bot.keyboards.position_actions import make_close_callback


def build_positions_menu(open_positions: list[dict]) -> InlineKeyboardMarkup:
    """Retourne le clavier inline du menu Positions.

    Affiche un bouton Close par position ouverte, puis Refresh et Retour.
    """
    buttons: list[list[InlineKeyboardButton]] = []

    for pos in open_positions:
        raw_id = pos.get("id")
        if not raw_id:
            continue
        symbol = pos.get("token_symbol") or f"{str(pos.get('token_address', '?'))[:8]}..."
        buttons.append([
            InlineKeyboardButton(
                text=f"🔴 Close {symbol}",
                callback_data=make_close_callback(uuid.UUID(str(raw_id))),
            )
        ])

    buttons.append([
        InlineKeyboardButton("🔄 Refresh", callback_data=POSITIONS),
        InlineKeyboardButton("⬅️ Retour", callback_data=MAIN),
    ])

    return InlineKeyboardMarkup(buttons)
