from app.bot.enums.status import BotStatus


def get_status_message(status: BotStatus) -> str:
    return f"""
**État du Bot**

Statut : {status.value}

Mode : Trading inactif
Paires suivies : Aucune
Solde : Non connecté
"""