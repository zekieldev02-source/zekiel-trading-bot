# Source of truth: backend (app/core/enums/trading_mode.py).
# This local copy is used for display only (Telegram UI labels).
from enum import Enum


class TradingMode(Enum):
    PAPER = "paper"
    LIVE = "live"

    @property
    def display(self) -> str:
        labels = {
            TradingMode.PAPER: "📝 Paper Trading",
            TradingMode.LIVE: "💰 Live Trading",
        }
        return labels[self]
