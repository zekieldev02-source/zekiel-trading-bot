"""Paper trading position schema."""

from typing import Optional

from pydantic import BaseModel

from app.core.enums.position_status import PositionStatus


class PaperPosition(BaseModel):
    """Represents a simulated position in paper trading mode.

    Created when the bot detects a buy from the tracked wallet
    and the user is in paper mode.
    """

    token_address: str
    entry_price: float
    amount: float
    entry_market_cap: Optional[float] = None
    take_profit_multiplier: Optional[float] = None
    status: PositionStatus = PositionStatus.OPEN
    entry_time: float  # Unix timestamp

    def to_dict(self) -> dict:
        """Serialize for storage in user_data."""
        return {
            "token_address": self.token_address,
            "entry_price": self.entry_price,
            "amount": self.amount,
            "entry_market_cap": self.entry_market_cap,
            "take_profit_multiplier": self.take_profit_multiplier,
            "status": self.status.value,
            "entry_time": self.entry_time,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PaperPosition":
        """Deserialize from user_data storage."""
        data = data.copy()
        data["status"] = PositionStatus(data["status"])
        return cls(**data)
