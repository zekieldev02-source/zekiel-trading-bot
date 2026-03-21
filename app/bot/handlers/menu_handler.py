"""Navigation handler for inline menus.

Routes menu:* callbacks to the corresponding display functions.
No business logic here — only routing and rendering.
"""

from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from app.bot.callbacks.menu_callbacks import COPY_TRADING, MAIN, POSITIONS
from app.bot.keyboards.copy_trading_menu import build_copy_trading_menu
from app.bot.keyboards.main_menu import build_main_menu
from app.bot.keyboards.positions_menu import build_positions_menu
from app.bot.messages.menu_messages import (
    get_config_hint,
    get_copy_trading_menu_message,
    get_main_menu_message,
)
from app.bot.messages.position_messages import NO_POSITIONS_MESSAGE, get_positions_message
from app.services.telegram import position_service, status_service

_BACKEND_ERROR = "⚠️ Service indisponible. Réessaie dans un instant."


async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Single entry point for all menu:* callbacks. Routes by callback_data."""
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    telegram_id = query.from_user.id

    if data == MAIN:
        await _show_main_menu(query, telegram_id)
    elif data == COPY_TRADING:
        await _show_copy_trading_menu(query, telegram_id)
    elif data == POSITIONS:
        await _show_positions_menu(query, telegram_id)
    elif data.startswith("menu:ct:"):
        await _show_config_hint(query, telegram_id, data)


async def _show_main_menu(query, telegram_id: int) -> None:
    config = await status_service.get_status(telegram_id)
    if config is None:
        await query.edit_message_text(_BACKEND_ERROR)
        return

    await query.edit_message_text(
        text=get_main_menu_message(config),
        parse_mode="Markdown",
        reply_markup=build_main_menu(config.bot_active),
    )


async def _show_copy_trading_menu(query, telegram_id: int) -> None:
    config = await status_service.get_status(telegram_id)
    if config is None:
        await query.edit_message_text(_BACKEND_ERROR)
        return

    await query.edit_message_text(
        text=get_copy_trading_menu_message(config),
        parse_mode="Markdown",
        reply_markup=build_copy_trading_menu(),
    )


async def _show_positions_menu(query, telegram_id: int) -> None:
    data = await position_service.get_positions_summary(telegram_id)
    if data is None:
        await query.edit_message_text(_BACKEND_ERROR)
        return

    summary = data.get("summary", {})
    has_positions = summary.get("open_count", 0) > 0 or summary.get("closed_count", 0) > 0

    if not has_positions:
        await query.edit_message_text(
            text=NO_POSITIONS_MESSAGE,
            parse_mode="Markdown",
            reply_markup=build_positions_menu([]),
        )
        return

    open_positions = data.get("open_positions", [])

    await query.edit_message_text(
        text=get_positions_message(data),
        parse_mode="Markdown",
        reply_markup=build_positions_menu(open_positions),
    )


async def _show_config_hint(query, telegram_id: int, callback_data: str) -> None:
    """Shows an instruction message for config buttons.

    ConversationHandlers cannot be triggered from a callback, so the user is
    guided to the corresponding command instead.
    """
    config = await status_service.get_status(telegram_id)
    if config is None:
        await query.edit_message_text(_BACKEND_ERROR)
        return

    hint = get_config_hint(callback_data)

    await query.edit_message_text(
        text=f"{get_copy_trading_menu_message(config)}\n\n{hint}",
        parse_mode="Markdown",
        reply_markup=build_copy_trading_menu(),
    )


menu_handler = CallbackQueryHandler(handle_menu, pattern=r"^menu:")
