# 🚀 Zekiel Trading Bot

Bot Telegram de copy trading sur Solana. Interface utilisateur complète en commandes Telegram, conçue pour être connectée ultérieurement à un moteur de trading (FastAPI + Solana + Jupiter).

## Stack

- Python 3.12
- [python-telegram-bot](https://python-telegram-bot.org/) 22.6
- Pydantic / Pydantic Settings
- Architecture modulaire (handlers / services / schemas / enums)

## Installation

```bash
# Cloner le repo
git clone <repo-url>
cd zekiel-trading-bot

# Créer l'environnement virtuel
python3.12 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Configurer le token
cp .env.exemple .env
# Éditer .env et ajouter BOT_TOKEN=<ton_token_telegram>
```

## Lancer le bot

```bash
python run.py
```

---

## Commandes disponibles

### Configuration

| Commande | Description | Type |
|---|---|---|
| `/setwallet` | Définir le wallet Solana à suivre | ConversationHandler |
| `/setamount` | Définir le montant d'entrée (SOL) | ConversationHandler |
| `/settp` | Définir le multiplicateur de take-profit (ex: x2, x1.5) | ConversationHandler |
| `/setentrymc` | Définir le market cap max d'entrée (ex: 500k, 1M) | ConversationHandler |
| `/setexitmc` | Définir le market cap cible de sortie | ConversationHandler |
| `/mode` | Choisir le mode : `/mode paper` ou `/mode live` | CommandHandler |

### Réinitialisation

| Commande | Description |
|---|---|
| `/resetwallet` | Supprimer le wallet suivi |
| `/resetamount` | Supprimer le montant d'entrée |
| `/resettp` | Supprimer le take-profit |
| `/resetentrymc` | Supprimer le MC d'entrée |
| `/resetexitmc` | Supprimer le MC de sortie |
| `/resetall` | Réinitialiser toute la configuration |
| `/reset` | Réinitialisation complète (config + positions) avec confirmation |

### Contrôle

| Commande | Description |
|---|---|
| `/startbot` | Activer le copy trading (requiert wallet + montant) |
| `/stopbot` | Désactiver le copy trading |

### Informations

| Commande | Description |
|---|---|
| `/start` | Accueil + initialisation utilisateur |
| `/help` | Afficher la liste des commandes |
| `/status` | État du bot (mode, config, positions ouvertes) |
| `/settings` | Voir la configuration complète |

---

## Architecture

```
zekiel-trading-bot/
├── run.py                              # Point d'entrée
├── app/
│   ├── bot/
│   │   ├── main.py                     # Build Application + run_polling
│   │   ├── register_handlers.py        # Enregistrement centralisé des handlers
│   │   ├── handlers/
│   │   │   ├── start.py                # /start — accueil + init user_data
│   │   │   ├── help.py                 # /help
│   │   │   ├── status.py              # /status — vue synthétique
│   │   │   ├── settings.py            # /settings — config complète
│   │   │   ├── control.py             # /startbot, /stopbot
│   │   │   ├── wallet.py              # /setwallet (ConversationHandler)
│   │   │   ├── amount.py              # /setamount (ConversationHandler)
│   │   │   ├── take_profit.py         # /settp (ConversationHandler)
│   │   │   ├── market_cap.py          # /setentrymc, /setexitmc
│   │   │   ├── mode.py               # /mode paper | /mode live
│   │   │   ├── reset.py              # /resetwallet..resetall
│   │   │   └── full_reset.py         # /reset (avec confirmation)
│   │   └── messages/
│   │       ├── bot_messages.py        # start, help, control, status, settings
│   │       ├── config_messages.py     # wallet, amount, tp, mc, mode
│   │       ├── reset_messages.py      # individual + full reset
│   │       └── error_messages.py      # cancel, erreurs génériques
│   ├── core/
│   │   ├── config.py                  # Pydantic Settings (BOT_TOKEN, ENV)
│   │   ├── constants.py               # Limites, UserDataKeys
│   │   └── enums/
│   │       ├── bot_status.py          # IDLE, ACTIVE, STOPPED, ERROR
│   │       ├── trading_mode.py        # PAPER, LIVE
│   │       ├── position_status.py     # OPEN, CLOSED, CANCELLED
│   │       └── conversation_state.py  # ASK_VALUE, CONFIRM
│   ├── schemas/
│   │   ├── user_config.py             # Config utilisateur complète
│   │   └── paper_position.py          # Position simulée (paper trading)
│   └── services/
│       └── user_config_service.py     # Logique métier centralisée
├── requirements.txt
├── .env
└── .env.exemple
```

## Principes d'architecture

### Séparation des responsabilités

- **Handlers** → réception des commandes Telegram, orchestration du flux
- **Messages** → tous les textes externalisés (aucun texte hardcodé dans les handlers)
- **Services** → logique métier (validation, stockage, règles d'activation)
- **Schemas** → modèles Pydantic pour la validation des données
- **Enums** → valeurs contrôlées dans `core/enums/`
- **Constants** → limites et clés centralisées (pas de magic strings)

### Stockage MVP

Tout est stocké dans `context.user_data` (dict en mémoire par utilisateur, fourni par python-telegram-bot). Prévu pour migrer vers Redis/PostgreSQL via un adapter de persistance.

### Structure utilisateur

Chaque utilisateur possède la structure suivante dans `user_data` :

| Clé | Type | Défaut | Description |
|---|---|---|---|
| `telegram_id` | `int` | — | ID Telegram de l'utilisateur |
| `wallet_address` | `str \| None` | `None` | Wallet Solana suivi |
| `trading_wallet_public_key` | `str \| None` | `None` | Wallet de trading (futur) |
| `trade_amount` | `float \| None` | `None` | Montant engagé par trade (SOL) |
| `tp_multiplier` | `float \| None` | `None` | Multiplicateur take-profit |
| `entry_market_cap` | `float \| None` | `None` | MC max d'entrée (USD) |
| `exit_market_cap` | `float \| None` | `None` | MC cible de sortie (USD) |
| `mode` | `str` | `"paper"` | Mode de trading |
| `bot_active` | `bool` | `False` | Copy trading actif ou non |
| `positions` | `list[dict]` | `[]` | Positions paper simulées |

### Paper Position

| Champ | Type | Description |
|---|---|---|
| `token_address` | `str` | Adresse du token |
| `entry_price` | `float` | Prix d'entrée |
| `amount` | `float` | Montant engagé (SOL) |
| `entry_market_cap` | `float \| None` | MC au moment de l'entrée |
| `take_profit_multiplier` | `float \| None` | TP configuré à l'entrée |
| `status` | `str` | `open`, `closed`, `cancelled` |
| `entry_time` | `float` | Timestamp Unix de l'entrée |

---

## Validations

| Paramètre | Règles |
|---|---|
| Wallet Solana | Base58, 32-44 caractères |
| Montant | 0.001 – 100 SOL |
| Take-profit | ≥ 1.01, ≤ 100 |
| MC d'entrée | $1,000 – $100M (supporte `500k`, `1M`) |
| MC de sortie | $1,000 – $1B (supporte `500k`, `5M`) |

## Règles métier

- **`/startbot`** requiert au minimum : wallet + montant configurés
- **Changement de mode** → le bot est automatiquement désactivé par sécurité
- **Reset du wallet ou du montant** → le bot est automatiquement désactivé (paramètres obligatoires)
- **`/reset`** → nécessite de taper `oui` pour confirmer, réinitialise tout mais préserve le `telegram_id`
- **Tous les utilisateurs** démarrent en mode **Paper Trading** par défaut

---

## Prochaines étapes prévues

- [ ] Connexion au backend FastAPI
- [ ] Détection des trades du wallet suivi (Solana WebSocket)
- [ ] Exécution réelle des trades via Jupiter
- [ ] Persistance Redis / PostgreSQL
- [ ] Boutons inline et menus avancés
- [ ] Commandes `/positions`, `/syncposition`
- [ ] Notifications temps réel