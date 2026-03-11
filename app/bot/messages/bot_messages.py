"""Bot-level messages: start, help, control (startbot/stopbot), status, settings."""

from app.schemas.user_config import UserConfig


# ------------------------------------------------------------------ #
#  /start
# ------------------------------------------------------------------ #

START_MESSAGE = (
    "🚀 *Bienvenue sur Zekiel Bot !*\n"
    "\n"
    "Ton assistant de copy trading sur Solana.\n"
    "\n"
    "Pour commencer :\n"
    "1️⃣ Configure un wallet à suivre → /setwallet\n"
    "2️⃣ Définis ton montant d'entrée → /setamount\n"
    "3️⃣ Lance le copy trading → /startbot\n"
    "\n"
    "Tape /help pour voir toutes les commandes."
)

# ------------------------------------------------------------------ #
#  /help
# ------------------------------------------------------------------ #

HELP_MESSAGE = (
    "📖 *Commandes disponibles*\n"
    "\n"
    "*Configuration :*\n"
    "/setwallet — Définir le wallet à suivre\n"
    "/setamount — Définir le montant d'entrée (SOL)\n"
    "/settp — Définir le multiplicateur de take-profit\n"
    "/setentrymc — Définir le market cap max d'entrée\n"
    "/setexitmc — Définir le market cap cible de sortie\n"
    "/mode — Choisir le mode (paper / live)\n"
    "\n"
    "*Réinitialisation :*\n"
    "/resetwallet — Supprimer le wallet\n"
    "/resetamount — Supprimer le montant\n"
    "/resettp — Supprimer le take-profit\n"
    "/resetentrymc — Supprimer le MC d'entrée\n"
    "/resetexitmc — Supprimer le MC de sortie\n"
    "/resetall — Réinitialiser la config\n"
    "/reset — Tout réinitialiser (config + positions)\n"
    "\n"
    "*Contrôle :*\n"
    "/startbot — Activer le copy trading\n"
    "/stopbot — Désactiver le copy trading\n"
    "\n"
    "*Informations :*\n"
    "/settings — Voir ta configuration\n"
    "/status — État du bot\n"
    "/help — Afficher cette aide"
)

# ------------------------------------------------------------------ #
#  /startbot, /stopbot
# ------------------------------------------------------------------ #

BOT_STARTED_MESSAGE = (
    "🟢 *Copy trading activé !*\n"
    "\n"
    "Le bot surveille maintenant le wallet configuré.\n"
    "Utilise /stopbot pour désactiver."
)

BOT_STOPPED_MESSAGE = (
    "🔴 *Copy trading désactivé.*\n"
    "\n"
    "Le bot ne copiera plus de trades.\n"
    "Utilise /startbot pour réactiver."
)

BOT_ALREADY_ACTIVE_MESSAGE = "ℹ️ Le copy trading est déjà actif."

BOT_ALREADY_STOPPED_MESSAGE = "ℹ️ Le copy trading est déjà arrêté."

# ------------------------------------------------------------------ #
#  /status
# ------------------------------------------------------------------ #


def get_status_message(config: UserConfig) -> str:
    """Build a formatted status summary from the user's config."""
    wallet = config.wallet_address or "Non configuré"
    amount = f"{config.trade_amount} SOL" if config.trade_amount else "Non configuré"
    tp = f"x{config.tp_multiplier}" if config.tp_multiplier else "Non configuré"
    entry_mc = _format_market_cap(config.entry_market_cap)
    exit_mc = _format_market_cap(config.exit_market_cap)
    bot_state = "🟢 Actif" if config.bot_active else "⏸ Inactif"
    mode = config.mode.display
    positions_count = len([p for p in config.positions if p.get("status") == "open"])

    return (
        "📊 *État du Bot*\n"
        "\n"
        f"*Statut :* {bot_state}\n"
        f"*Mode :* {mode}\n"
        f"*Positions ouvertes :* {positions_count}\n"
        "\n"
        f"*Wallet suivi :* `{wallet}`\n"
        f"*Montant d'entrée :* {amount}\n"
        f"*Take-profit :* {tp}\n"
        f"*MC max d'entrée :* {entry_mc}\n"
        f"*MC cible de sortie :* {exit_mc}\n"
    )


# ------------------------------------------------------------------ #
#  /settings
# ------------------------------------------------------------------ #


def get_settings_message(config: UserConfig) -> str:
    """Build a formatted settings summary."""
    wallet = f"`{config.wallet_address}`" if config.wallet_address else "❌ Non configuré"
    amount = f"{config.trade_amount} SOL" if config.trade_amount else "❌ Non configuré"
    tp = f"x{config.tp_multiplier}" if config.tp_multiplier else "➖ Non configuré"
    entry_mc = _format_mc(config.entry_market_cap)
    exit_mc = _format_mc(config.exit_market_cap)
    bot_state = "🟢 Actif" if config.bot_active else "🔴 Inactif"
    mode = config.mode.display

    return (
        "⚙️ *Ta configuration*\n"
        "\n"
        f"*Mode :* {mode}\n"
        f"*Wallet suivi :* {wallet}\n"
        f"*Montant d'entrée :* {amount}\n"
        f"*Take-profit :* {tp}\n"
        f"*MC max d'entrée :* {entry_mc}\n"
        f"*MC cible de sortie :* {exit_mc}\n"
        "\n"
        f"*Copy trading :* {bot_state}"
    )


# ------------------------------------------------------------------ #
#  Helpers
# ------------------------------------------------------------------ #


def _format_market_cap(value: float | None) -> str:
    if value is None:
        return "Non configuré"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


def _format_mc(value: float | None) -> str:
    if value is None:
        return "➖ Non configuré"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"
