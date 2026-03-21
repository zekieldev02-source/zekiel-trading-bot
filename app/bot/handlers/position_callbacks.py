"""Handler for inline callbacks on paper positions."""

import logging

from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackQueryHandler, ContextTypes

from app.bot.keyboards.position_actions import build_positions_keyboard, parse_close_callback
from app.bot.messages.position_messages import (
    NO_POSITIONS_MESSAGE,
    get_close_confirmation_message,
    get_positions_message,
)
from app.services.telegram import position_service

_logger = logging.getLogger(__name__)

_ERROR_MESSAGES: dict[str, str] = {
    "already_closed": "⚠️ This position is already closed.",
    "not_found": "⚠️ Position not found.",
}


async def close_position_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles a click on the Close button of an open position.

    Flow: callback query → parse position_id → backend close
          → edit original message → send PnL confirmation.

    Error handling:
    - Invalid callback → immediate alert, no action.
    - Position already closed / not found → alert, message not edited.
    - Backend unavailable → alert, message not edited.
    - Success → message updated (refreshed positions) + PnL confirmation.
    """
    query = update.callback_query

    position_id = parse_close_callback(query.data or "")
    if position_id is None:
        await query.answer("⚠️ Invalid action.", show_alert=True)
        return

    telegram_id = update.effective_user.id
    result = await position_service.manual_close_position(telegram_id, position_id)

    if isinstance(result, str):
        await query.answer(
            _ERROR_MESSAGES.get(result, "⚠️ Unable to close this position."),
            show_alert=True,
        )
        return

    if result is None:
        await query.answer("⚠️ Backend unavailable.", show_alert=True)
        return

    await query.answer()

    data = await position_service.get_positions_summary(telegram_id)
    summary = data.get("summary", {}) if data else {}
    has_positions = summary.get("open_count", 0) > 0 or summary.get("closed_count", 0) > 0

    try:
        if data and has_positions:
            open_positions = data.get("open_positions", [])
            await query.edit_message_text(
                text=get_positions_message(data),
                parse_mode="Markdown",
                reply_markup=build_positions_keyboard(open_positions),
            )
        else:
            await query.edit_message_text(NO_POSITIONS_MESSAGE, parse_mode="Markdown")
    except TelegramError:
        _logger.debug("Positions message edit skipped (content unchanged).")

    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=get_close_confirmation_message(result),
        parse_mode="Markdown",
    )


close_position_callback_handler = CallbackQueryHandler(
    close_position_callback,
    pattern=r"^close_position:",
)
