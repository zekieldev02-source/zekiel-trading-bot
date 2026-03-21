"""Configuration flow messages: wallet, amount, take-profit, market caps, mode."""

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

ASK_AMOUNT_MESSAGE = (
    "💰 *Configuration du montant*\n"
    "\n"
    "Combien de SOL veux-tu investir par trade copié ?\n"
    "\n"
    "Tape /cancel pour annuler."
)

AMOUNT_CONFIRM_MESSAGE = (
    "✅ *Montant configuré !*\n"
    "\n"
    "Montant par trade : *{amount} SOL*"
)

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
    "Le bot vendra quand le prix atteindra x{multiplier} du prix d'entrée."
)

ASK_ENTRY_MC_MESSAGE = (
    "🎯 *MC d'entrée maximale*\n"
    "\n"
    "Quelle est la market cap maximale pour accepter un trade ?\n"
    "Exemples : `500000`, `500k`, `1M`\n"
    "\n"
    "Tape /cancel pour annuler."
)

ENTRY_MC_CONFIRM_MESSAGE = (
    "✅ *MC d'entrée configurée !*\n"
    "\n"
    "MC d'entrée max : *${value}*\n"
    "Les tokens avec une MC plus élevée seront ignorés."
)

ASK_EXIT_MC_MESSAGE = (
    "🏁 *MC de sortie cible*\n"
    "\n"
    "À quelle market cap le bot doit-il vendre ?\n"
    "Exemples : `5000000`, `5M`, `10M`\n"
    "\n"
    "Tape /cancel pour annuler."
)

EXIT_MC_CONFIRM_MESSAGE = (
    "✅ *MC de sortie configurée !*\n"
    "\n"
    "MC de sortie cible : *${value}*\n"
    "Le bot vendra quand le token atteindra cette market cap."
)

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
