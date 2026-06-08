"""Messages for inline menus."""

from app.core.enums.trading_mode import TradingMode  # used in _MODE_DESCRIPTIONS
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
        f"*Mode:* {config.mode.display}\n"
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
    "menu:ct:wallet": (
        "🔗 *Smart money wallet to copy*\n"
        "Use /setwallet to set the wallet you want to track.\n"
        "_This is someone else's wallet — not your own._"
    ),
    "menu:ct:amount": "💰 To set your trade amount, use /setamount",
    "menu:ct:tp": "📊 To set your take-profit multiplier, use /settp",
    "menu:ct:mc": (
        "📉 To configure market caps:\n"
        "• Max entry MC → /setentrymc\n"
        "• Target exit MC → /setexitmc"
    ),
    "menu:settings:wallet": (
        "🔗 *Smart money wallet to copy*\n"
        "Use /setwallet to set the wallet you want to track.\n"
        "_This is someone else's wallet — not your own._"
    ),
    "menu:settings:amount": "💰 To set your trade amount, use /setamount",
    "menu:settings:tp": "📈 To set your take-profit multiplier, use /settp",
    "menu:settings:sl": "🛑 To set your stop-loss percentage, use /setstoploss",
    "menu:settings:entrymc": "📉 To set the max entry market cap, use /setentrymc",
    "menu:settings:exitmc": "📈 To set the target exit market cap, use /setexitmc",
    "menu:settings:importwallet": (
        "📥 *Import your personal wallet*\n"
        "Use /importwallet to import your own Solana wallet by private key.\n"
        "_Your key is encrypted immediately. Your message will be deleted._"
    ),
}


def get_config_hint(callback_data: str) -> str:
    return _CONFIG_HINTS.get(callback_data, "Use the available commands.")


_MODE_DESCRIPTIONS = {
    TradingMode.PAPER: "📝 *Paper* — trades simulées, aucun SOL dépensé.",
    TradingMode.AUTO: "🤖 *Auto* — le bot exécute de vrais swaps automatiquement.",
    TradingMode.MANUAL: "🖐 *Manual* — tu reçois des alertes et trades toi-même.",
}


def get_mode_menu_message(config: UserConfig) -> str:
    current = config.mode
    desc = _MODE_DESCRIPTIONS.get(current, "")
    return (
        "🔀 *Trading Mode*\n"
        "\n"
        f"Mode actuel : *{current.display}*\n"
        f"{desc}\n"
        "\n"
        "_Sélectionne un mode ci-dessous. Le bot sera mis en pause lors d'un changement._"
    )


def _fmt_mc(value: float | None) -> str:
    if value is None:
        return "➖ Not configured"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"
