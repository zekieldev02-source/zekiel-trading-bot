"""Handler for /start command."""

from telegram import Update
from telegram.ext import ContextTypes

from app.bot.keyboards.main_menu import build_main_menu
from app.bot.messages.error_messages import BACKEND_UNAVAILABLE_MESSAGE
from app.bot.messages.menu_messages import get_main_menu_message
from app.services.telegram import start_service, status_service


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome the user, register them if needed, and display the main menu."""
    user = update.effective_user
    success = await start_service.register_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    if not success:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return

    config = await status_service.get_status(user.id)
    if config is None:
        await update.message.reply_text(BACKEND_UNAVAILABLE_MESSAGE)
        return

    await update.message.reply_text(
        text=get_main_menu_message(config),
        parse_mode="Markdown",
        reply_markup=build_main_menu(config.bot_active),
    )
