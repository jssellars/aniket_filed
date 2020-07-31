from Core.Dexter.Engine.Algorithms.FuzzyRuleBasedOptimization.AlgorithmsFactoryBase import AlgorithmsFactoryBase
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.GoogleRuleBasedOptimizationAdGroupLevel import \
    GoogleRuleBasedOptimizationAdGroupLevel
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.GoogleRuleBasedOptimizationAdLevel import \
    GoogleRuleBasedOptimizationAdLevel
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.GoogleRuleBasedOptimizationCampaignLevel import \
    GoogleRuleBasedOptimizationCampaignLevel
from GoogleDexter.Engine.Algorithms.GoogleAlgorithmsEnum import GoogleAlgorithmsEnum


class GoogleAlgorithmsFactory(AlgorithmsFactoryBase):

    _factory = {
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN,
         ChannelEnum.GOOGLE): GoogleRuleBasedOptimizationCampaignLevel(),
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADGROUP,
         ChannelEnum.GOOGLE): GoogleRuleBasedOptimizationAdGroupLevel(),
        (GoogleAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD,
         ChannelEnum.GOOGLE): GoogleRuleBasedOptimizationAdLevel(),
    }