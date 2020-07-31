from Core.Dexter.Engine.Algorithms.RulesFactoryBase import RulesFactoryBase
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules.Rules import Rules
from GoogleDexter.Engine.Algorithms.GoogleAlgorithmsEnum import GoogleAlgorithmsEnum


class GoogleRulesFactory(RulesFactoryBase):

    _factory = {
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN): Rules(),
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADGROUP): Rules(),
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD): Rules()
    }