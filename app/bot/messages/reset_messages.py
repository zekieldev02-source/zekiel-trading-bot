"""Reset messages: individual resets (/resetwallet…) + full reset (/reset)."""

# ------------------------------------------------------------------ #
#  Individual resets
# ------------------------------------------------------------------ #

RESET_WALLET_MESSAGE = "🗑 *Wallet supprimé.*\nUtilise /setwallet pour en configurer un nouveau."

RESET_WALLET_BOT_STOPPED_MESSAGE = (
    "🗑 *Wallet supprimé.*\n"
    "⚠️ Le copy trading a été désactivé (wallet requis).\n"
    "\n"
    "Utilise /setwallet pour en configurer un nouveau."
)

RESET_AMOUNT_MESSAGE = "🗑 *Montant d'entrée supprimé.*\nUtilise /setamount pour le redéfinir."

RESET_TP_MESSAGE = "🗑 *Take-profit supprimé.*\nUtilise /settp pour le redéfinir."

RESET_ENTRY_MC_MESSAGE = "🗑 *MC max d'entrée supprimé.*\nUtilise /setentrymc pour le redéfinir."

RESET_EXIT_MC_MESSAGE = "🗑 *MC cible de sortie supprimé.*\nUtilise /setexitmc pour le redéfinir."

RESET_ALL_MESSAGE = (
    "🗑 *Configuration réinitialisée.*\n"
    "\n"
    "Tous les paramètres ont été remis à zéro.\n"
    "Utilise /setwallet et /setamount pour recommencer."
)

RESET_NOTHING_MESSAGE = "ℹ️ Le {param} n'est pas configuré, rien à supprimer."

# ------------------------------------------------------------------ #
#  Full reset (/reset with confirmation)
# ------------------------------------------------------------------ #

RESET_CONFIRM_ASK_MESSAGE = (
    "⚠️ *Réinitialisation complète*\n"
    "\n"
    "Cette action va :\n"
    "• Supprimer toute ta configuration\n"
    "• Supprimer toutes tes positions paper\n"
    "• Remettre tous les paramètres par défaut\n"
    "• Remettre le mode en Paper Trading\n"
    "\n"
    "Tape `oui` pour confirmer ou /cancel pour annuler."
)

RESET_DONE_MESSAGE = (
    "🗑 *Réinitialisation complète effectuée.*\n"
    "\n"
    "Tous tes paramètres ont été remis à zéro.\n"
    "Utilise /setwallet et /setamount pour recommencer."
)

RESET_CANCELLED_MESSAGE = "✅ Réinitialisation annulée. Ta configuration est intacte."
