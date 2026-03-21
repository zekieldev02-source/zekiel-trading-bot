# Source of truth: backend (app/core/enums/bot_status.py).
# This local copy is used for display only (Telegram UI labels).
from enum import Enum


class BotStatus(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    STOPPED = "stopped"
    ERROR = "error"

    @property
    def display(self) -> str:
        labels = {
            BotStatus.IDLE: "⏸ Idle",
            BotStatus.ACTIVE: "🟢 Active",
            BotStatus.STOPPED: "🔴 Stopped",
            BotStatus.ERROR: "⚠️ Error",
        }
        return labels[self]
