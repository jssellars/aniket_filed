from enum import Enum


class RecommendationOptimizationTypeEnum(Enum):
    RULE_BASED = "Rule Based"
    FACEBOOK = 'Facebook'


class RecommendationStatusEnum(Enum):
    ACTIVE = 'active'
    DISMISSED = 'dismissed'
    APPLIED = 'applied'
    DEPRECATED = 'deprecated'

