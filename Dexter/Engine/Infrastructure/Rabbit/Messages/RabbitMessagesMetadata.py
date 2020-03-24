from enum import Enum


class MessageTypes(Enum):
    ALTER_BUDGET = "GetBudgetRecommendationMessageResponse"
    STOP = "GetStopRecommendationMessageResponse"
    START = "GetStartRecommendationMessageResponse"
    REMOVE_BD = "GetRemoveBreakdownRecommendationMessageResponse"
    SPLIT_STRUCTURE = "GetSplitStructureRecommendationMessageResponse"
    SPLIT_BD = "GetSplitBreakdownRecommendationMessageResponse"
    OPTIMIZATION_RULE = "GetRuleBasedRecommendationMessageResponse"
    FACEBOOK_RECOMMENDATION = "GetFacebookRecommendationMessageResponse"


class FacebookRecommendationMessageFieldNames(Enum):
    TEMPLATE = "template"


class OptimizationRuleMessageFieldNames(Enum):
    TEMPLATE = "template"


class StandardMessageFieldNames(Enum):
    ID = "id"
    LEVEL = "level"
    OPTIMIZATION_TYPE = "optimization_type"
    RECOMMENDATION_TYPE = "recommendation_type"
    CONFIDENCE = "confidence"
    IMPORTANCE = "importance"
    SOURCE = "source"


class BudgetMessageFieldNames(Enum):
    VALUE = "value"
    FLUCTUATION_VALUE = "fluctuation_value"
    EFFECT = "effect"


class RemoveBDMessageFieldNames(Enum):
    BREAKDOWN_TYPE = "breakdown_type"
    BREAKDOWN_IDS = "breakdowns"


class SplitStructureMessageFieldNames(Enum):
    VALUES = "values"


# TODO: We should rename the properties of this to SNAKE_CASE
class Recommendation(object):
    structureId = None
    level = None
    optimizationType = None
    recommendationType = None
    confidence = None
    importance = None
    source = None
    campaignId = None
    parentId = None
    adAccountId = None
    createdAt = None
    template = None
    metric = None
    applicationDetails = None
    structureName = None
    campaignName = None
    parentName = None
    channel = None
