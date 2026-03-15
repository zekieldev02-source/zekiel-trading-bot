"""Messages pour la commande /positions."""

from decimal import Decimal, InvalidOperation

from telegram.helpers import escape_markdown

# Le backend renvoie toutes les positions fermées triées.
# C'est le bot qui décide d'en limiter l'affichage — pas le backend.
MAX_CLOSED_DISPLAY = 3


NO_POSITIONS_MESSAGE = (
    "📊 *Positions paper*\n"
    "\n"
    "Tu n'as encore aucune position paper.\n"
    "Le bot en créera automatiquement quand un signal sera détecté."
)


def get_positions_message(data: dict) -> str:
    """Construit le message Telegram depuis la réponse /positions/summary.

    Gère proprement tous les cas :
    - positions ouvertes sans fermées
    - positions fermées sans ouvertes
    - mix des deux

    Les valeurs dynamiques (token_symbol, token_address, close_reason)
    sont systématiquement échappées pour éviter tout bug Markdown.

    Args:
        data: dict contenant open_positions, closed_positions et summary.

    Returns:
        Message formaté en Markdown v1 pour Telegram.
    """
    summary = data.get("summary", {})
    open_positions: list[dict] = data.get("open_positions", [])
    closed_positions: list[dict] = data.get("closed_positions", [])

    open_count: int = summary.get("open_count", 0)
    closed_count: int = summary.get("closed_count", 0)

    lines = ["📊 *Positions paper*", ""]

    # ---- Résumé global ----
    lines.append(f"🟢 Ouvertes : {open_count}")
    lines.append(f"🔴 Fermées : {closed_count}")

    if closed_count > 0:
        total_pnl = _to_decimal(summary.get("total_pnl_absolute", 0))
        avg_pnl = _to_decimal(summary.get("average_pnl_percent", 0))
        pnl_sign = "+" if total_pnl >= 0 else ""
        avg_sign = "+" if avg_pnl >= 0 else ""
        lines.append(f"💰 PnL total : {pnl_sign}{total_pnl:.4f} SOL")
        lines.append(f"📈 PnL moyen : {avg_sign}{avg_pnl:.2f}%")

    # ---- Positions ouvertes ----
    lines.append("")
    if open_positions:
        lines.append("*Positions ouvertes :*")
        for i, pos in enumerate(open_positions, start=1):
            symbol = _safe_md(pos.get("token_symbol") or pos.get("token_address", "?"))
            lines.append("")
            lines.append(f"{i}. *{symbol}*")
            lines.append(f"   Entrée : `{_fmt_price(pos.get('entry_price'))}` SOL")
            lines.append(f"   Montant : `{_fmt_amount(pos.get('amount'))}` SOL")

            tp = pos.get("take_profit_multiplier")
            if tp:
                lines.append(f"   TP : x{_to_decimal(tp):.2f}")

            mc = pos.get("entry_market_cap")
            if mc:
                lines.append(f"   MC entrée : {_fmt_market_cap(_to_decimal(mc))}")
    else:
        # Il y a forcément des positions fermées (le handler garantit qu'au moins l'un des deux > 0)
        lines.append("_Aucune position ouverte actuellement._")

    # ---- Dernières positions fermées ----
    # La limite MAX_CLOSED_DISPLAY est appliquée ici côté bot.
    # Le backend renvoie tout — cette décision d'affichage reste côté UI.
    if closed_positions:
        recent = closed_positions[:MAX_CLOSED_DISPLAY]
        lines.append("")
        lines.append(f"*Dernières positions fermées ({len(recent)}/{closed_count}) :*")
        for pos in recent:
            symbol = _safe_md(pos.get("token_symbol") or pos.get("token_address", "?"))
            reason = _safe_md(_fmt_close_reason(pos.get("close_reason")))
            pnl_abs = pos.get("pnl_absolute")
            pnl_pct = pos.get("pnl_percent")

            pnl_str = ""
            if pnl_abs is not None and pnl_pct is not None:
                pnl_d = _to_decimal(pnl_abs)
                pct_d = _to_decimal(pnl_pct)
                sign = "+" if pnl_d >= 0 else ""
                pnl_str = f" — {sign}{pnl_d:.4f} SOL ({sign}{pct_d:.2f}%)"

            lines.append(f"  • *{symbol}*{pnl_str} _{reason}_")
    elif open_positions:
        lines.append("")
        lines.append("_Aucune position fermée pour le moment._")

    return "\n".join(lines)


# ------------------------------------------------------------------ #
#  Helpers
# ------------------------------------------------------------------ #


def _safe_md(text: str) -> str:
    """Échappe les caractères spéciaux Markdown v1 pour Telegram (*_`[).

    À appliquer sur toutes les valeurs dynamiques injectées dans le message :
    token_symbol, token_address, close_reason, etc.
    """
    return escape_markdown(str(text), version=1)


def _to_decimal(value) -> Decimal:
    """Convertit toute valeur numérique (float, str, int) en Decimal.

    Passage par str() pour éviter les imprécisions d'un float intermédiaire.
    Par exemple : Decimal(str(0.1 + 0.2)) == Decimal("0.3"), alors que
    Decimal(0.1 + 0.2) reflète l'imprécision binaire.
    """
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return Decimal("0")


def _fmt_price(value) -> str:
    """Formate un prix de token avec une précision adaptée à sa magnitude.

    Utilise Decimal pour éviter les imprécisions float sur les très petits prix
    (ex : tokens Solana à 0.000000001 SOL).
    """
    if value is None:
        return "?"
    d = _to_decimal(value)
    if d == 0:
        return "0"
    if d < Decimal("0.000001"):
        return f"{d:.12f}".rstrip("0").rstrip(".")
    if d < Decimal("0.001"):
        return f"{d:.8f}".rstrip("0").rstrip(".")
    return f"{d:.6f}".rstrip("0").rstrip(".")


def _fmt_amount(value) -> str:
    if value is None:
        return "?"
    return f"{_to_decimal(value):.4f}".rstrip("0").rstrip(".")


def _fmt_market_cap(value: Decimal) -> str:
    if value >= Decimal("1000000"):
        return f"${value / Decimal('1000000'):.1f}M"
    if value >= Decimal("1000"):
        return f"${value / Decimal('1000'):.0f}K"
    return f"${value:,.0f}"


def _fmt_close_reason(reason: str | None) -> str:
    mapping = {
        "tp_hit": "TP atteint",
        "exit_mc_hit": "MC cible atteinte",
        "manual_close": "fermeture manuelle",
        "bot_stop": "bot arrêté",
        "cancelled": "annulée",
    }
    return mapping.get(reason or "", reason or "fermée")
