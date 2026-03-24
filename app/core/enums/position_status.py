from enum import Enum


class PositionStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"

    @property
    def display(self) -> str:
        labels = {
            PositionStatus.OPEN: "🟢 Open",
            PositionStatus.CLOSED: "🔴 Closed",
            PositionStatus.CANCELLED: "⚪ Cancelled",
        }
        return labels[self]
