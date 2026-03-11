"""Service layer for user configuration management.

All user config is stored in context.user_data (in-memory dict) for the MVP.
This service centralizes all read/write logic so the storage backend can be
swapped later (Redis, PostgreSQL) without touching any handler code.
"""

import re

from app.core.constants import (
    MAX_ENTRY_MARKET_CAP,
    MAX_EXIT_MARKET_CAP,
    MAX_TP_MULTIPLIER,
    MAX_TRADE_AMOUNT,
    MIN_MARKET_CAP,
    MIN_TP_MULTIPLIER,
    MIN_TRADE_AMOUNT,
    SOLANA_ADDRESS_MAX_LENGTH,
    SOLANA_ADDRESS_MIN_LENGTH,
    SOLANA_BASE58_CHARS,
    UserDataKeys,
)
from app.core.enums.trading_mode import TradingMode
from app.schemas.user_config import UserConfig


_SOLANA_REGEX = re.compile(
    f"^[{re.escape(SOLANA_BASE58_CHARS)}]"
    f"{{{SOLANA_ADDRESS_MIN_LENGTH},{SOLANA_ADDRESS_MAX_LENGTH}}}$"
)


class UserConfigService:
    """Stateless service — every method takes user_data dict as first arg."""

    @staticmethod
    def init_user_data(user_data: dict, telegram_id: int | None = None) -> None:
        """Populate default keys if missing (idempotent).

        If telegram_id is provided, it always overwrites the stored value
        to stay in sync with the Telegram API.
        """
        defaults = {
            UserDataKeys.TELEGRAM_ID: telegram_id,
            UserDataKeys.WALLET_ADDRESS: None,
            UserDataKeys.TRADING_WALLET_PUBLIC_KEY: None,
            UserDataKeys.TRADE_AMOUNT: None,
            UserDataKeys.TP_MULTIPLIER: None,
            UserDataKeys.ENTRY_MARKET_CAP: None,
            UserDataKeys.EXIT_MARKET_CAP: None,
            UserDataKeys.MODE: TradingMode.PAPER.value,
            UserDataKeys.BOT_ACTIVE: False,
            UserDataKeys.POSITIONS: [],
        }
        for key, value in defaults.items():
            user_data.setdefault(key, value)
        if telegram_id is not None:
            user_data[UserDataKeys.TELEGRAM_ID] = telegram_id

    @staticmethod
    def get_config(user_data: dict) -> UserConfig:
        """Build a validated UserConfig from the raw user_data dict."""
        mode_value = user_data.get(UserDataKeys.MODE, TradingMode.PAPER.value)
        return UserConfig(
            telegram_id=user_data.get(UserDataKeys.TELEGRAM_ID),
            wallet_address=user_data.get(UserDataKeys.WALLET_ADDRESS),
            trading_wallet_public_key=user_data.get(UserDataKeys.TRADING_WALLET_PUBLIC_KEY),
            trade_amount=user_data.get(UserDataKeys.TRADE_AMOUNT),
            tp_multiplier=user_data.get(UserDataKeys.TP_MULTIPLIER),
            entry_market_cap=user_data.get(UserDataKeys.ENTRY_MARKET_CAP),
            exit_market_cap=user_data.get(UserDataKeys.EXIT_MARKET_CAP),
            mode=TradingMode(mode_value),
            bot_active=user_data.get(UserDataKeys.BOT_ACTIVE, False),
            positions=user_data.get(UserDataKeys.POSITIONS, []),
        )

    @staticmethod
    def is_config_complete(user_data: dict) -> bool:
        """Check minimum requirements to start copying trades (wallet + amount)."""
        return (
            user_data.get(UserDataKeys.WALLET_ADDRESS) is not None
            and user_data.get(UserDataKeys.TRADE_AMOUNT) is not None
        )

    @staticmethod
    def validate_wallet(address: str) -> tuple[bool, str]:
        """Return (is_valid, error_message)."""
        address = address.strip()
        if not _SOLANA_REGEX.match(address):
            return False, (
                "Adresse invalide. Une adresse Solana doit contenir "
                f"entre {SOLANA_ADDRESS_MIN_LENGTH} et {SOLANA_ADDRESS_MAX_LENGTH} "
                "caractères alphanumériques (base58)."
            )
        return True, ""

    @staticmethod
    def validate_amount(raw: str) -> tuple[bool, float | None, str]:
        """Return (is_valid, parsed_value, error_message)."""
        try:
            amount = float(raw.strip())
        except ValueError:
            return False, None, "Veuillez entrer un nombre valide."

        if amount < MIN_TRADE_AMOUNT:
            return False, None, f"Le montant minimum est {MIN_TRADE_AMOUNT} SOL."
        if amount > MAX_TRADE_AMOUNT:
            return False, None, f"Le montant maximum est {MAX_TRADE_AMOUNT} SOL."
        return True, amount, ""

    @staticmethod
    def validate_tp_multiplier(raw: str) -> tuple[bool, float | None, str]:
        """Return (is_valid, parsed_value, error_message)."""
        cleaned = raw.strip().lower().lstrip("x")
        try:
            multiplier = float(cleaned)
        except ValueError:
            return False, None, "Veuillez entrer un multiplicateur valide (ex: 2, 1.5, x3)."

        if multiplier < MIN_TP_MULTIPLIER:
            return False, None, f"Le multiplicateur minimum est {MIN_TP_MULTIPLIER}."
        if multiplier > MAX_TP_MULTIPLIER:
            return False, None, f"Le multiplicateur maximum est {MAX_TP_MULTIPLIER}."
        return True, multiplier, ""

    @staticmethod
    def validate_market_cap(raw: str, is_entry: bool = True) -> tuple[bool, float | None, str]:
        """Parse and validate a market cap value. Supports shorthand (500k, 1M)."""
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
            return False, None, "Veuillez entrer un nombre valide (ex: 500000, 500k, 1M)."

        max_cap = MAX_ENTRY_MARKET_CAP if is_entry else MAX_EXIT_MARKET_CAP

        if value < MIN_MARKET_CAP:
            return False, None, f"Le market cap minimum est ${MIN_MARKET_CAP:,.0f}."
        if value > max_cap:
            return False, None, f"Le market cap maximum est ${max_cap:,.0f}."
        return True, value, ""

    @staticmethod
    def set_wallet(user_data: dict, address: str) -> None:
        user_data[UserDataKeys.WALLET_ADDRESS] = address.strip()

    @staticmethod
    def set_amount(user_data: dict, amount: float) -> None:
        user_data[UserDataKeys.TRADE_AMOUNT] = amount

    @staticmethod
    def set_take_profit(user_data: dict, multiplier: float) -> None:
        user_data[UserDataKeys.TP_MULTIPLIER] = multiplier

    @staticmethod
    def set_entry_market_cap(user_data: dict, value: float) -> None:
        user_data[UserDataKeys.ENTRY_MARKET_CAP] = value

    @staticmethod
    def set_exit_market_cap(user_data: dict, value: float) -> None:
        user_data[UserDataKeys.EXIT_MARKET_CAP] = value

    @staticmethod
    def set_mode(user_data: dict, mode: TradingMode) -> None:
        """Switch trading mode. Deactivates bot to prevent unintended trades."""
        user_data[UserDataKeys.MODE] = mode.value
        user_data[UserDataKeys.BOT_ACTIVE] = False

    @staticmethod
    def get_mode(user_data: dict) -> TradingMode:
        return TradingMode(user_data.get(UserDataKeys.MODE, TradingMode.PAPER.value))

    @staticmethod
    def activate(user_data: dict) -> tuple[bool, str]:
        """Activate copy trading.

        Requires wallet and trade amount to be configured.
        Returns (success, error_message).
        """
        if not user_data.get(UserDataKeys.WALLET_ADDRESS):
            return False, "❌ Veuillez d'abord configurer un wallet avec /setwallet"
        if not user_data.get(UserDataKeys.TRADE_AMOUNT):
            return False, "❌ Veuillez d'abord configurer un montant avec /setamount"
        user_data[UserDataKeys.BOT_ACTIVE] = True
        return True, ""

    @staticmethod
    def deactivate(user_data: dict) -> None:
        user_data[UserDataKeys.BOT_ACTIVE] = False

    @staticmethod
    def reset_wallet(user_data: dict) -> None:
        """Remove the wallet. Deactivates bot since wallet is mandatory."""
        user_data[UserDataKeys.WALLET_ADDRESS] = None
        user_data[UserDataKeys.BOT_ACTIVE] = False

    @staticmethod
    def reset_amount(user_data: dict) -> None:
        """Remove the trade amount. Deactivates bot since amount is mandatory."""
        user_data[UserDataKeys.TRADE_AMOUNT] = None
        user_data[UserDataKeys.BOT_ACTIVE] = False

    @staticmethod
    def reset_take_profit(user_data: dict) -> None:
        user_data[UserDataKeys.TP_MULTIPLIER] = None

    @staticmethod
    def reset_entry_market_cap(user_data: dict) -> None:
        user_data[UserDataKeys.ENTRY_MARKET_CAP] = None

    @staticmethod
    def reset_exit_market_cap(user_data: dict) -> None:
        user_data[UserDataKeys.EXIT_MARKET_CAP] = None

    @staticmethod
    def reset_all(user_data: dict) -> None:
        """Reset all config fields to defaults. Does not clear positions."""
        user_data[UserDataKeys.WALLET_ADDRESS] = None
        user_data[UserDataKeys.TRADING_WALLET_PUBLIC_KEY] = None
        user_data[UserDataKeys.TRADE_AMOUNT] = None
        user_data[UserDataKeys.TP_MULTIPLIER] = None
        user_data[UserDataKeys.ENTRY_MARKET_CAP] = None
        user_data[UserDataKeys.EXIT_MARKET_CAP] = None
        user_data[UserDataKeys.BOT_ACTIVE] = False

    @staticmethod
    def full_reset(user_data: dict) -> None:
        """Wipe everything: config, positions, mode. Only telegram_id is preserved."""
        telegram_id = user_data.get(UserDataKeys.TELEGRAM_ID)
        user_data.clear()
        UserConfigService.init_user_data(user_data, telegram_id=telegram_id)

    @staticmethod
    def get_positions(user_data: dict) -> list[dict]:
        """Return the list of paper positions."""
        return user_data.get(UserDataKeys.POSITIONS, [])

    @staticmethod
    def get_open_positions(user_data: dict) -> list[dict]:
        """Return only open positions."""
        return [
            p for p in user_data.get(UserDataKeys.POSITIONS, [])
            if p.get("status") == "open"
        ]

    @staticmethod
    def add_position(user_data: dict, position_dict: dict) -> None:
        """Append a paper position to the user's list."""
        positions = user_data.get(UserDataKeys.POSITIONS, [])
        positions.append(position_dict)
        user_data[UserDataKeys.POSITIONS] = positions

    @staticmethod
    def clear_positions(user_data: dict) -> None:
        """Remove all positions."""
        user_data[UserDataKeys.POSITIONS] = []
