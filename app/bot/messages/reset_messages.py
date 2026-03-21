"""Reset messages: individual resets (/resetwallet…) + full reset (/reset)."""

RESET_WALLET_MESSAGE = "🗑 *Wallet supprimé.*\nUtilise /setwallet pour en configurer un nouveau."

RESET_WALLET_BOT_STOPPED_MESSAGE = (
    "🗑 *Wallet supprimé.*\n"
    "⚠️ Le copy trading a été désactivé (wallet requis).\n"
    "\n"
    "Utilise /setwallet pour en configurer un nouveau."
)

RESET_AMOUNT_MESSAGE = "🗑 *Montant supprimé.*\nUtilise /setamount pour en définir un nouveau."

RESET_TP_MESSAGE = "🗑 *Take-profit supprimé.*\nUtilise /settp pour en définir un nouveau."

RESET_ENTRY_MC_MESSAGE = "🗑 *MC d'entrée supprimée.*\nUtilise /setentrymc pour en définir une nouvelle."

RESET_EXIT_MC_MESSAGE = "🗑 *MC de sortie supprimée.*\nUtilise /setexitmc pour en définir une nouvelle."

RESET_ALL_MESSAGE = (
    "🗑 *Configuration réinitialisée.*\n"
    "\n"
    "Tous les paramètres ont été effacés.\n"
    "Utilise /setwallet et /setamount pour recommencer."
)

RESET_NOTHING_MESSAGE = "ℹ️ {param} n'est pas configuré — rien à supprimer."

RESET_CONFIRM_ASK_MESSAGE = (
    "⚠️ *Reset complet*\n"
    "\n"
    "Cette action va :\n"
    "• Supprimer toute ta configuration\n"
    "• Supprimer toutes tes positions paper\n"
    "• Remettre tous les paramètres à zéro\n"
    "• Repasser en mode Paper Trading\n"
    "\n"
    "Tape `yes` pour confirmer ou /cancel pour annuler."
)

RESET_DONE_MESSAGE = (
    "🗑 *Reset complet effectué.*\n"
    "\n"
    "Tous tes paramètres ont été effacés.\n"
    "Utilise /setwallet et /setamount pour recommencer."
)

RESET_CANCELLED_MESSAGE = "✅ Reset annulé. Ta configuration est intacte."
