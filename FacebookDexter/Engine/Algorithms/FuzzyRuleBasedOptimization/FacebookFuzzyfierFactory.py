from Core.Dexter.Engine.Algorithms.FuzzyFactoryBase import FuzzyFactoryBase

from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import FacebookAlgorithmsEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.FacebookRuleBasedOptimizationFuzzyfierFactory import \
    FacebookRuleBasedOptimizationFuzzyfierFactory


class FacebookFuzzyfierFactory(FuzzyFactoryBase):
    _factory = {
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
         LevelEnum.CAMPAIGN): FacebookRuleBasedOptimizationFuzzyfierFactory(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
         LevelEnum.ADSET): FacebookRuleBasedOptimizationFuzzyfierFactory(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): FacebookRuleBasedOptimizationFuzzyfierFactory()
    }
