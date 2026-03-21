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
    START_BOT_CONFIRM: "⚠️ *Activer le copy trading ?*\n\nLe bot va commencer à surveiller le wallet configuré.",
    STOP_BOT_CONFIRM: "⚠️ *Désactiver le copy trading ?*\n\nLe bot arrêtera de surveiller le wallet.",
    RESET_CONFIRM: "⚠️ *Réinitialiser toute la configuration ?*\n\nCette action est irréversible.",
}

_START_BOT_RESULTS: dict[str, str] = {
    "success": "🟢 *Copy trading activé !*\n\nLe bot surveille maintenant le wallet configuré.",
    "already_active": "ℹ️ Le copy trading est déjà actif.",
    "missing_wallet": "❌ Configure d'abord un wallet avec /setwallet",
    "missing_amount": "❌ Configure d'abord un montant avec /setamount",
    "backend_error": "⚠️ Service indisponible. Réessaie dans un instant.",
}

_STOP_BOT_RESULTS: dict[str, str] = {
    "success": "🔴 *Copy trading désactivé.*\n\nUtilise Démarrer le bot pour réactiver.",
    "already_inactive": "ℹ️ Le copy trading est déjà arrêté.",
    "backend_error": "⚠️ Service indisponible. Réessaie dans un instant.",
}

_RESET_RESULTS: dict[str, str] = {
    "success": "✅ *Configuration réinitialisée.*",
    "backend_error": "⚠️ Service indisponible. Réessaie dans un instant.",
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
    text = _START_BOT_RESULTS.get(result, "⚠️ Erreur inattendue.")
    await _show_result_and_return(query, telegram_id, text)


async def _execute_stop_bot(query, telegram_id: int) -> None:
    result = await config_service.deactivate_bot(telegram_id)
    text = _STOP_BOT_RESULTS.get(result, "⚠️ Erreur inattendue.")
    await _show_result_and_return(query, telegram_id, text)


async def _execute_reset(query, telegram_id: int) -> None:
    result = await config_service.reset_all_fields(telegram_id)
    text = _RESET_RESULTS.get(result, "⚠️ Erreur inattendue.")
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
        await query.edit_message_text("⚠️ Service indisponible.")
        return

    await query.edit_message_text(
        text=get_main_menu_message(config),
        parse_mode="Markdown",
        reply_markup=build_main_menu(config.bot_active),
    )


action_handler = CallbackQueryHandler(handle_action, pattern=r"^act:")
