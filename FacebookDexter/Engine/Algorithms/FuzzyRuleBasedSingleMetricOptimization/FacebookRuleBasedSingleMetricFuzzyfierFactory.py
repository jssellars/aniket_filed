from Core.Dexter.Engine.Algorithms.FuzzyFactoryBase import FuzzyFactoryBase

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import FacebookAlgorithmsEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Fuzzyfiers.FacebookRuleBasedSingleMetricOptimizationFuzzyfierFactory import \
    FacebookRuleBasedSingleMetricOptimizationFuzzyfierFactory


class FacebookRuleBasedSingleMetricFuzzyfierFactory(FuzzyFactoryBase):
    _factory = {
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
         LevelEnum.CAMPAIGN): FacebookRuleBasedSingleMetricOptimizationFuzzyfierFactory(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
         LevelEnum.ADSET): FacebookRuleBasedSingleMetricOptimizationFuzzyfierFactory(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
         LevelEnum.AD): FacebookRuleBasedSingleMetricOptimizationFuzzyfierFactory()
    }
