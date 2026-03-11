"""Application-wide constants and default values."""

SOLANA_ADDRESS_MIN_LENGTH = 32
SOLANA_ADDRESS_MAX_LENGTH = 44
SOLANA_BASE58_CHARS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

MIN_TRADE_AMOUNT = 0.001
MAX_TRADE_AMOUNT = 100.0
DEFAULT_TRADE_AMOUNT = None

MIN_TP_MULTIPLIER = 1.01
MAX_TP_MULTIPLIER = 100.0
DEFAULT_TP_MULTIPLIER = None

MIN_MARKET_CAP = 1_000
MAX_ENTRY_MARKET_CAP = 100_000_000
MAX_EXIT_MARKET_CAP = 1_000_000_000
DEFAULT_ENTRY_MARKET_CAP = None
DEFAULT_EXIT_MARKET_CAP = None


class UserDataKeys:
    """Keys used in context.user_data (in-memory dict per user)."""

    TELEGRAM_ID = "telegram_id"
    WALLET_ADDRESS = "wallet_address"
    TRADING_WALLET_PUBLIC_KEY = "trading_wallet_public_key"
    TRADE_AMOUNT = "trade_amount"
    TP_MULTIPLIER = "tp_multiplier"
    ENTRY_MARKET_CAP = "entry_market_cap"
    EXIT_MARKET_CAP = "exit_market_cap"
    MODE = "mode"
    BOT_ACTIVE = "bot_active"
    POSITIONS = "positions"
