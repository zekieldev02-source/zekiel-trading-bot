from enum import Enum


class TradingMode(Enum):
    PAPER = "paper"
    AUTO = "auto"
    MANUAL = "manual"
    LIVE = "live"

    @property
    def display(self) -> str:
        labels = {
            TradingMode.PAPER: "📝 Paper",
            TradingMode.AUTO: "🤖 Auto",
            TradingMode.MANUAL: "🖐 Manual",
            TradingMode.LIVE: "💰 Live",
        }
        return labels[self]
