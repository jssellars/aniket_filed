from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnum import \
    FacebookRecommendationConfidenceEnum, FacebookRecommendationImportanceEnum


class FacebookRecommendation:
    blame_field: str = None
    code: int = None
    confidence: FacebookRecommendationConfidenceEnum = None
    importance: FacebookRecommendationImportanceEnum = None
    message: str = None
    title: str = None
