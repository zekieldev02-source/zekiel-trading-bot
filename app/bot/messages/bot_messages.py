"""Bot-level messages: start, help, control (startbot/stopbot), status, settings."""

from app.schemas.user_config import UserConfig


START_MESSAGE = (
    "🚀 *Welcome to Zekiel Bot!*\n"
    "\n"
    "Your copy trading assistant on Solana.\n"
    "\n"
    "To get started:\n"
    "1️⃣ Configure a wallet to track → /setwallet\n"
    "2️⃣ Set your trade amount → /setamount\n"
    "3️⃣ Start copy trading → /startbot\n"
    "\n"
    "Type /help to see all commands."
)

HELP_MESSAGE = (
    "📖 *Available commands*\n"
    "\n"
    "*Configuration:*\n"
    "/setwallet — Set the wallet to track\n"
    "/setamount — Set the trade amount (SOL)\n"
    "/settp — Set the take-profit multiplier\n"
    "/setstoploss — Set the stop-loss percentage\n"
    "/setentrymc — Set the max entry market cap\n"
    "/setexitmc — Set the target exit market cap\n"
    "/mode — Choose mode (paper / live)\n"
    "\n"
    "*Reset:*\n"
    "/resetwallet — Remove the wallet\n"
    "/resetamount — Remove the amount\n"
    "/resettp — Remove the take-profit\n"
    "/resetstoploss — Remove the stop-loss\n"
    "/resetentrymc — Remove the entry MC\n"
    "/resetexitmc — Remove the exit MC\n"
    "/resetall — Reset all configuration\n"
    "/reset — Full reset (config + positions)\n"
    "\n"
    "*Control:*\n"
    "/startbot — Enable copy trading\n"
    "/stopbot — Disable copy trading\n"
    "\n"
    "*Info:*\n"
    "/settings — View your configuration\n"
    "/status — Bot status\n"
    "/positions — View your paper positions\n"
    "/help — Show this help"
)

BOT_STARTED_MESSAGE = (
    "🟢 *Copy trading enabled!*\n"
    "\n"
    "The bot is now tracking the configured wallet.\n"
    "Use /stopbot to disable."
)

BOT_STOPPED_MESSAGE = (
    "🔴 *Copy trading disabled.*\n"
    "\n"
    "The bot is no longer copying trades.\n"
    "Use /startbot to re-enable."
)

BOT_ALREADY_ACTIVE_MESSAGE = "ℹ️ Copy trading is already active."

BOT_ALREADY_STOPPED_MESSAGE = "ℹ️ Copy trading is already stopped."


def get_status_message(config: UserConfig) -> str:
    wallet = config.wallet_address or "Not configured"
    amount = f"{config.trade_amount} SOL" if config.trade_amount else "Not configured"
    tp = f"x{config.tp_multiplier}" if config.tp_multiplier else "Not configured"
    sl = f"{config.stop_loss_multiplier * 100:.0f}%" if config.stop_loss_multiplier else "Not configured"
    entry_mc = _format_market_cap(config.entry_market_cap)
    exit_mc = _format_market_cap(config.exit_market_cap)
    bot_state = "🟢 Active" if config.bot_active else "⏸ Inactive"
    mode = config.mode.display
    positions_count = len([p for p in config.positions if p.get("status") == "open"])

    return (
        "📊 *Bot status*\n"
        "\n"
        f"*Status:* {bot_state}\n"
        f"*Mode:* {mode}\n"
        f"*Open positions:* {positions_count}\n"
        "\n"
        f"*Tracked wallet:* `{wallet}`\n"
        f"*Amount per trade:* {amount}\n"
        f"*Take-profit:* {tp}\n"
        f"*Stop-loss:* {sl}\n"
        f"*Max entry MC:* {entry_mc}\n"
        f"*Target exit MC:* {exit_mc}\n"
    )


def get_settings_message(config: UserConfig) -> str:
    wallet = f"`{config.wallet_address}`" if config.wallet_address else "❌ Not configured"
    amount = f"{config.trade_amount} SOL" if config.trade_amount else "❌ Not configured"
    tp = f"x{config.tp_multiplier}" if config.tp_multiplier else "➖ Not configured"
    sl = f"{config.stop_loss_multiplier * 100:.0f}%" if config.stop_loss_multiplier else "➖ Not configured"
    entry_mc = _format_mc(config.entry_market_cap)
    exit_mc = _format_mc(config.exit_market_cap)
    bot_state = "🟢 Active" if config.bot_active else "🔴 Inactive"
    mode = config.mode.display

    return (
        "⚙️ *Settings*\n"
        "\n"
        f"*Mode:* {mode}\n"
        f"*Copy trading:* {bot_state}\n"
        "\n"
        f"*Tracked wallet:* {wallet}\n"
        f"*Amount per trade:* {amount}\n"
        f"*Take-profit:* {tp}\n"
        f"*Stop-loss:* {sl}\n"
        f"*Max entry MC:* {entry_mc}\n"
        f"*Target exit MC:* {exit_mc}\n"
        "\n"
        "_Tap a parameter below to modify it._"
    )


def _format_market_cap(value: float | None) -> str:
    if value is None:
        return "Not configured"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


def _format_mc(value: float | None) -> str:
    if value is None:
        return "➖ Not configured"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"
