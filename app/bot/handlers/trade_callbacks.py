from telegram import Update
from telegram.error import TelegramError
from telegram.ext import CallbackQueryHandler, ContextTypes

from app.services.telegram import trade_service

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
    await query.answer(
        "Utilise /positions pour voir tes positions ouvertes.",
        show_alert=False,
    )


copy_trade_callback_handler = CallbackQueryHandler(
    handle_copy_trade,
    pattern=r"^ct:.+",
)

view_positions_callback_handler = CallbackQueryHandler(
    handle_view_positions,
    pattern=r"^vp$",
)
