import typing

from Core.Dexter.Engine.Algorithms.RuleEvaluatorFactoryBase import RuleEvaluatorFactoryBase
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Engine.Algorithms.GoogleAlgorithmsEnum import GoogleAlgorithmsEnum
from GoogleDexter.Infrastructure.Domain.Rules.GoogleRuleEvaluator import GoogleRuleEvaluator

RuleEvaluatorType = typing.Union[GoogleRuleEvaluator,
                                 typing.NoReturn]


class GoogleRuleEvaluatorFactory(RuleEvaluatorFactoryBase):
    _factory = {
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): GoogleRuleEvaluator(),
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADGROUP): GoogleRuleEvaluator(),
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): GoogleRuleEvaluator()
    }
