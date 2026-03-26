"""Centralized handler registration.

All command handlers and conversation handlers are registered here.
main.py only builds the Application and calls this function.
"""

from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from app.bot.handlers.amount import setamount_handler
from app.bot.handlers.control import start_bot, stop_bot
from app.bot.handlers.position_callbacks import close_position_callback_handler
from app.bot.handlers.action_handler import action_handler
from app.bot.handlers.menu_handler import menu_handler
from app.bot.handlers.trade_callbacks import (
    copy_trade_callback_handler,
    view_positions_callback_handler,
)
from app.bot.handlers.positions import positions
from app.bot.handlers.full_reset import full_reset_handler
from app.bot.handlers.help import help_command
from app.bot.handlers.market_cap import setentrymc_handler, setexitmc_handler
from app.bot.handlers.mode import mode
from app.bot.handlers.trading_wallet import generate_wallet, deposit_info
from app.bot.handlers.reset import (
    reset_all,
    reset_amount,
    reset_entry_mc,
    reset_exit_mc,
    reset_stop_loss,
    reset_tp,
    reset_wallet,
)
from app.bot.handlers.settings import settings
from app.bot.handlers.start import start
from app.bot.handlers.status import status
from app.bot.handlers.stop_loss import setstoploss_handler
from app.bot.handlers.take_profit import settp_handler
from app.bot.handlers.wallet import setwallet_handler


def register_all_handlers(app: Application) -> None:
    """Register all handlers on the Application instance."""

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(CommandHandler("positions", positions))

    app.add_handler(CommandHandler("startbot", start_bot))
    app.add_handler(CommandHandler("stopbot", stop_bot))

    app.add_handler(setwallet_handler)
    app.add_handler(setamount_handler)
    app.add_handler(settp_handler)
    app.add_handler(setstoploss_handler)
    app.add_handler(setentrymc_handler)
    app.add_handler(setexitmc_handler)
    app.add_handler(CommandHandler("mode", mode))
    app.add_handler(CommandHandler("generatewallet", generate_wallet))
    app.add_handler(CommandHandler("depositinfo", deposit_info))

    app.add_handler(action_handler)
    app.add_handler(menu_handler)
    app.add_handler(close_position_callback_handler)
    app.add_handler(copy_trade_callback_handler)
    app.add_handler(view_positions_callback_handler)

    app.add_handler(CommandHandler("resetwallet", reset_wallet))
    app.add_handler(CommandHandler("resetamount", reset_amount))
    app.add_handler(CommandHandler("resettp", reset_tp))
    app.add_handler(CommandHandler("resetstoploss", reset_stop_loss))
    app.add_handler(CommandHandler("resetentrymc", reset_entry_mc))
    app.add_handler(CommandHandler("resetexitmc", reset_exit_mc))
    app.add_handler(CommandHandler("resetall", reset_all))
    app.add_handler(full_reset_handler)
