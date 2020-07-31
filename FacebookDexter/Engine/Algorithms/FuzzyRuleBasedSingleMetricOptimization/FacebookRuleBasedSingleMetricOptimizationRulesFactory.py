from Core.Dexter.Engine.Algorithms.RulesFactoryBase import RulesFactoryBase
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import FacebookAlgorithmsEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Rules.Rules import Rules


class FacebookRuleBasedSingleMetricOptimizationRulesFactory(RulesFactoryBase):

    _factory = {
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): Rules(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADSET): Rules(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): Rules()
    }