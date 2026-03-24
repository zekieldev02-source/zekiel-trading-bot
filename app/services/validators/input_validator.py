import re

from app.core.constants import (
    MAX_ENTRY_MARKET_CAP,
    MAX_EXIT_MARKET_CAP,
    MAX_STOP_LOSS,
    MAX_TP_MULTIPLIER,
    MAX_TRADE_AMOUNT,
    MIN_MARKET_CAP,
    MIN_STOP_LOSS,
    MIN_TP_MULTIPLIER,
    MIN_TRADE_AMOUNT,
    SOLANA_ADDRESS_MAX_LENGTH,
    SOLANA_ADDRESS_MIN_LENGTH,
    SOLANA_BASE58_CHARS,
)

_SOLANA_REGEX = re.compile(
    f"^[{re.escape(SOLANA_BASE58_CHARS)}]"
    f"{{{SOLANA_ADDRESS_MIN_LENGTH},{SOLANA_ADDRESS_MAX_LENGTH}}}$"
)


def validate_wallet(address: str) -> tuple[bool, str]:
    address = address.strip()
    if not _SOLANA_REGEX.match(address):
        return False, (
            "Invalid address. A Solana address must contain "
            f"between {SOLANA_ADDRESS_MIN_LENGTH} and {SOLANA_ADDRESS_MAX_LENGTH} "
            "alphanumeric characters (base58)."
        )
    return True, ""


def validate_amount(raw: str) -> tuple[bool, float | None, str]:
    try:
        amount = float(raw.strip())
    except ValueError:
        return False, None, "Please enter a valid number."

    if amount < MIN_TRADE_AMOUNT:
        return False, None, f"Minimum amount is {MIN_TRADE_AMOUNT} SOL."
    if amount > MAX_TRADE_AMOUNT:
        return False, None, f"Maximum amount is {MAX_TRADE_AMOUNT} SOL."
    return True, amount, ""


def validate_tp_multiplier(raw: str) -> tuple[bool, float | None, str]:
    cleaned = raw.strip().lower().lstrip("x")
    try:
        multiplier = float(cleaned)
    except ValueError:
        return False, None, "Please enter a valid multiplier (e.g. 2, 1.5, x3)."

    if multiplier < MIN_TP_MULTIPLIER:
        return False, None, f"Minimum multiplier is {MIN_TP_MULTIPLIER}."
    if multiplier > MAX_TP_MULTIPLIER:
        return False, None, f"Maximum multiplier is {MAX_TP_MULTIPLIER}."
    return True, multiplier, ""


def validate_stop_loss(raw: str) -> tuple[bool, float | None, str]:
    cleaned = raw.strip().replace("%", "")
    try:
        value = float(cleaned)
    except ValueError:
        return False, None, "Please enter a valid percentage (e.g. 50, 25, 0.5)."

    if value > 1:
        value = value / 100.0

    if value < MIN_STOP_LOSS:
        return False, None, f"Minimum stop-loss is {MIN_STOP_LOSS * 100:.0f}%."
    if value > MAX_STOP_LOSS:
        return False, None, f"Maximum stop-loss is {MAX_STOP_LOSS * 100:.0f}%."
    return True, value, ""


def validate_market_cap(raw: str, is_entry: bool = True) -> tuple[bool, float | None, str]:
    cleaned = raw.strip().replace(",", "").replace(" ", "")

    multiplier = 1
    if cleaned[-1:].lower() == "k":
        multiplier = 1_000
        cleaned = cleaned[:-1]
    elif cleaned[-1:].lower() == "m":
        multiplier = 1_000_000
        cleaned = cleaned[:-1]

    try:
        value = float(cleaned) * multiplier
    except ValueError:
        return False, None, "Please enter a valid number (e.g. 500000, 500k, 1M)."

    max_cap = MAX_ENTRY_MARKET_CAP if is_entry else MAX_EXIT_MARKET_CAP

    if value < MIN_MARKET_CAP:
        return False, None, f"Minimum market cap is ${MIN_MARKET_CAP:,.0f}."
    if value > max_cap:
        return False, None, f"Maximum market cap is ${max_cap:,.0f}."
    return True, value, ""
