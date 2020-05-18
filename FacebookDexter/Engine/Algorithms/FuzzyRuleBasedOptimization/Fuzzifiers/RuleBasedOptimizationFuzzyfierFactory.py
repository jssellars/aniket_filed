from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.AggregatedMetricFuzzyfierCollection import \
    AGGREGATED_METRIC_FUZZYFIER_COLLECTION
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.TrendMetricFuzzyfierCollection import \
    TREND_METRIC_FUZZYFIER_COLLECTION
from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzyfierFactoryBase import FuzzyfierFactoryBase


class RuleBasedOptimizationFuzzyfierFactory(FuzzyfierFactoryBase):

    def __init__(self):
        fuzzyfier_collection = {
            AntecedentTypeEnum.FUZZY_VALUE: AGGREGATED_METRIC_FUZZYFIER_COLLECTION,
            AntecedentTypeEnum.FUZZY_TREND: TREND_METRIC_FUZZYFIER_COLLECTION,
            AntecedentTypeEnum.WEIGHTED_FUZZY_TREND: TREND_METRIC_FUZZYFIER_COLLECTION
        }
        super().__init__(fuzzyfier_collection)
