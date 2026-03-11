"""Position lifecycle status for paper trading."""

from enum import Enum


class PositionStatus(Enum):
    """Tracks whether a paper position is active, closed at profit, or cancelled."""

    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"

    @property
    def display(self) -> str:
        labels = {
            PositionStatus.OPEN: "🟢 Ouverte",
            PositionStatus.CLOSED: "🔴 Fermée",
            PositionStatus.CANCELLED: "⚪ Annulée",
        }
        return labels[self]
