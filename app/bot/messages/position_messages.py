"""Messages for the /positions command."""

from decimal import Decimal, InvalidOperation

from telegram.helpers import escape_markdown

# The backend returns all closed positions sorted. Display limiting is done client-side.
MAX_CLOSED_DISPLAY = 3


NO_POSITIONS_MESSAGE = (
    "📊 *Positions paper*\n"
    "\n"
    "Tu n'as pas encore de positions paper.\n"
    "Le bot en créera automatiquement quand un signal sera détecté."
)


def get_positions_message(data: dict) -> str:
    """Builds the Telegram message from the /positions/summary response.

    Handles all cases cleanly:
    - open positions only
    - closed positions only
    - mix of both

    Dynamic values (token_symbol, token_address, close_reason) are always
    escaped to prevent Markdown rendering bugs.

    Args:
        data: dict containing open_positions, closed_positions and summary.

    Returns:
        Message formatted in Markdown v1 for Telegram.
    """
    summary = data.get("summary", {})
    open_positions: list[dict] = data.get("open_positions", [])
    closed_positions: list[dict] = data.get("closed_positions", [])

    open_count: int = summary.get("open_count", 0)
    closed_count: int = summary.get("closed_count", 0)

    lines = ["📊 *Positions paper*", ""]

    lines.append(f"🟢 Ouvertes : {open_count}")
    lines.append(f"🔴 Fermées : {closed_count}")

    if closed_count > 0:
        total_pnl = _to_decimal(summary.get("total_pnl_absolute", 0))
        avg_pnl = _to_decimal(summary.get("average_pnl_percent", 0))
        pnl_sign = "+" if total_pnl >= 0 else ""
        avg_sign = "+" if avg_pnl >= 0 else ""
        lines.append(f"💰 PnL total : {pnl_sign}{total_pnl:.4f} SOL")
        lines.append(f"📈 PnL moyen : {avg_sign}{avg_pnl:.2f}%")

    lines.append("")
    if open_positions:
        lines.append("*Positions ouvertes :*")
        for i, pos in enumerate(open_positions, start=1):
            symbol = _safe_md(pos.get("token_symbol") or pos.get("token_address", "?"))
            addr = pos.get("token_address") or ""
            lines.append("")
            lines.append(f"{i}. *{symbol}*")
            if addr:
                lines.append(f"   Adresse : `{addr}`")
            lines.append(f"   Entrée : `{_fmt_price(pos.get('entry_price'))}` SOL")
            lines.append(f"   Montant : `{_fmt_amount(pos.get('amount'))}` SOL")

            tp = pos.get("take_profit_multiplier")
            if tp:
                lines.append(f"   TP : x{_to_decimal(tp):.2f}")

            mc = pos.get("entry_market_cap")
            if mc:
                lines.append(f"   MC d'entrée : {_fmt_market_cap(_to_decimal(mc))}")
    else:
        lines.append("_Aucune position ouverte pour le moment._")

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


def get_close_confirmation_message(position_data: dict) -> str:
    """Builds the confirmation message after a manual position close.

    Args:
        position_data: dict returned by the backend after closing (ClosePositionResponse).

    Returns:
        Message formatted in Markdown v1 for Telegram.
    """
    addr = str(position_data.get("token_address") or "")
    symbol = _safe_md(position_data.get("token_symbol") or _short_addr(addr) or "?")
    lines = [
        "🔴 *Position fermée*",
        "",
        f"Token : *{symbol}*",
    ]
    if addr:
        lines.append(f"Adresse : `{addr}`")
    lines.append("Raison : fermeture manuelle")

    pnl_abs = position_data.get("pnl_absolute")
    pnl_pct = position_data.get("pnl_percent")

    if pnl_abs is not None and pnl_pct is not None:
        pnl_d = _to_decimal(pnl_abs)
        pct_d = _to_decimal(pnl_pct)
        sign = "+" if pnl_d >= 0 else ""
        lines.append(f"PnL : `{sign}{pct_d:.2f}%`")
        lines.append(f"Résultat : `{sign}{pnl_d:.4f} SOL`")

    return "\n".join(lines)


def _short_addr(address: str) -> str:
    """Returns a short address for display: `So11...1112`."""
    if len(address) <= 10:
        return address
    return f"{address[:4]}...{address[-4:]}"


def _safe_md(text: str) -> str:
    """Escapes Markdown v1 special characters for Telegram (*_`[).

    Must be applied to all dynamic values injected into messages:
    token_symbol, token_address, close_reason, etc.
    """
    return escape_markdown(str(text), version=1)


def _to_decimal(value) -> Decimal:
    """Converts any numeric value (float, str, int) to Decimal via str() to avoid
    float precision issues. e.g. Decimal(str(0.1 + 0.2)) == Decimal("0.3").
    """
    try:
        return Decimal(str(value))
    except (InvalidOperation, TypeError):
        return Decimal("0")


def _fmt_price(value) -> str:
    """Formats a token price with precision adapted to its magnitude.

    Uses Decimal to avoid float imprecision on very small prices
    (e.g. Solana tokens at 0.000000001 SOL).
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
        "exit_mc_hit": "MC de sortie atteinte",
        "manual_close": "fermeture manuelle",
        "bot_stop": "bot arrêté",
        "cancelled": "annulé",
    }
    return mapping.get(reason or "", reason or "fermé")
