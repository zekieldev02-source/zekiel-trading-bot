"""Trading mode enum: paper (simulated) or live (real transactions)."""

from enum import Enum


class TradingMode(Enum):
    """Determines whether trades are simulated or executed on-chain."""

    PAPER = "paper"
    LIVE = "live"

    @property
    def display(self) -> str:
        labels = {
            TradingMode.PAPER: "📝 Paper Trading",
            TradingMode.LIVE: "💰 Live Trading",
        }
        return labels[self]
