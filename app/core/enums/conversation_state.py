from enum import IntEnum, auto


class ConversationState(IntEnum):
    """Shared conversation states for all ConversationHandlers.

    All config-setting flows follow the same pattern:
    ASK_VALUE → user types value → CONFIRM → user confirms → END
    """

    ASK_VALUE = auto()
    CONFIRM = auto()
