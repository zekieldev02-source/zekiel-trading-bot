from enum import Enum


class BotStatus(Enum):
    RUNNING = "En ligne"
    STOPPED = "Arrêté"
    MAINTENANCE = "Maintenance"
    TRADING = "En cours de trading"
    ERROR = "Erreur"
