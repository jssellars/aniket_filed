import typing

from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendation import \
    FacebookRecommendation
from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnhancerBase import \
    FacebookRecommendationEnhancerBase
from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnum import \
    FacebookRecommendationImportanceEnum, FacebookRecommendationConfidenceEnum, FacebookRecommendationFieldsEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationBuilder import RecommendationBuilder


class FacebookRecommendationEnhancerAdSetLevel(FacebookRecommendationEnhancerBase):
    def __init__(self):
        super().__init__()
        self.set_level(level=LevelEnum.AD)



