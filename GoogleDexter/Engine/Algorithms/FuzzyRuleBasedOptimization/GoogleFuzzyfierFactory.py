from Core.Dexter.Engine.Algorithms.FuzzyFactoryBase import FuzzyFactoryBase
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.GoogleRuleBasedOptimizationFuzzyfierFactory import \
    GoogleRuleBasedOptimizationFuzzyfierFactory
from GoogleDexter.Engine.Algorithms.GoogleAlgorithmsEnum import GoogleAlgorithmsEnum


class GoogleFuzzyfierFactory(FuzzyFactoryBase):
    _factory = {
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
         LevelEnum.CAMPAIGN): GoogleRuleBasedOptimizationFuzzyfierFactory(),
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
         LevelEnum.ADGROUP): GoogleRuleBasedOptimizationFuzzyfierFactory(),
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE,
         LevelEnum.AD): GoogleRuleBasedOptimizationFuzzyfierFactory()
    }
