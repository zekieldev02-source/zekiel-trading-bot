"""Navigation handler for inline menus.

Routes menu:* callbacks to the corresponding display functions.
No business logic here — only routing and rendering.
"""

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CallbackQueryHandler, ContextTypes

from app.bot.callbacks.menu_callbacks import (
    COPY_TRADING,
    HELP,
    MAIN,
    MODE_MANUAL,
    MODE_MENU,
    MODE_PAPER,
    POSITIONS,
    SETTINGS,
)
from app.bot.keyboards.copy_trading_menu import build_copy_trading_menu
from app.bot.keyboards.main_menu import build_main_menu
from app.bot.keyboards.mode_menu import build_mode_menu
from app.bot.keyboards.position_actions import build_positions_keyboard
from app.bot.keyboards.settings_menu import build_settings_menu
from app.bot.messages.bot_messages import HELP_MESSAGE, get_settings_message
from app.bot.messages.menu_messages import (
    get_config_hint,
    get_copy_trading_menu_message,
    get_main_menu_message,
    get_mode_menu_message,
)
from app.bot.messages.position_messages import NO_POSITIONS_MESSAGE, get_positions_message
from app.core.enums.trading_mode import TradingMode
from app.services.telegram import config_service, position_service, status_service

_BACKEND_ERROR = "⚠️ Service indisponible. Réessaie dans un instant."


async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Single entry point for all menu:* callbacks. Routes by callback_data."""
    query = update.callback_query
    await query.answer()
    try:
        await _dispatch(query, update, context)
    except BadRequest as e:
        if "Message is not modified" not in str(e):
            raise


async def _dispatch(query, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    data = query.data or ""
    telegram_id = query.from_user.id

    if data == MAIN:
        await _show_main_menu(query, telegram_id)
    elif data == HELP:
        await _show_help(query, telegram_id)
    elif data == COPY_TRADING:
        await _show_copy_trading_menu(query, telegram_id)
    elif data == POSITIONS:
        await _show_positions_menu(query, telegram_id)
    elif data == SETTINGS:
        await _show_settings_menu(query, telegram_id)
    elif data == MODE_MENU:
        await _show_mode_menu(query, telegram_id)
    elif data in (MODE_PAPER, MODE_MANUAL):
        await _execute_mode_change(query, telegram_id, data)
    elif data.startswith("menu:settings:reset:"):
        await _execute_settings_reset(query, telegram_id, data)
    elif data.startswith("menu:settings:"):
        await _show_settings_hint(query, telegram_id, data)
    elif data.startswith("menu:ct:"):
        await _show_config_hint(query, telegram_id, data)


async def _show_help(query, telegram_id: int) -> None:
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("⬅️ Back", callback_data=MAIN),
    ]])
    await query.edit_message_text(
        text=HELP_MESSAGE,
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


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
        await query.message.reply_text(_BACKEND_ERROR)
        return

    summary = data.get("summary", {})
    has_positions = summary.get("open_count", 0) > 0 or summary.get("closed_count", 0) > 0

    if not has_positions:
        await query.message.reply_text(NO_POSITIONS_MESSAGE, parse_mode="Markdown")
        return

    open_positions = data.get("open_positions", [])
    keyboard = build_positions_keyboard(open_positions)
    await query.message.reply_text(get_positions_message(data), parse_mode="Markdown", reply_markup=keyboard)


async def _show_settings_menu(query, telegram_id: int) -> None:
    config = await status_service.get_status(telegram_id)
    if config is None:
        await query.edit_message_text(_BACKEND_ERROR)
        return

    await query.edit_message_text(
        text=get_settings_message(config),
        parse_mode="Markdown",
        reply_markup=build_settings_menu(),
    )


_RESET_ACTIONS = {
    "menu:settings:reset:wallet": config_service.reset_wallet,
    "menu:settings:reset:amount": config_service.reset_amount,
    "menu:settings:reset:tp": config_service.reset_tp,
    "menu:settings:reset:sl": config_service.reset_stop_loss,
    "menu:settings:reset:entrymc": config_service.reset_entry_mc,
    "menu:settings:reset:exitmc": config_service.reset_exit_mc,
}

_RESET_LABELS = {
    "menu:settings:reset:wallet": "Wallet",
    "menu:settings:reset:amount": "Montant",
    "menu:settings:reset:tp": "Take-profit",
    "menu:settings:reset:sl": "Stop-loss",
    "menu:settings:reset:entrymc": "MC d'entrée",
    "menu:settings:reset:exitmc": "MC de sortie",
}


async def _execute_settings_reset(query, telegram_id: int, callback_data: str) -> None:
    action = _RESET_ACTIONS.get(callback_data)
    label = _RESET_LABELS.get(callback_data, "paramètre")

    if action is None:
        await query.answer("Action inconnue.")
        return

    result = await action(telegram_id)

    if result == "already_empty":
        await query.answer(f"{label} déjà vide.")
    elif result in ("success", "success_was_active"):
        await query.answer(f"✅ {label} supprimé.")
    else:
        await query.answer("⚠️ Erreur, réessaie.")
        return

    config = await status_service.get_status(telegram_id)
    if config is None:
        await query.edit_message_text(_BACKEND_ERROR)
        return

    await query.edit_message_text(
        text=get_settings_message(config),
        parse_mode="Markdown",
        reply_markup=build_settings_menu(),
    )


async def _show_settings_hint(query, telegram_id: int, callback_data: str) -> None:
    config = await status_service.get_status(telegram_id)
    if config is None:
        await query.edit_message_text(_BACKEND_ERROR)
        return

    hint = get_config_hint(callback_data)

    await query.edit_message_text(
        text=f"{get_settings_message(config)}\n\n{hint}",
        parse_mode="Markdown",
        reply_markup=build_settings_menu(),
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


async def _show_mode_menu(query, telegram_id: int) -> None:
    config = await status_service.get_status(telegram_id)
    if config is None:
        await query.edit_message_text(_BACKEND_ERROR)
        return

    await query.edit_message_text(
        text=get_mode_menu_message(config),
        parse_mode="Markdown",
        reply_markup=build_mode_menu(config.mode),
    )


_MODE_MAP = {
    MODE_PAPER: TradingMode.PAPER,
    MODE_MANUAL: TradingMode.MANUAL,
}

_MODE_SUCCESS_TEXTS = {
    TradingMode.PAPER: "📝 Mode *Paper* activé. Trades simulés — aucun SOL dépensé.",
    TradingMode.MANUAL: "🖐 Mode *Manual* activé. Tu recevras des alertes pour trader toi-même.",
}


async def _execute_mode_change(query, telegram_id: int, callback_data: str) -> None:
    new_mode = _MODE_MAP[callback_data]

    config = await status_service.get_status(telegram_id)
    if config is None:
        await query.edit_message_text(_BACKEND_ERROR)
        return

    if config.mode == new_mode:
        await query.answer(f"Tu es déjà en mode {new_mode.display}.")
        await query.edit_message_text(
            text=get_mode_menu_message(config),
            parse_mode="Markdown",
            reply_markup=build_mode_menu(config.mode),
        )
        return

    updated = await config_service.update_mode(telegram_id, new_mode)
    if updated is None:
        await query.answer("⚠️ Erreur, réessaie.")
        return

    await query.answer(f"✅ Mode {new_mode.display} activé.")
    await query.edit_message_text(
        text=f"{_MODE_SUCCESS_TEXTS[new_mode]}\n\n{get_mode_menu_message(updated)}",
        parse_mode="Markdown",
        reply_markup=build_mode_menu(updated.mode),
    )


menu_handler = CallbackQueryHandler(handle_menu, pattern=r"^menu:")
