import typing

from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationAdLevel import \
    RuleBasedOptimizationAdLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationAdSetLevel import \
    RuleBasedOptimizationAdSetLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationCampaignLevel import \
    RuleBasedOptimizationCampaignLevel
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum

AlgorithmType = typing.Union[RuleBasedOptimizationCampaignLevel,
                             RuleBasedOptimizationAdSetLevel,
                             RuleBasedOptimizationAdLevel,
                             typing.NoReturn]


class AlgorithmsFactory:
    __factory = {
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): RuleBasedOptimizationCampaignLevel(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADSET): RuleBasedOptimizationAdSetLevel(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): RuleBasedOptimizationAdLevel()
    }

    @classmethod
    def get(cls, algorithm_type: AlgorithmsEnum = None, level: LevelEnum = None) -> AlgorithmType:
        algorithm = cls.__factory.get((algorithm_type, level), None)
        return algorithm
