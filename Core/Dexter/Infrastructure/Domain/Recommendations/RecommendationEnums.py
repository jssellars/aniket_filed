from enum import Enum


class RecommendationOptimizationTypeEnum(Enum):
    RULE_BASED = "Rule Based"
    FACEBOOK = 'Facebook'


class RecommendationStatusEnum(Enum):
    ACTIVE = 'active'
    DISMISSED = 'dismissed'
    APPLIED = 'applied'
    DEPRECATED = 'deprecated'

class RecommendationKeysSnakeCase(Enum):
    ID = 'id'
    APPLICATION_DETAILS = 'application_details'
    IMPORTANCE = 'importance'

class RecommendationKeysCamelCase(Enum):
    ID = 'id'
    APPLICATION_DETIALS = 'applicationDetails'
    IMPORTANCE = 'importance'
