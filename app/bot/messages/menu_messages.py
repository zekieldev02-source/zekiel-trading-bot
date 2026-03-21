"""Messages for inline menus."""

from app.schemas.user_config import UserConfig


def get_main_menu_message(config: UserConfig) -> str:
    status = "🟢 Active" if config.bot_active else "🔴 Inactive"
    wallet = f"`{config.wallet_address}`" if config.wallet_address else "❌ Not configured"
    amount = f"{config.trade_amount} SOL" if config.trade_amount else "❌ Not configured"
    open_count = len([p for p in config.positions if p.get("status") == "open"])

    return (
        "🤖 *Zekiel Bot*\n"
        "\n"
        f"*Status:* {status}\n"
        f"*Open positions:* {open_count}\n"
        "\n"
        f"*Tracked wallet:* {wallet}\n"
        f"*Amount per trade:* {amount}\n"
    )


def get_copy_trading_menu_message(config: UserConfig) -> str:
    wallet = f"`{config.wallet_address}`" if config.wallet_address else "❌ Not configured"
    amount = f"{config.trade_amount} SOL" if config.trade_amount else "❌ Not configured"
    tp = f"x{config.tp_multiplier}" if config.tp_multiplier else "➖ Not configured"
    entry_mc = _fmt_mc(config.entry_market_cap)
    exit_mc = _fmt_mc(config.exit_market_cap)

    return (
        "🔁 *Copy Trading*\n"
        "\n"
        f"*Tracked wallet:* {wallet}\n"
        f"*Amount per trade:* {amount}\n"
        f"*Take-profit:* {tp}\n"
        f"*Max entry MC:* {entry_mc}\n"
        f"*Target exit MC:* {exit_mc}\n"
        "\n"
        "_Use the buttons below to update your configuration._"
    )


_CONFIG_HINTS: dict[str, str] = {
    "menu:ct:wallet": "✏️ To configure your tracked wallet, use the /setwallet command",
    "menu:ct:amount": "💰 To set your trade amount, use the /setamount command",
    "menu:ct:tp": "📊 To set your take-profit, use the /settp command",
    "menu:ct:mc": (
        "📉 To configure market caps:\n"
        "• Entry → /setentrymc\n"
        "• Exit → /setexitmc"
    ),
}


def get_config_hint(callback_data: str) -> str:
    """Returns the instruction message for a configuration button."""
    return _CONFIG_HINTS.get(callback_data, "Use the available commands.")


def _fmt_mc(value: float | None) -> str:
    if value is None:
        return "➖ Not configured"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"
