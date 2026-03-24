"""Reset messages: individual resets (/resetwallet…) + full reset (/reset)."""

RESET_WALLET_MESSAGE = "🗑 *Wallet removed.*\nUse /setwallet to configure a new one."

RESET_WALLET_BOT_STOPPED_MESSAGE = (
    "🗑 *Wallet removed.*\n"
    "⚠️ Copy trading has been disabled (wallet required).\n"
    "\n"
    "Use /setwallet to configure a new one."
)

RESET_AMOUNT_MESSAGE = "🗑 *Amount removed.*\nUse /setamount to set a new one."

RESET_TP_MESSAGE = "🗑 *Take-profit removed.*\nUse /settp to set a new one."

RESET_STOP_LOSS_MESSAGE = "🗑 *Stop-loss removed.*\nUse /setstoploss to set a new one."

RESET_ENTRY_MC_MESSAGE = "🗑 *Entry MC removed.*\nUse /setentrymc to set a new one."

RESET_EXIT_MC_MESSAGE = "🗑 *Exit MC removed.*\nUse /setexitmc to set a new one."

RESET_ALL_MESSAGE = (
    "🗑 *Configuration reset.*\n"
    "\n"
    "All settings have been cleared.\n"
    "Use /setwallet and /setamount to start again."
)

RESET_NOTHING_MESSAGE = "ℹ️ {param} is not configured — nothing to remove."

RESET_CONFIRM_ASK_MESSAGE = (
    "⚠️ *Full reset*\n"
    "\n"
    "This action will:\n"
    "• Delete all your configuration\n"
    "• Delete all your paper positions\n"
    "• Reset all parameters to zero\n"
    "• Switch back to Paper Trading mode\n"
    "\n"
    "Type `yes` to confirm or /cancel to abort."
)

RESET_DONE_MESSAGE = (
    "🗑 *Full reset completed.*\n"
    "\n"
    "All your settings have been cleared.\n"
    "Use /setwallet and /setamount to start again."
)

RESET_CANCELLED_MESSAGE = "✅ Reset cancelled. Your configuration is intact."
