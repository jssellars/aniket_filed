from enum import Enum


class RecommendationOptimizationTypeEnum(Enum):
    RULE_BASED = "Rule Based"
    FACEBOOK = 'Facebook'


class RecommendationStatusEnum(Enum):
    DEPRECATED = 0
    ACTIVE = 1
