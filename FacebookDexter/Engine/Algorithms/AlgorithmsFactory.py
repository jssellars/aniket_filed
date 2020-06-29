import typing

from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnhancerAdLevel import \
    FacebookRecommendationEnhancerAdLevel
from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnhancerAdSetLevel import FacebookRecommendationEnhancerAdSetLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationAdLevel import \
    RuleBasedOptimizationAdLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationAdSetLevel import \
    RuleBasedOptimizationAdSetLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationCampaignLevel import \
    RuleBasedOptimizationCampaignLevel
from FacebookDexter.Engine.Algorithms.NoActionAlgorithm import NoActionAlgorithm
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum

AlgorithmType = typing.Union[RuleBasedOptimizationCampaignLevel,
                             RuleBasedOptimizationAdSetLevel,
                             RuleBasedOptimizationAdLevel,
                             typing.NoReturn]


class AlgorithmsFactory:
    __factory = {
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): RuleBasedOptimizationCampaignLevel(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADSET): RuleBasedOptimizationAdSetLevel(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): RuleBasedOptimizationAdLevel(),
        (AlgorithmsEnum.FACEBOOK_ENHANCER, LevelEnum.ADSET): FacebookRecommendationEnhancerAdSetLevel(),
        (AlgorithmsEnum.FACEBOOK_ENHANCER, LevelEnum.AD): FacebookRecommendationEnhancerAdLevel()
    }

    @classmethod
    def get(cls, algorithm_type: AlgorithmsEnum = None, level: LevelEnum = None) -> AlgorithmType:
        algorithm = cls.__factory.get((algorithm_type, level), NoActionAlgorithm())
        return algorithm
