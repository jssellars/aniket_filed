import typing

from GoogleDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.Rules import Rules
from GoogleDexter.Infrastructure.Domain.LevelEnums import LevelEnum

RulesType = typing.Union[Rules, typing.NoReturn]


class RulesFactory:
    __factory = {
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): Rules(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADGROUP): Rules(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): Rules()
    }

    @classmethod
    def get(cls, algorithm_type: AlgorithmsEnum = None, level: LevelEnum = None) -> RulesType:
        rules = cls.__factory.get((algorithm_type, level), None)
        return rules
