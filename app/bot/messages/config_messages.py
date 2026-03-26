"""Configuration flow messages: wallet, amount, take-profit, stop-loss, market caps, mode."""

ASK_WALLET_MESSAGE = (
    "🔗 *Wallet setup*\n"
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
    "The bot will now track buys from this wallet."
)

WALLET_UPDATED_MESSAGE = (
    "🔄 *Wallet updated!*\n"
    "\n"
    "New address: `{address}`"
)

ASK_AMOUNT_MESSAGE = (
    "💰 *Trade amount setup*\n"
    "\n"
    "How much SOL do you want to invest per copied trade?\n"
    "\n"
    "Type /cancel to abort."
)

AMOUNT_CONFIRM_MESSAGE = (
    "✅ *Amount configured!*\n"
    "\n"
    "Amount per trade: *{amount} SOL*"
)

ASK_TP_MESSAGE = (
    "📈 *Take-profit setup*\n"
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
    "The bot will sell when price reaches x{multiplier} of the entry price."
)

ASK_STOP_LOSS_MESSAGE = (
    "🛑 *Stop-loss setup*\n"
    "\n"
    "At what percentage loss do you want to sell?\n"
    "Examples: `50`, `25`, `50%`, `0.5`\n"
    "\n"
    "Type /cancel to abort."
)

STOP_LOSS_CONFIRM_MESSAGE = (
    "✅ *Stop-loss configured!*\n"
    "\n"
    "The bot will sell if the price drops to *{percent}%* of the entry price."
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
    "✅ *Entry MC configured!*\n"
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
    "✅ *Exit MC configured!*\n"
    "\n"
    "Target exit MC: *${value}*\n"
    "The bot will sell when the token reaches this market cap."
)

MODE_SET_PAPER_MESSAGE = (
    "📝 *Paper mode enabled*\n"
    "\n"
    "Trades are simulated — no real transactions."
)

MODE_SET_AUTO_MESSAGE = (
    "🤖 *Auto mode enabled*\n"
    "\n"
    "⚠️ The bot will execute real trades automatically.\n"
    "Make sure your trading wallet is funded.\n"
    "Use /startbot to activate."
)

MODE_SET_MANUAL_MESSAGE = (
    "🖐 *Manual mode enabled*\n"
    "\n"
    "You will receive alerts with a Jupiter link to execute trades yourself.\n"
    "Use /startbot to activate."
)

MODE_SET_LIVE_MESSAGE = MODE_SET_AUTO_MESSAGE

MODE_ALREADY_MESSAGE = "ℹ️ You are already in *{mode}* mode."

MODE_INVALID_MESSAGE = (
    "⚠️ Invalid mode.\n"
    "Usage: `/mode paper`, `/mode auto` or `/mode manual`"
)

MODE_USAGE_MESSAGE = (
    "⚙️ *Trading mode*\n"
    "\n"
    "Current mode: *{current_mode}*\n"
    "\n"
    "• `/mode paper` — simulated trades\n"
    "• `/mode auto` — bot executes trades automatically\n"
    "• `/mode manual` — receive alerts, trade manually"
)

WALLET_GENERATE_SUCCESS_MESSAGE = (
    "✅ *Trading wallet ready*\n"
    "\n"
    "Public key: `{public_key}`\n"
    "\n"
    "Send SOL to this address to fund your trading wallet.\n"
    "Use `/depositinfo` to see it again."
)

WALLET_GENERATE_ERROR_MESSAGE = (
    "⚠️ Failed to generate trading wallet. Please try again."
)

DEPOSIT_INFO_MESSAGE = (
    "💳 *Trading wallet*\n"
    "\n"
    "Address: `{public_key}`\n"
    "\n"
    "Send SOL here to fund auto trades.\n"
    "⚠️ Only send SOL — other tokens may be lost."
)

DEPOSIT_INFO_NO_WALLET_MESSAGE = (
    "⚠️ No trading wallet yet.\n"
    "Use /generatewallet to create one."
)
