"""Configuration flow messages: wallet, amount, take-profit, market caps, mode."""

# ------------------------------------------------------------------ #
#  /setwallet
# ------------------------------------------------------------------ #

ASK_WALLET_MESSAGE = (
    "🔗 *Configuration du wallet*\n"
    "\n"
    "Envoie-moi l'adresse du wallet Solana que tu veux suivre.\n"
    "\n"
    "Tape /cancel pour annuler."
)

WALLET_CONFIRM_MESSAGE = (
    "✅ *Wallet configuré !*\n"
    "\n"
    "Adresse : `{address}`\n"
    "\n"
    "Le bot surveillera les achats de ce wallet."
)

WALLET_UPDATED_MESSAGE = (
    "🔄 *Wallet mis à jour !*\n"
    "\n"
    "Nouvelle adresse : `{address}`"
)

# ------------------------------------------------------------------ #
#  /setamount
# ------------------------------------------------------------------ #

ASK_AMOUNT_MESSAGE = (
    "💰 *Configuration du montant d'entrée*\n"
    "\n"
    "Combien de SOL veux-tu engager par trade copié ?\n"
    "\n"
    "Tape /cancel pour annuler."
)

AMOUNT_CONFIRM_MESSAGE = (
    "✅ *Montant configuré !*\n"
    "\n"
    "Montant d'entrée : *{amount} SOL* par trade."
)

# ------------------------------------------------------------------ #
#  /settp
# ------------------------------------------------------------------ #

ASK_TP_MESSAGE = (
    "📈 *Configuration du take-profit*\n"
    "\n"
    "Quel multiplicateur de sortie veux-tu ?\n"
    "Exemples : `1.5`, `2`, `x3`, `x10`\n"
    "\n"
    "Tape /cancel pour annuler."
)

TP_CONFIRM_MESSAGE = (
    "✅ *Take-profit configuré !*\n"
    "\n"
    "Multiplicateur : *x{multiplier}*\n"
    "Le bot vendra quand le prix atteint x{multiplier} du prix d'entrée."
)

# ------------------------------------------------------------------ #
#  /setentrymc
# ------------------------------------------------------------------ #

ASK_ENTRY_MC_MESSAGE = (
    "🎯 *Market cap max d'entrée*\n"
    "\n"
    "Quel est le market cap maximum pour accepter un trade ?\n"
    "Exemples : `500000`, `500k`, `1M`\n"
    "\n"
    "Tape /cancel pour annuler."
)

ENTRY_MC_CONFIRM_MESSAGE = (
    "✅ *Market cap d'entrée configuré !*\n"
    "\n"
    "MC max d'entrée : *${value}*\n"
    "Les tokens avec un MC supérieur seront ignorés."
)

# ------------------------------------------------------------------ #
#  /setexitmc
# ------------------------------------------------------------------ #

ASK_EXIT_MC_MESSAGE = (
    "🏁 *Market cap cible de sortie*\n"
    "\n"
    "À quel market cap veux-tu que le bot vende ?\n"
    "Exemples : `5000000`, `5M`, `10M`\n"
    "\n"
    "Tape /cancel pour annuler."
)

EXIT_MC_CONFIRM_MESSAGE = (
    "✅ *Market cap de sortie configuré !*\n"
    "\n"
    "MC cible de sortie : *${value}*\n"
    "Le bot vendra quand le token atteint ce market cap."
)

# ------------------------------------------------------------------ #
#  /mode
# ------------------------------------------------------------------ #

MODE_SET_PAPER_MESSAGE = (
    "📝 *Mode Paper Trading activé !*\n"
    "\n"
    "Les trades seront simulés.\n"
    "Aucune transaction réelle ne sera exécutée."
)

MODE_SET_LIVE_MESSAGE = (
    "💰 *Mode Live Trading activé !*\n"
    "\n"
    "⚠️ Les trades seront réels.\n"
    "Le copy trading a été désactivé par précaution.\n"
    "Utilise /startbot pour le réactiver."
)

MODE_ALREADY_MESSAGE = "ℹ️ Tu es déjà en mode *{mode}*."

MODE_INVALID_MESSAGE = (
    "⚠️ Mode invalide.\n"
    "Usage : `/mode paper` ou `/mode live`"
)

MODE_USAGE_MESSAGE = (
    "⚙️ *Mode de trading*\n"
    "\n"
    "Mode actuel : *{current_mode}*\n"
    "\n"
    "Usage : `/mode paper` ou `/mode live`"
)
