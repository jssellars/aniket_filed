import typing

from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.RuleBasedOptimizationFuzzyfierFactory import \
    RuleBasedOptimizationFuzzyfierFactory
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum

FuzzyfierFactoryType = typing.Union[RuleBasedOptimizationFuzzyfierFactory,
                                    typing.NoReturn]


class FuzzyfierFactory:
    __factory = {
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): RuleBasedOptimizationFuzzyfierFactory(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADSET): RuleBasedOptimizationFuzzyfierFactory(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): RuleBasedOptimizationFuzzyfierFactory()
    }

    @classmethod
    def get(cls, algorithm_type: AlgorithmsEnum = None, level: LevelEnum = None) -> FuzzyfierFactoryType:
        fuzzyfier_factory = cls.__factory.get((algorithm_type, level), None)
        return fuzzyfier_factory