from Core.Dexter.Engine.Algorithms.FuzzyRuleBasedOptimization.AlgorithmsFactoryBase import AlgorithmsFactoryBase
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Engine.Algorithms.AlgorithmsEnum import FacebookAlgorithmsEnum
from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnhancerAdLevel import \
    FacebookRecommendationEnhancerAdLevel
from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnhancerAdSetLevel import \
    FacebookRecommendationEnhancerAdSetLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.FacebookRuleBasedOptimizationAdLevel import \
    FacebookRuleBasedOptimizationAdLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.FacebookRuleBasedOptimizationAdSetLevel import \
    FacebookRuleBasedOptimizationAdSetLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.FacebookRuleBasedOptimizationCampaignLevel import \
    FacebookRuleBasedOptimizationCampaignLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.FacebookRuleBasedSingleMetricOptimizationAdLevel import FacebookRuleBasedSingleMetricOptimizationAdLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.FacebookRuleBasedSingleMetricOptimizationAdSetLevel import FacebookRuleBasedSingleMetricOptimizationAdSetLevel
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.FacebookRuleBasedSingleMetricOptimizationCampaignLevel import \
    FacebookRuleBasedSingleMetricOptimizationCampaignLevel
from FacebookDexter.Engine.MasterWorker.FacebookStrategyEnum import FacebookStrategyEnum


class FacebookAlgorithmsFactory(AlgorithmsFactoryBase):
    _factory = {
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN,
         ChannelEnum.FACEBOOK, FacebookStrategyEnum.DEFAULT): FacebookRuleBasedOptimizationCampaignLevel(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADSET,
         ChannelEnum.FACEBOOK, FacebookStrategyEnum.DEFAULT): FacebookRuleBasedOptimizationAdSetLevel(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD,
         ChannelEnum.FACEBOOK, FacebookStrategyEnum.DEFAULT): FacebookRuleBasedOptimizationAdLevel(),
        (FacebookAlgorithmsEnum.FACEBOOK_ENHANCER, LevelEnum.ADSET,
         ChannelEnum.FACEBOOK, FacebookStrategyEnum.DEFAULT): FacebookRecommendationEnhancerAdSetLevel(),
        (FacebookAlgorithmsEnum.FACEBOOK_ENHANCER, LevelEnum.AD,
         ChannelEnum.FACEBOOK, FacebookStrategyEnum.DEFAULT): FacebookRecommendationEnhancerAdLevel(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.CAMPAIGN,
         ChannelEnum.FACEBOOK,
         FacebookStrategyEnum.SINGLE_METRIC): FacebookRuleBasedSingleMetricOptimizationCampaignLevel(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.ADSET,
         ChannelEnum.FACEBOOK,
         FacebookStrategyEnum.SINGLE_METRIC): FacebookRuleBasedSingleMetricOptimizationAdSetLevel(),
        (FacebookAlgorithmsEnum.DEXTER_FUZZY_INFERENCE, LevelEnum.AD,
         ChannelEnum.FACEBOOK,
         FacebookStrategyEnum.SINGLE_METRIC): FacebookRuleBasedSingleMetricOptimizationAdLevel(),
    }
