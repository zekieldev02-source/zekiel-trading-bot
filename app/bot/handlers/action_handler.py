"""Handler for critical actions that require confirmation.

Flow: button → confirmation → execution → return to main menu.
Calls business services directly — not Telegram commands.
"""

from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from app.bot.callbacks.menu_callbacks import (
    CANCEL,
    EXPORT_WALLET_CONFIRM,
    EXPORT_WALLET_EXEC,
    MAIN,
    MODE_AUTO_CONFIRM,
    MODE_AUTO_EXEC,
    MODE_MENU,
    RESET_CONFIRM,
    RESET_EXEC,
    SETTINGS,
    START_BOT_CONFIRM,
    START_BOT_EXEC,
    STOP_BOT_CONFIRM,
    STOP_BOT_EXEC,
)
from app.bot.keyboards.confirm_keyboard import build_confirm_keyboard
from app.bot.keyboards.main_menu import build_main_menu
from app.bot.keyboards.mode_menu import build_mode_menu
from app.bot.messages.menu_messages import get_main_menu_message, get_mode_menu_message
from app.core.enums.trading_mode import TradingMode
from app.client.backend import config_client
from app.services.telegram import config_service, status_service

_CONFIRM_TEXTS: dict[str, str] = {
    START_BOT_CONFIRM: "⚠️ *Enable copy trading?*\n\nThe bot will start monitoring the configured wallet.",
    STOP_BOT_CONFIRM: "⚠️ *Disable copy trading?*\n\nThe bot will stop monitoring the wallet.",
    RESET_CONFIRM: "⚠️ *Reset all configuration?*\n\nThis action is irreversible.",
    MODE_AUTO_CONFIRM: (
        "⚠️ *Activer le mode Auto ?*\n\n"
        "Le bot exécutera de *vrais swaps* avec tes SOL dès qu'un signal arrive.\n\n"
        "Assure-toi que ton trading wallet est financé.\n"
        "Le bot sera mis en pause — utilise /startbot pour relancer."
    ),
    EXPORT_WALLET_CONFIRM: (
        "🔑 *Export private key*\n\n"
        "⚠️ *WARNING — Read carefully before confirming:*\n\n"
        "• Your private key gives *full access* to your trading wallet\n"
        "• Anyone who sees it can steal all your funds\n"
        "• The key will appear in this chat — *delete the message immediately* after copying\n"
        "• The message will auto-delete after *60 seconds*\n\n"
        "Only use this to import into Phantom/Solflare.\n\n"
        "Do you want to proceed?"
    ),
}

_START_BOT_RESULTS: dict[str, str] = {
    "success": "🟢 *Copy trading enabled!*\n\nThe bot is now monitoring the configured wallet.",
    "already_active": "ℹ️ Copy trading is already active.",
    "missing_wallet": "❌ No smart money wallet configured.\nUse /setwallet to set the wallet you want to copy _(not your own)_.",
    "missing_amount": "❌ Please set an amount first with /setamount",
    "backend_error": "⚠️ Service unavailable. Please try again in a moment.",
}

_STOP_BOT_RESULTS: dict[str, str] = {
    "success": "🔴 *Copy trading disabled.*\n\nUse Start bot to re-enable.",
    "already_inactive": "ℹ️ Copy trading is already stopped.",
    "backend_error": "⚠️ Service unavailable. Please try again in a moment.",
}

_RESET_RESULTS: dict[str, str] = {
    "success": "✅ *Configuration reset.*",
    "backend_error": "⚠️ Service unavailable. Please try again in a moment.",
}


async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Single entry point for all act:* callbacks. Routes to confirmation or execution."""
    query = update.callback_query
    await query.answer()

    data = query.data or ""
    telegram_id = query.from_user.id

    if data in _CONFIRM_TEXTS:
        await _show_confirmation(query, data)
    elif data == EXPORT_WALLET_EXEC:
        await _execute_export_wallet(query, telegram_id)
    elif data == START_BOT_EXEC:
        await _execute_start_bot(query, telegram_id)
    elif data == STOP_BOT_EXEC:
        await _execute_stop_bot(query, telegram_id)
    elif data == RESET_EXEC:
        await _execute_reset(query, telegram_id)
    elif data == MODE_AUTO_EXEC:
        await _execute_mode_auto(query, telegram_id)
    elif data == CANCEL:
        await _back_to_main(query, telegram_id)


async def _show_confirmation(query, data: str) -> None:
    """Replaces the message with confirmation text and Confirm/Cancel buttons."""
    execute_callbacks = {
        START_BOT_CONFIRM: START_BOT_EXEC,
        STOP_BOT_CONFIRM: STOP_BOT_EXEC,
        RESET_CONFIRM: RESET_EXEC,
        MODE_AUTO_CONFIRM: MODE_AUTO_EXEC,
        EXPORT_WALLET_CONFIRM: EXPORT_WALLET_EXEC,
    }
    cancel_callbacks = {
        MODE_AUTO_CONFIRM: MODE_MENU,
        EXPORT_WALLET_CONFIRM: SETTINGS,
    }
    cancel_cb = cancel_callbacks.get(data, CANCEL)

    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Confirmer", callback_data=execute_callbacks[data]),
        InlineKeyboardButton("❌ Annuler", callback_data=cancel_cb),
    ]])

    await query.edit_message_text(
        text=_CONFIRM_TEXTS[data],
        parse_mode="Markdown",
        reply_markup=keyboard,
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


async def _execute_export_wallet(query, telegram_id: int) -> None:
    data = await config_client.export_trading_wallet(telegram_id)
    if not data:
        await query.edit_message_text(
            "⚠️ No trading wallet found. Use /generatewallet first.",
            parse_mode="Markdown",
        )
        return

    public_key = data.get("public_key", "")
    private_key_bytes = data.get("private_key_bytes", "")

    # Delete the confirmation message first
    await query.message.delete()

    # Send the key as a new private message — scheduled for auto-deletion after 60s
    sent = await query.message.chat.send_message(
        text=(
            "🔑 *Your trading wallet private key*\n\n"
            f"*Public key:* `{public_key}`\n\n"
            "*Private key (Phantom format):*\n"
            f"`{private_key_bytes}`\n\n"
            "⚠️ *Delete this message immediately after copying.*\n"
            "This message will self-destruct in *60 seconds*."
        ),
        parse_mode="Markdown",
    )

    # Schedule auto-deletion
    import asyncio
    async def _delete_later():
        await asyncio.sleep(60)
        try:
            await sent.delete()
        except Exception:
            pass

    asyncio.create_task(_delete_later())


async def _execute_mode_auto(query, telegram_id: int) -> None:
    updated = await config_service.update_mode(telegram_id, TradingMode.AUTO)
    if updated is None:
        await query.answer("⚠️ Erreur, réessaie.")
        return

    await query.edit_message_text(
        text=(
            "🤖 Mode *Auto* activé.\n\n"
            "⚠️ Le bot exécutera de vrais swaps automatiquement.\n"
            "Assure-toi que ton trading wallet est financé, puis utilise /startbot."
            f"\n\n{get_mode_menu_message(updated)}"
        ),
        parse_mode="Markdown",
        reply_markup=build_mode_menu(updated.mode),
    )


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
        await query.edit_message_text("⚠️ Service unavailable.")
        return

    await query.edit_message_text(
        text=get_main_menu_message(config),
        parse_mode="Markdown",
        reply_markup=build_main_menu(config.bot_active),
    )


action_handler = CallbackQueryHandler(handle_action, pattern=r"^act:")
