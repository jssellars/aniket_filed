from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnhancerBase import \
    FacebookRecommendationEnhancerBase
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum


class FacebookRecommendationEnhancerAdLevel(FacebookRecommendationEnhancerBase):
    def __init__(self):
        super().__init__()
        self.set_level(level=LevelEnum.AD)