import typing

from GoogleDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationAdGroupLevel import \
    RuleBasedOptimizationAdGroupLevel
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationAdLevel import \
    RuleBasedOptimizationAdLevel
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationCampaignLevel import \
    RuleBasedOptimizationCampaignLevel
from GoogleDexter.Infrastructure.Domain.LevelEnums import LevelEnum

AlgorithmType = typing.Union[RuleBasedOptimizationCampaignLevel,
                             RuleBasedOptimizationAdGroupLevel,
                             RuleBasedOptimizationAdLevel,
                             typing.NoReturn]


class AlgorithmsFactory:
    __factory = {
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): RuleBasedOptimizationCampaignLevel(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADGROUP): RuleBasedOptimizationAdGroupLevel(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): RuleBasedOptimizationAdLevel()
    }

    @classmethod
    def get(cls, algorithm_type: AlgorithmsEnum = None, level: LevelEnum = None) -> AlgorithmType:
        algorithm = cls.__factory.get((algorithm_type, level), None)
        return algorithm
