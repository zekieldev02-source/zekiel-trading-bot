from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackQueryHandler, ContextTypes

from app.bot.keyboards.position_actions import build_positions_keyboard
from app.bot.messages.position_messages import NO_POSITIONS_MESSAGE, get_positions_message
from app.services.telegram import position_service, trade_service

_COPY_TRADE_PREFIX = "ct:"
_VIEW_POSITIONS = "vp"


async def handle_copy_trade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    telegram_id = query.from_user.id
    data = query.data or ""

    if not data.startswith(_COPY_TRADE_PREFIX):
        await query.answer("⚠️ Callback invalide.", show_alert=True)
        return

    signal_id = data[len(_COPY_TRADE_PREFIX):]
    if not signal_id:
        await query.answer("⚠️ Signal manquant.", show_alert=True)
        return

    result = await trade_service.execute_copy_trade(telegram_id, signal_id)

    if result == "already_open":
        await query.answer(
            "⚠️ Une position est déjà ouverte pour ce token.",
            show_alert=True,
        )
        return

    if result in ("signal_not_found", "expired"):
        await query.answer(
            "⚠️ Ce signal a expiré ou a déjà été utilisé.",
            show_alert=True,
        )
        return

    if result is None:
        await query.answer(
            "⚠️ Service indisponible. Réessaie dans un instant.",
            show_alert=True,
        )
        return

    await query.answer("✅ Copy trade exécuté !", show_alert=False)
    try:
        await query.edit_message_reply_markup(reply_markup=None)
    except TelegramError:
        pass


async def handle_view_positions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    telegram_id = query.from_user.id
    data = await position_service.get_positions_summary(telegram_id)

    if data is None:
        await query.message.reply_text("⚠️ Service unavailable. Please try again in a moment.")
        return

    summary = data.get("summary", {})
    has_positions = summary.get("open_count", 0) > 0 or summary.get("closed_count", 0) > 0

    if not has_positions:
        await query.message.reply_text(NO_POSITIONS_MESSAGE, parse_mode="Markdown")
        return

    open_positions = data.get("open_positions", [])
    keyboard = build_positions_keyboard(open_positions)
    await query.message.reply_text(get_positions_message(data), parse_mode="Markdown", reply_markup=keyboard)


copy_trade_callback_handler = CallbackQueryHandler(
    handle_copy_trade,
    pattern=r"^ct:.+",
)

view_positions_callback_handler = CallbackQueryHandler(
    handle_view_positions,
    pattern=r"^vp$",
)
