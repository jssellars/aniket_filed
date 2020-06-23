from enum import Enum


class FacebookRecommendationImportanceEnum(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class FacebookRecommendationConfidenceEnum(Enum):
    LOW = 0.55
    MEDIUM = 0.85
    HIGH = 1

class FacebookRecommendationFieldsEnum(Enum):
    TITLE = 'title'
    MESSAGE = 'message'
    IMPORTANCE = 'importance'
    CONFIDENCE = 'confidence'
    BLAME_FIELD = 'blame_field'