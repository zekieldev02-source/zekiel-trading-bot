"""Handler for critical actions that require confirmation.

Flow: button → confirmation → execution → return to main menu.
Calls business services directly — not Telegram commands.
"""

from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from app.bot.callbacks.menu_callbacks import (
    CANCEL,
    MAIN,
    RESET_CONFIRM,
    RESET_EXEC,
    START_BOT_CONFIRM,
    START_BOT_EXEC,
    STOP_BOT_CONFIRM,
    STOP_BOT_EXEC,
)
from app.bot.keyboards.confirm_keyboard import build_confirm_keyboard
from app.bot.keyboards.main_menu import build_main_menu
from app.bot.messages.menu_messages import get_main_menu_message
from app.services.telegram import config_service, status_service

_CONFIRM_TEXTS: dict[str, str] = {
    START_BOT_CONFIRM: "⚠️ *Enable copy trading?*\n\nThe bot will start monitoring the configured wallet.",
    STOP_BOT_CONFIRM: "⚠️ *Disable copy trading?*\n\nThe bot will stop monitoring the wallet.",
    RESET_CONFIRM: "⚠️ *Reset all configuration?*\n\nThis action is irreversible.",
}

_START_BOT_RESULTS: dict[str, str] = {
    "success": "🟢 *Copy trading enabled!*\n\nThe bot is now monitoring the configured wallet.",
    "already_active": "ℹ️ Copy trading is already active.",
    "missing_wallet": "❌ Set a wallet first with /setwallet",
    "missing_amount": "❌ Set a trade amount first with /setamount",
    "backend_error": "⚠️ Backend unavailable. Try again in a moment.",
}

_STOP_BOT_RESULTS: dict[str, str] = {
    "success": "🔴 *Copy trading disabled.*\n\nUse Start Bot to re-enable.",
    "already_inactive": "ℹ️ Copy trading is already stopped.",
    "backend_error": "⚠️ Backend unavailable. Try again in a moment.",
}

_RESET_RESULTS: dict[str, str] = {
    "success": "✅ *Configuration reset.*",
    "backend_error": "⚠️ Backend unavailable. Try again in a moment.",
}


async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Single entry point for all act:* callbacks. Routes to confirmation or execution."""
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    telegram_id = query.from_user.id

    if data in _CONFIRM_TEXTS:
        await _show_confirmation(query, data)
    elif data == START_BOT_EXEC:
        await _execute_start_bot(query, telegram_id)
    elif data == STOP_BOT_EXEC:
        await _execute_stop_bot(query, telegram_id)
    elif data == RESET_EXEC:
        await _execute_reset(query, telegram_id)
    elif data == CANCEL:
        await _back_to_main(query, telegram_id)


async def _show_confirmation(query, data: str) -> None:
    """Replaces the message with confirmation text and Confirm/Cancel buttons."""
    execute_callbacks = {
        START_BOT_CONFIRM: START_BOT_EXEC,
        STOP_BOT_CONFIRM: STOP_BOT_EXEC,
        RESET_CONFIRM: RESET_EXEC,
    }
    await query.edit_message_text(
        text=_CONFIRM_TEXTS[data],
        parse_mode="Markdown",
        reply_markup=build_confirm_keyboard(execute_callbacks[data]),
    )


async def _execute_start_bot(query, telegram_id: int) -> None:
    result = await config_service.activate_bot(telegram_id)
    text = _START_BOT_RESULTS.get(result, "⚠️ Unexpected error.")
    await _show_result_and_return(query, telegram_id, text)


async def _execute_stop_bot(query, telegram_id: int) -> None:
    result = await config_service.deactivate_bot(telegram_id)
    text = _STOP_BOT_RESULTS.get(result, "⚠️ Unexpected error.")
    await _show_result_and_return(query, telegram_id, text)


async def _execute_reset(query, telegram_id: int) -> None:
    result = await config_service.reset_all_fields(telegram_id)
    text = _RESET_RESULTS.get(result, "⚠️ Unexpected error.")
    await _show_result_and_return(query, telegram_id, text)


async def _show_result_and_return(query, telegram_id: int, result_text: str) -> None:
    """Shows the action result then returns to the main menu with a fresh config."""
    config = await status_service.get_status(telegram_id)
    if config is None:
        await query.edit_message_text(result_text, parse_mode="Markdown")
        return

    text = f"{result_text}\n\n{get_main_menu_message(config)}"
    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        reply_markup=build_main_menu(config.bot_active),
    )


async def _back_to_main(query, telegram_id: int) -> None:
    """Cancellation — returns to main menu without executing the action."""
    config = await status_service.get_status(telegram_id)
    if config is None:
        await query.edit_message_text("⚠️ Backend unavailable.")
        return

    await query.edit_message_text(
        text=get_main_menu_message(config),
        parse_mode="Markdown",
        reply_markup=build_main_menu(config.bot_active),
    )


action_handler = CallbackQueryHandler(handle_action, pattern=r"^act:")
