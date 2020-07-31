from Core.Dexter.Infrastructure.Domain.Rules.RuleEnums import RuleSourceEnumBase, RuleTypeEnumBase, \
    RuleCategoryEnumBase, RuleRedirectEnumBase, RuleTypeSelectionEnumBase, RuleImportanceEnumBase


class FacebookRuleTypeEnum(RuleTypeEnumBase):
    AUDIENCE = "Audience"
    BUDGET_AND_BID = "Budget & Bid"
    CREATIVE = "Creative"
    PERFORMANCE = 'Performance'
    PLACEMENT_AND_DEVICE = "Placement & Device"


class FacebookRuleSourceEnum(RuleSourceEnumBase):
    FACEBOOK = "Facebook"
    DEXTER = "Dexter"


class FacebookRuleImportanceEnum(RuleImportanceEnumBase):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class FacebookRuleCategoryEnum(RuleCategoryEnumBase):
    IMPROVE_CPR = "cpr"
    IMPROVE_CPC = "cpc"
    IMPROVE_CTR = "ctr"
    IMPROVE_ROAS = "roas"
    IMPROVE_CONVERSION_RATE = "conversion_rate"
    IMPROVE_ENGAGEMENT = "engagement"
    OPTIMIZE_TARGETING = "targeting"
    OPTIMIZE_BUDGET = "budget"


class FacebookRuleRedirectEnum(RuleRedirectEnumBase):
    CAMPAIGN_MANAGER = 1
    CREATE = 2  # ads manager - campaign level
    EDIT_STRUCTURE = 3
    CREATE_PIXEL = 4
    CREATE_LOOKALIKE_AUDIENCE = 5
    CREATE_RETARGETING_AUDIENCE = 6
    DUPLICATE = 7


class FacebookRuleTypeSelectionEnum(RuleTypeSelectionEnumBase):
    REMOVE_BREAKDOWN = 0
    GENERAL = 1
    BUDGET = 2
    PAUSE = 3
    CREATE = 4
