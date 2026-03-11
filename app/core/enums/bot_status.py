"""Bot operational status enum."""

from enum import Enum


class BotStatus(Enum):
    """High-level operational state of the copy trading bot."""

    IDLE = "idle"
    ACTIVE = "active"
    STOPPED = "stopped"
    ERROR = "error"

    @property
    def display(self) -> str:
        labels = {
            BotStatus.IDLE: "⏸ En attente",
            BotStatus.ACTIVE: "🟢 Actif",
            BotStatus.STOPPED: "🔴 Arrêté",
            BotStatus.ERROR: "⚠️ Erreur",
        }
        return labels[self]
