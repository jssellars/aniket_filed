import typing

from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import AlgorithmsEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluator import RuleEvaluator

RuleEvaluatorType = typing.Union[RuleEvaluator,
                                 typing.NoReturn]


class RuleEvaluatorFactory:
    __factory = {
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): RuleEvaluator(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADSET): RuleEvaluator(),
        (AlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): RuleEvaluator()
    }

    @classmethod
    def get(cls, algorithm_type: AlgorithmsEnum = None, level: LevelEnum = None) -> RuleEvaluatorType:
        rule_evaluator = cls.__factory.get((algorithm_type, level), None)
        return rule_evaluator
