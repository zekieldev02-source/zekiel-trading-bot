"""Reset messages: individual resets (/resetwallet…) + full reset (/reset)."""

RESET_WALLET_MESSAGE = "🗑 *Wallet removed.*\nUse /setwallet to configure a new one."

RESET_WALLET_BOT_STOPPED_MESSAGE = (
    "🗑 *Wallet removed.*\n"
    "⚠️ Copy trading has been disabled (wallet required).\n"
    "\n"
    "Use /setwallet to configure a new one."
)

RESET_AMOUNT_MESSAGE = "🗑 *Trade amount removed.*\nUse /setamount to set a new one."

RESET_TP_MESSAGE = "🗑 *Take-profit removed.*\nUse /settp to set a new one."

RESET_ENTRY_MC_MESSAGE = "🗑 *Max entry MC removed.*\nUse /setentrymc to set a new one."

RESET_EXIT_MC_MESSAGE = "🗑 *Target exit MC removed.*\nUse /setexitmc to set a new one."

RESET_ALL_MESSAGE = (
    "🗑 *Configuration reset.*\n"
    "\n"
    "All parameters have been cleared.\n"
    "Use /setwallet and /setamount to start over."
)

RESET_NOTHING_MESSAGE = "ℹ️ {param} is not configured — nothing to remove."

RESET_CONFIRM_ASK_MESSAGE = (
    "⚠️ *Full reset*\n"
    "\n"
    "This action will:\n"
    "• Delete all your configuration\n"
    "• Delete all your paper positions\n"
    "• Reset all parameters to defaults\n"
    "• Switch mode back to Paper Trading\n"
    "\n"
    "Type `yes` to confirm or /cancel to abort."
)

RESET_DONE_MESSAGE = (
    "🗑 *Full reset completed.*\n"
    "\n"
    "All your parameters have been cleared.\n"
    "Use /setwallet and /setamount to start over."
)

RESET_CANCELLED_MESSAGE = "✅ Reset cancelled. Your configuration is intact."
