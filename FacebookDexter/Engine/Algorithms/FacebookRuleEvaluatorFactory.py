from Core.Dexter.Engine.Algorithms.RuleEvaluatorFactoryBase import RuleEvaluatorFactoryBase
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import FacebookAlgorithmsEnum
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEvaluator import FacebookRuleEvaluator


class FacebookRuleEvaluatorFactory(RuleEvaluatorFactoryBase):
    _factory = {
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): FacebookRuleEvaluator(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADSET): FacebookRuleEvaluator(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): FacebookRuleEvaluator()
    }