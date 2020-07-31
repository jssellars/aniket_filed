from Core.Dexter.Infrastructure.Domain.Rules.RuleEnums import RuleDataFieldTypeBaseEnum, RuleImportanceEnumBase, \
    RuleTypeEnumBase, RuleSourceEnumBase, RuleCategoryEnumBase, RuleRedirectEnumBase


# class GoogleRuleDataFieldTypeEnum(RuleDataFieldTypeBaseEnum):
#     AVERAGE = 1
#     TREND = 2
#     RAW_DATA = 3
#     STRUCTURE = 4


class GoogleRuleImportanceEnum(RuleImportanceEnumBase):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class GoogleRuleTypeEnum(RuleTypeEnumBase):
    AUDIENCE = "Audience"
    BUDGET_AND_BID = "Budget & Bid"
    CREATIVE = "Creative"
    PERFORMANCE = 'Performance'
    PLACEMENT_AND_DEVICE = "Placement & Device"


class GoogleRuleSourceEnum(RuleSourceEnumBase):
    DEXTER = "Dexter"
    GOOGLE = "Google"


class GoogleRuleCategoryEnum(RuleCategoryEnumBase):
    IMPROVE_CPR = "cpr"
    IMPROVE_CPC = "cpc"
    IMPROVE_CTR = "ctr"
    IMPROVE_ROAS = "roas"
    IMPROVE_CONVERSION_RATE = "conversion_rate"
    IMPROVE_ENGAGEMENT = "engagement"
    OPTIMIZE_TARGETING = "targeting"
    OPTIMIZE_BUDGET = "budget"


class GoogleRuleRedirectEnum(RuleRedirectEnumBase):
    CAMPAIGN_MANAGER = 1
    CREATE = 2  # ads manager - campaign level
    EDIT_STRUCTURE = 3
    CREATE_PIXEL = 4
    CREATE_LOOKALIKE_AUDIENCE = 5
    CREATE_RETARGETING_AUDIENCE = 6
