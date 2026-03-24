"""Represents the full configuration of a user.

Used for validation/serialization. The source of truth at MVP
is context.user_data (in-memory dict).
"""

from typing import Optional

from pydantic import BaseModel

from app.core.enums.trading_mode import TradingMode


class UserConfig(BaseModel):
    telegram_id: Optional[int] = None
    wallet_address: Optional[str] = None
    trading_wallet_public_key: Optional[str] = None
    trade_amount: Optional[float] = None
    tp_multiplier: Optional[float] = None
    stop_loss_multiplier: Optional[float] = None
    entry_market_cap: Optional[float] = None
    exit_market_cap: Optional[float] = None
    mode: TradingMode = TradingMode.PAPER
    bot_active: bool = False
    positions: list = []

    @property
    def is_ready_to_trade(self) -> bool:
        """Minimum config required: wallet + trade amount."""
        return self.wallet_address is not None and self.trade_amount is not None
