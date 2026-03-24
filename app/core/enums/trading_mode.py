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
