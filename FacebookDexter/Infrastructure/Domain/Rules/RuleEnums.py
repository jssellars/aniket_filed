from enum import Enum


class RuleDataFieldTypeEnum(Enum):
    AVERAGE = 1
    TREND = 2
    RAW_DATA = 3
    STRUCTURE = 4


class RuleImportanceEnum(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class RuleTypeEnum(Enum):
    AUDIENCE = "Audience"
    BUDGET_AND_BID = "Budget & Bid"
    CREATIVE = "Creative"
    PERFORMANCE = 'Performance'
    PLACEMENT_AND_DEVICE = "Placement & Device"


class RuleSourceEnum(Enum):
    DEXTER = "Dexter"
    FACEBOOK = "Facebook"
    GOOGLE = "Google"


class RuleCategoryEnum(Enum):
    IMPROVE_CPR = "cpr"
    IMPROVE_CPC = "cpc"
    IMPROVE_CTR = "ctr"
    IMPROVE_ROAS = "roas"
    IMPROVE_CONVERSION_RATE = "conversion_rate"
    IMPROVE_ENGAGEMENT = "engagement"
    OPTIMIZE_TARGETING = "audience"
    OPTIMIZE_BUDGET = "budget"


class RuleRedirectEnum(Enum):
    CAMPAIGN_MANAGER = 1
    CREATE = 2  # ads manager - campaign level
    EDIT_STRUCTURE = 3
    CREATE_PIXEL = 4
    CREATE_LOOKALIKE_AUDIENCE = 5
    CREATE_RETARGETING_AUDIENCE = 6
