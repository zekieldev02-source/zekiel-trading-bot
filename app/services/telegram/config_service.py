"""Service Telegram pour la gestion de la configuration de trading.

Chaque méthode d'action retourne un code résultat (str) que le handler
mappe vers le message Telegram approprié. Le service ne connaît pas les messages UI.

Codes communs :
    "success"        — opération réussie
    "backend_error"  — backend indisponible ou erreur réseau
    "already_empty"  — le champ était déjà vide, rien à faire
"""

from app.client.backend import config_client
from app.core.enums.trading_mode import TradingMode
from app.schemas.user_config import UserConfig


async def get_config(telegram_id: int) -> UserConfig | None:
    """Récupère la configuration courante de l'utilisateur.

    Retourne None si le backend est indisponible.
    """
    return await config_client.get_config(telegram_id)


# ------------------------------------------------------------------ #
#  Mises à jour de configuration
# ------------------------------------------------------------------ #

async def update_wallet(telegram_id: int, address: str) -> UserConfig | None:
    """Met à jour l'adresse du wallet suivi."""
    return await config_client.update_config(telegram_id, wallet_address=address)


async def update_trade_amount(telegram_id: int, amount: float) -> UserConfig | None:
    """Met à jour le montant d'entrée par trade."""
    return await config_client.update_config(telegram_id, trade_amount=amount)


async def update_tp_multiplier(telegram_id: int, multiplier: float) -> UserConfig | None:
    """Met à jour le multiplicateur de take-profit."""
    return await config_client.update_config(telegram_id, tp_multiplier=multiplier)


async def update_entry_market_cap(telegram_id: int, value: float) -> UserConfig | None:
    """Met à jour le market cap maximum d'entrée."""
    return await config_client.update_config(telegram_id, entry_market_cap=value)


async def update_exit_market_cap(telegram_id: int, value: float) -> UserConfig | None:
    """Met à jour le market cap cible de sortie."""
    return await config_client.update_config(telegram_id, exit_market_cap=value)


async def update_mode(telegram_id: int, mode: TradingMode) -> UserConfig | None:
    """Change le mode de trading (paper / live).

    Désactive systématiquement le bot lors du changement de mode
    pour éviter des trades involontaires.
    """
    return await config_client.update_config(
        telegram_id,
        mode=mode.value,
        bot_active=False,
        bot_status="idle",
    )


# ------------------------------------------------------------------ #
#  Contrôle du bot
# ------------------------------------------------------------------ #

async def activate_bot(telegram_id: int) -> str:
    """Valide les prérequis et active le bot de trading.

    Codes retournés :
        "success"         — bot activé
        "already_active"  — bot déjà en cours d'exécution
        "missing_wallet"  — wallet non configuré
        "missing_amount"  — montant non configuré
        "backend_error"   — backend indisponible
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if config.bot_active:
        return "already_active"
    if not config.wallet_address:
        return "missing_wallet"
    if not config.trade_amount:
        return "missing_amount"

    updated = await config_client.update_config(telegram_id, bot_active=True, bot_status="active")
    return "success" if updated is not None else "backend_error"


async def deactivate_bot(telegram_id: int) -> str:
    """Désactive le bot de trading.

    Codes retournés :
        "success"           — bot arrêté
        "already_inactive"  — bot déjà arrêté
        "backend_error"     — backend indisponible
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.bot_active:
        return "already_inactive"

    updated = await config_client.update_config(telegram_id, bot_active=False, bot_status="idle")
    return "success" if updated is not None else "backend_error"


# ------------------------------------------------------------------ #
#  Réinitialisations individuelles
# ------------------------------------------------------------------ #

async def reset_wallet(telegram_id: int) -> str:
    """Supprime le wallet et désactive le bot.

    Codes retournés :
        "success"            — wallet supprimé
        "success_was_active" — wallet supprimé, bot arrêté au passage
        "already_empty"      — aucun wallet configuré
        "backend_error"      — backend indisponible
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.wallet_address:
        return "already_empty"

    was_active = config.bot_active
    updated = await config_client.update_config(
        telegram_id,
        wallet_address=None,
        bot_active=False,
        bot_status="idle",
    )
    if updated is None:
        return "backend_error"
    return "success_was_active" if was_active else "success"


async def reset_amount(telegram_id: int) -> str:
    """Supprime le montant de trade et désactive le bot.

    Codes retournés :
        "success"        — montant supprimé
        "already_empty"  — aucun montant configuré
        "backend_error"  — backend indisponible
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.trade_amount:
        return "already_empty"

    updated = await config_client.update_config(
        telegram_id,
        trade_amount=None,
        bot_active=False,
        bot_status="idle",
    )
    return "success" if updated is not None else "backend_error"


async def reset_tp(telegram_id: int) -> str:
    """Supprime le multiplicateur de take-profit.

    Codes retournés :
        "success"        — TP supprimé
        "already_empty"  — aucun TP configuré
        "backend_error"  — backend indisponible
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.tp_multiplier:
        return "already_empty"

    updated = await config_client.update_config(telegram_id, tp_multiplier=None)
    return "success" if updated is not None else "backend_error"


async def reset_entry_mc(telegram_id: int) -> str:
    """Supprime le market cap d'entrée.

    Codes retournés :
        "success"        — MC d'entrée supprimé
        "already_empty"  — non configuré
        "backend_error"  — backend indisponible
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.entry_market_cap:
        return "already_empty"

    updated = await config_client.update_config(telegram_id, entry_market_cap=None)
    return "success" if updated is not None else "backend_error"


async def reset_exit_mc(telegram_id: int) -> str:
    """Supprime le market cap de sortie.

    Codes retournés :
        "success"        — MC de sortie supprimé
        "already_empty"  — non configuré
        "backend_error"  — backend indisponible
    """
    config = await config_client.get_config(telegram_id)
    if config is None:
        return "backend_error"
    if not config.exit_market_cap:
        return "already_empty"

    updated = await config_client.update_config(telegram_id, exit_market_cap=None)
    return "success" if updated is not None else "backend_error"


async def reset_all_fields(telegram_id: int) -> str:
    """Remet tous les champs de config à None et désactive le bot.
    Les positions paper sont conservées.

    Codes retournés :
        "success"       — config remise à zéro
        "backend_error" — backend indisponible
    """
    updated = await config_client.update_config(
        telegram_id,
        wallet_address=None,
        trading_wallet_public_key=None,
        trade_amount=None,
        tp_multiplier=None,
        entry_market_cap=None,
        exit_market_cap=None,
        bot_active=False,
        bot_status="idle",
    )
    return "success" if updated is not None else "backend_error"
