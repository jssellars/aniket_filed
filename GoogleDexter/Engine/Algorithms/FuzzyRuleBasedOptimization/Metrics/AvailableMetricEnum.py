from Core.Tools.Misc.EnumerationBase import EnumerationBase
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricBaseEnum import \
    AvailableMetricBaseEnum
from GoogleDexter.Infrastructure.Domain.Metrics.Metric import Metric
from GoogleDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum, AggregatorEnum
from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata

MILE_MULTIPLIER = 1000
PERCENTAGE_MULTIPLIER = 100


class AvailableMetricEnum(EnumerationBase):
    CPC = Metric(name=GoogleFieldsMetadata.average_cpc.name, display_name="CPC",
                 numerator=AvailableMetricBaseEnum.SPEND.value,
                 denominator=AvailableMetricBaseEnum.LINK_CLICKS.value, mtype=MetricTypeEnum.INSIGHT)
    CPM = Metric(name=GoogleFieldsMetadata.average_cpm.name, display_name="CPM",
                 numerator=AvailableMetricBaseEnum.SPEND.value,
                 denominator=AvailableMetricBaseEnum.IMPRESSIONS.value, multiplier=MILE_MULTIPLIER,
                 mtype=MetricTypeEnum.INSIGHT)
    # link_clicks / impressions
    CTR = Metric(name=GoogleFieldsMetadata.ctr.name, display_name="CTR",
                 numerator=AvailableMetricBaseEnum.LINK_CLICKS.value,
                 denominator=AvailableMetricBaseEnum.IMPRESSIONS.value, mtype=MetricTypeEnum.INSIGHT)
    COST_PER_RESULT = Metric(name=GoogleFieldsMetadata.cost_per_conversion.name, display_name="Cost per result",
                             numerator=AvailableMetricBaseEnum.SPEND.value,
                             denominator=AvailableMetricBaseEnum.RESULTS.value, mtype=MetricTypeEnum.INSIGHT)
    COST_PER_CONVERSION = Metric(name=GoogleFieldsMetadata.cost_per_conversion.name,
                                 display_name="Cost per conversion",
                                 numerator=AvailableMetricBaseEnum.SPEND.value,
                                 denominator=AvailableMetricBaseEnum.CONVERSIONS.value, mtype=MetricTypeEnum.INSIGHT)
    # frequency =  impressions / reach
    FREQUENCY = Metric(name=GoogleFieldsMetadata.average_frequency.name, display_name="Frequency",
                       numerator=AvailableMetricBaseEnum.IMPRESSIONS.value,
                       denominator=AvailableMetricBaseEnum.REACH.value, mtype=MetricTypeEnum.INSIGHT)
    CR = Metric(name=GoogleFieldsMetadata.conversion_rate.name, display_name="Conversion rate",
                numerator=AvailableMetricBaseEnum.CONVERSIONS.value,
                denominator=AvailableMetricBaseEnum.LINK_CLICKS.value, mtype=MetricTypeEnum.INSIGHT)
    # roas = purchase_value / spend
    ROAS = Metric(name="ROAS", display_name="ROAS",
                  numerator=AvailableMetricBaseEnum.PURCHASES_VALUE.value,
                  denominator=AvailableMetricBaseEnum.SPEND.value, mtype=MetricTypeEnum.INSIGHT)
    # impressions / spend
    IMPRESSIONS = Metric(name=GoogleFieldsMetadata.impressions.name, display_name="Impressions",
                         numerator=AvailableMetricBaseEnum.IMPRESSIONS.value,
                         denominator=AvailableMetricBaseEnum.SPEND.value, mtype=MetricTypeEnum.INSIGHT)
    # reach / spend
    REACH = Metric(name=GoogleFieldsMetadata.impression_reach.name, display_name="Reach",
                   numerator=AvailableMetricBaseEnum.REACH.value,
                   denominator=AvailableMetricBaseEnum.SPEND.value, mtype=MetricTypeEnum.INSIGHT)

    # single metrics
    RESULTS = Metric(name=GoogleFieldsMetadata.conversions.name, display_name="Results",
                     numerator=AvailableMetricBaseEnum.RESULTS.value, mtype=MetricTypeEnum.INSIGHT)
    SPEND = Metric(name=GoogleFieldsMetadata.cost.name, display_name="Amount spent",
                   numerator=AvailableMetricBaseEnum.SPEND.value,
                   mtype=MetricTypeEnum.INSIGHT)
    AVERAGE_SPEND = Metric(name=GoogleFieldsMetadata.average_cost.name, display_name="Average amount spent",
                           numerator=AvailableMetricBaseEnum.SPEND.value,
                           numerator_aggregator=AggregatorEnum.AVERAGE, mtype=MetricTypeEnum.INSIGHT)
    LINK_CLICKS = Metric(name=GoogleFieldsMetadata.link_clicks.name, display_name="Link clicks",
                         numerator=AvailableMetricBaseEnum.LINK_CLICKS.value,
                         mtype=MetricTypeEnum.INSIGHT)
    PURCHASES = Metric(name=GoogleFieldsMetadata.purchases.name, display_name="Purchases",
                       numerator=AvailableMetricBaseEnum.PURCHASES.value,
                       mtype=MetricTypeEnum.INSIGHT)
    LEADS = Metric(name=GoogleFieldsMetadata.leads.name, display_name="Leads",
                   numerator=AvailableMetricBaseEnum.LEADS.value, mtype=MetricTypeEnum.INSIGHT)
    CONVERSIONS = Metric(name=GoogleFieldsMetadata.conversions.name, display_name="Conversions",
                         numerator=AvailableMetricBaseEnum.CONVERSIONS.value,
                         mtype=MetricTypeEnum.INSIGHT)
    PURCHASES_VALUE = Metric(name=GoogleFieldsMetadata.purchase_value.name, display_name="Purchases value",
                             numerator=AvailableMetricBaseEnum.PURCHASES_VALUE.value,
                             mtype=MetricTypeEnum.INSIGHT)
    CLICKS = Metric(name=GoogleFieldsMetadata.clicks.name, display_name="Clicks",
                    numerator=AvailableMetricBaseEnum.CLICKS.value, mtype=MetricTypeEnum.INSIGHT)

    MULTIPLE_KEYWORDS_PER_ADGROUP = Metric(name="Multiple Keywords Per Adgroup",
                                           display_name="Multiple Keywords Per Adgroup",
                                           numerator=AvailableMetricBaseEnum.MULTIPLE_KEYWORDS_PER_ADGROUP.value,
                                           mtype=MetricTypeEnum.KEYWORDS)
