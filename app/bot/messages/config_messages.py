"""Configuration flow messages: wallet, amount, take-profit, market caps, mode."""

ASK_WALLET_MESSAGE = (
    "🔗 *Wallet configuration*\n"
    "\n"
    "Send me the Solana wallet address you want to track.\n"
    "\n"
    "Type /cancel to abort."
)

WALLET_CONFIRM_MESSAGE = (
    "✅ *Wallet configured!*\n"
    "\n"
    "Address: `{address}`\n"
    "\n"
    "The bot will monitor purchases from this wallet."
)

WALLET_UPDATED_MESSAGE = (
    "🔄 *Wallet updated!*\n"
    "\n"
    "New address: `{address}`"
)

ASK_AMOUNT_MESSAGE = (
    "💰 *Trade amount configuration*\n"
    "\n"
    "How many SOL do you want to commit per copied trade?\n"
    "\n"
    "Type /cancel to abort."
)

AMOUNT_CONFIRM_MESSAGE = (
    "✅ *Amount configured!*\n"
    "\n"
    "Trade amount: *{amount} SOL* per trade."
)

ASK_TP_MESSAGE = (
    "📈 *Take-profit configuration*\n"
    "\n"
    "What exit multiplier do you want?\n"
    "Examples: `1.5`, `2`, `x3`, `x10`\n"
    "\n"
    "Type /cancel to abort."
)

TP_CONFIRM_MESSAGE = (
    "✅ *Take-profit configured!*\n"
    "\n"
    "Multiplier: *x{multiplier}*\n"
    "The bot will sell when the price reaches x{multiplier} of the entry price."
)

ASK_ENTRY_MC_MESSAGE = (
    "🎯 *Max entry market cap*\n"
    "\n"
    "What is the maximum market cap to accept a trade?\n"
    "Examples: `500000`, `500k`, `1M`\n"
    "\n"
    "Type /cancel to abort."
)

ENTRY_MC_CONFIRM_MESSAGE = (
    "✅ *Entry market cap configured!*\n"
    "\n"
    "Max entry MC: *${value}*\n"
    "Tokens with a higher MC will be ignored."
)

ASK_EXIT_MC_MESSAGE = (
    "🏁 *Target exit market cap*\n"
    "\n"
    "At what market cap should the bot sell?\n"
    "Examples: `5000000`, `5M`, `10M`\n"
    "\n"
    "Type /cancel to abort."
)

EXIT_MC_CONFIRM_MESSAGE = (
    "✅ *Exit market cap configured!*\n"
    "\n"
    "Target exit MC: *${value}*\n"
    "The bot will sell when the token reaches this market cap."
)

MODE_SET_PAPER_MESSAGE = (
    "📝 *Paper Trading mode enabled!*\n"
    "\n"
    "Trades will be simulated.\n"
    "No real transactions will be executed."
)

MODE_SET_LIVE_MESSAGE = (
    "💰 *Live Trading mode enabled!*\n"
    "\n"
    "⚠️ Trades will be real.\n"
    "Copy trading has been disabled as a precaution.\n"
    "Use /startbot to re-enable it."
)

MODE_ALREADY_MESSAGE = "ℹ️ You are already in *{mode}* mode."

MODE_INVALID_MESSAGE = (
    "⚠️ Invalid mode.\n"
    "Usage: `/mode paper` or `/mode live`"
)

MODE_USAGE_MESSAGE = (
    "⚙️ *Trading mode*\n"
    "\n"
    "Current mode: *{current_mode}*\n"
    "\n"
    "Usage: `/mode paper` or `/mode live`"
)
