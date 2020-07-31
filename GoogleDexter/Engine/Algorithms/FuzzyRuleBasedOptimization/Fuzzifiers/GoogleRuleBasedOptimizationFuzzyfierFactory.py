from Core.Dexter.Infrastructure.Domain.FuzzyEngine.FuzzyfierFactoryBase import FuzzyfierFactoryBase
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.AggregatedMetricFuzzyfierCollection import \
    AGGREGATED_METRIC_FUZZYFIER_COLLECTION
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.TrendMetricFuzzyfierCollection import \
    TREND_METRIC_FUZZYFIER_COLLECTION


class GoogleRuleBasedOptimizationFuzzyfierFactory(FuzzyfierFactoryBase):

    def __init__(self):
        fuzzyfier_collection = {
            AntecedentTypeEnum.FUZZY_VALUE: AGGREGATED_METRIC_FUZZYFIER_COLLECTION,
            AntecedentTypeEnum.FUZZY_TREND: TREND_METRIC_FUZZYFIER_COLLECTION,
            AntecedentTypeEnum.WEIGHTED_FUZZY_TREND: TREND_METRIC_FUZZYFIER_COLLECTION
        }
        super().__init__(fuzzyfier_collection)
