"""Messages for inline menus."""

from app.schemas.user_config import UserConfig


def get_main_menu_message(config: UserConfig) -> str:
    status = "🟢 Actif" if config.bot_active else "🔴 Inactif"
    wallet = f"`{config.wallet_address}`" if config.wallet_address else "❌ Non configuré"
    amount = f"{config.trade_amount} SOL" if config.trade_amount else "❌ Non configuré"
    open_count = len([p for p in config.positions if p.get("status") == "open"])

    return (
        "🤖 *Zekiel Bot*\n"
        "\n"
        f"*Statut :* {status}\n"
        f"*Positions ouvertes :* {open_count}\n"
        "\n"
        f"*Wallet suivi :* {wallet}\n"
        f"*Montant par trade :* {amount}\n"
    )


def get_copy_trading_menu_message(config: UserConfig) -> str:
    wallet = f"`{config.wallet_address}`" if config.wallet_address else "❌ Non configuré"
    amount = f"{config.trade_amount} SOL" if config.trade_amount else "❌ Non configuré"
    tp = f"x{config.tp_multiplier}" if config.tp_multiplier else "➖ Non configuré"
    entry_mc = _fmt_mc(config.entry_market_cap)
    exit_mc = _fmt_mc(config.exit_market_cap)

    return (
        "🔁 *Copy Trading*\n"
        "\n"
        f"*Wallet suivi :* {wallet}\n"
        f"*Montant par trade :* {amount}\n"
        f"*Take-profit :* {tp}\n"
        f"*MC d'entrée max :* {entry_mc}\n"
        f"*MC de sortie cible :* {exit_mc}\n"
        "\n"
        "_Utilise les boutons ci-dessous pour mettre à jour ta configuration._"
    )


_CONFIG_HINTS: dict[str, str] = {
    "menu:ct:wallet": "✏️ Pour configurer ton wallet suivi, utilise la commande /setwallet",
    "menu:ct:amount": "💰 Pour définir ton montant par trade, utilise la commande /setamount",
    "menu:ct:tp": "📊 Pour définir ton take-profit, utilise la commande /settp",
    "menu:ct:mc": (
        "📉 Pour configurer les market caps :\n"
        "• Entrée → /setentrymc\n"
        "• Sortie → /setexitmc"
    ),
}


def get_config_hint(callback_data: str) -> str:
    """Returns the instruction message for a configuration button."""
    return _CONFIG_HINTS.get(callback_data, "Utilise les commandes disponibles.")


def _fmt_mc(value: float | None) -> str:
    if value is None:
        return "➖ Non configuré"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"
