"""callback_data constants for inline menu navigation.

All values are below the Telegram 64-byte limit.
Prefix "menu:" for navigation, "act:" for actions requiring confirmation.
"""

MAIN = "menu:main"
COPY_TRADING = "menu:ct"
POSITIONS = "menu:pos"
SETTINGS = "menu:settings"

START_BOT_CONFIRM = "act:sb"
START_BOT_EXEC = "act:sb:ok"

STOP_BOT_CONFIRM = "act:stb"
STOP_BOT_EXEC = "act:stb:ok"

RESET_CONFIRM = "act:rst"
RESET_EXEC = "act:rst:ok"

CANCEL = "act:cancel"
