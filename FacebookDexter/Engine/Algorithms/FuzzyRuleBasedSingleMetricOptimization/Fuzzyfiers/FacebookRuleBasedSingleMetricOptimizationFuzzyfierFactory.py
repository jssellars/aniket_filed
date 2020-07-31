from Core.Dexter.Infrastructure.Domain.FuzzyEngine.FuzzyfierFactoryBase import FuzzyfierFactoryBase
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Fuzzyfiers.AggregatedSingleMetricFuzzyfierCollection import \
    AGGREGATED_METRIC_FUZZYFIER_COLLECTION
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Fuzzyfiers.TrendSingleMetricFuzzyfierCollection import \
    TREND_METRIC_FUZZYFIER_COLLECTION


class FacebookRuleBasedSingleMetricOptimizationFuzzyfierFactory(FuzzyfierFactoryBase):

    def __init__(self):
        fuzzyfier_collection = {
            AntecedentTypeEnum.FUZZY_VALUE: AGGREGATED_METRIC_FUZZYFIER_COLLECTION,
            AntecedentTypeEnum.FUZZY_TREND: TREND_METRIC_FUZZYFIER_COLLECTION,
            AntecedentTypeEnum.WEIGHTED_FUZZY_TREND: TREND_METRIC_FUZZYFIER_COLLECTION
        }
        super().__init__(fuzzyfier_collection)
