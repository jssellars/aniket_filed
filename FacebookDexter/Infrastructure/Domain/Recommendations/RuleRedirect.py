from enum import Enum


class RuleRedirectEnum(Enum):
    CAMPAIGN_MANAGER = 1
    CREATE = 2  # ads manager - campaign level
    EDIT_STRUCTURE = 3
    CREATE_PIXEL = 4
    CREATE_LOOKALIKE_AUDIENCE = 5
    CREATE_RETARGETING_AUDIENCE = 6
    DUPLICATE = 7
