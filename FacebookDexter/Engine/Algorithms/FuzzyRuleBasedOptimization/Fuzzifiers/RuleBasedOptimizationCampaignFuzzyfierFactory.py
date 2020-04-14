from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.AggregatedMetricFuzzyfier import AggregatedMetricFuzzyfierCollection
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Fuzzifiers.TrendMetricFuzzyfier import TrendMetricFuzzyfierCollection
from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum


class RuleBasedOptimizationCampaignFuzzyfierFactory:
    average = AggregatedMetricFuzzyfierCollection
    trend = TrendMetricFuzzyfierCollection

    @classmethod
    def get_fuzzyfier_collection_by_metric_type(cls, metric_type: MetricTypeEnum = None):
        try:
            fuzzyfier_collection = getattr(cls, metric_type.name.lower())
        except ValueError as e:
            raise ValueError(f"Invalid fuzzyfier collection name {metric_type.name}")

        return fuzzyfier_collection
