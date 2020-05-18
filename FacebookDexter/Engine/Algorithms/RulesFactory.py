import typing

from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.Rules import Rules
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum

RulesType = typing.Union[Rules, typing.NoReturn]


class RulesFactory:
    __factory = {
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): Rules(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADSET): Rules(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): Rules()
    }

    @classmethod
    def get(cls, algorithm_type: AlgorithmsEnum = None, level: LevelEnum = None) -> RulesType:
        rules = cls.__factory.get((algorithm_type, level), None)
        return rules
