from Core.Dexter.Infrastructure.Domain.Metrics.Metric import Metric
from Core.Dexter.Infrastructure.Domain.Metrics.MetricEnums import AggregatorEnum
from Core.Tools.Misc.EnumerationBase import EnumerationBase
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.GoogleAvailableMetricBaseEnum import \
    GoogleAvailableMetricBaseEnum
from GoogleDexter.Infrastructure.Domain.Metrics.GoogleMetricEnums import GoogleMetricTypeEnum
from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata

MILE_MULTIPLIER = 1000
PERCENTAGE_MULTIPLIER = 100


class GoogleAvailableMetricEnum(EnumerationBase):
    CPC = Metric(name=GoogleFieldsMetadata.average_cpc.name, display_name="CPC",
                 numerator=GoogleAvailableMetricBaseEnum.SPEND.value,
                 denominator=GoogleAvailableMetricBaseEnum.LINK_CLICKS.value, mtype=GoogleMetricTypeEnum.INSIGHT)
    CPM = Metric(name=GoogleFieldsMetadata.average_cpm.name, display_name="CPM",
                 numerator=GoogleAvailableMetricBaseEnum.SPEND.value,
                 denominator=GoogleAvailableMetricBaseEnum.IMPRESSIONS.value, multiplier=MILE_MULTIPLIER,
                 mtype=GoogleMetricTypeEnum.INSIGHT)
    # link_clicks / impressions
    CTR = Metric(name=GoogleFieldsMetadata.ctr.name, display_name="CTR",
                 numerator=GoogleAvailableMetricBaseEnum.LINK_CLICKS.value,
                 denominator=GoogleAvailableMetricBaseEnum.IMPRESSIONS.value, mtype=GoogleMetricTypeEnum.INSIGHT)
    COST_PER_RESULT = Metric(name=GoogleFieldsMetadata.cost_per_conversion.name, display_name="Cost per result",
                             numerator=GoogleAvailableMetricBaseEnum.SPEND.value,
                             denominator=GoogleAvailableMetricBaseEnum.RESULTS.value, mtype=GoogleMetricTypeEnum.INSIGHT)
    COST_PER_CONVERSION = Metric(name=GoogleFieldsMetadata.cost_per_conversion.name,
                                 display_name="Cost per conversion",
                                 numerator=GoogleAvailableMetricBaseEnum.SPEND.value,
                                 denominator=GoogleAvailableMetricBaseEnum.CONVERSIONS.value, mtype=GoogleMetricTypeEnum.INSIGHT)
    # frequency =  impressions / reach
    FREQUENCY = Metric(name=GoogleFieldsMetadata.average_frequency.name, display_name="Frequency",
                       numerator=GoogleAvailableMetricBaseEnum.IMPRESSIONS.value,
                       denominator=GoogleAvailableMetricBaseEnum.REACH.value, mtype=GoogleMetricTypeEnum.INSIGHT)
    CR = Metric(name=GoogleFieldsMetadata.conversion_rate.name, display_name="Conversion rate",
                numerator=GoogleAvailableMetricBaseEnum.CONVERSIONS.value,
                denominator=GoogleAvailableMetricBaseEnum.LINK_CLICKS.value, mtype=GoogleMetricTypeEnum.INSIGHT)
    # roas = purchase_value / spend
    ROAS = Metric(name="ROAS", display_name="ROAS",
                  numerator=GoogleAvailableMetricBaseEnum.PURCHASES_VALUE.value,
                  denominator=GoogleAvailableMetricBaseEnum.SPEND.value, mtype=GoogleMetricTypeEnum.INSIGHT)
    # impressions / spend
    IMPRESSIONS = Metric(name=GoogleFieldsMetadata.impressions.name, display_name="Impressions",
                         numerator=GoogleAvailableMetricBaseEnum.IMPRESSIONS.value,
                         denominator=GoogleAvailableMetricBaseEnum.SPEND.value, mtype=GoogleMetricTypeEnum.INSIGHT)
    # reach / spend
    REACH = Metric(name=GoogleFieldsMetadata.impression_reach.name, display_name="Reach",
                   numerator=GoogleAvailableMetricBaseEnum.REACH.value,
                   denominator=GoogleAvailableMetricBaseEnum.SPEND.value, mtype=GoogleMetricTypeEnum.INSIGHT)

    # single metrics
    RESULTS = Metric(name=GoogleFieldsMetadata.conversions.name, display_name="Results",
                     numerator=GoogleAvailableMetricBaseEnum.RESULTS.value, mtype=GoogleMetricTypeEnum.INSIGHT)
    SPEND = Metric(name=GoogleFieldsMetadata.cost.name, display_name="Amount spent",
                   numerator=GoogleAvailableMetricBaseEnum.SPEND.value,
                   mtype=GoogleMetricTypeEnum.INSIGHT)
    AVERAGE_SPEND = Metric(name=GoogleFieldsMetadata.average_cost.name, display_name="Average amount spent",
                           numerator=GoogleAvailableMetricBaseEnum.SPEND.value,
                           numerator_aggregator=AggregatorEnum.AVERAGE, mtype=GoogleMetricTypeEnum.INSIGHT)
    LINK_CLICKS = Metric(name=GoogleFieldsMetadata.link_clicks.name, display_name="Link clicks",
                         numerator=GoogleAvailableMetricBaseEnum.LINK_CLICKS.value,
                         mtype=GoogleMetricTypeEnum.INSIGHT)
    PURCHASES = Metric(name=GoogleFieldsMetadata.purchases.name, display_name="Purchases",
                       numerator=GoogleAvailableMetricBaseEnum.PURCHASES.value,
                       mtype=GoogleMetricTypeEnum.INSIGHT)
    LEADS = Metric(name=GoogleFieldsMetadata.leads.name, display_name="Leads",
                   numerator=GoogleAvailableMetricBaseEnum.LEADS.value, mtype=GoogleMetricTypeEnum.INSIGHT)
    CONVERSIONS = Metric(name=GoogleFieldsMetadata.conversions.name, display_name="Conversions",
                         numerator=GoogleAvailableMetricBaseEnum.CONVERSIONS.value,
                         mtype=GoogleMetricTypeEnum.INSIGHT)
    PURCHASES_VALUE = Metric(name=GoogleFieldsMetadata.purchase_value.name, display_name="Purchases value",
                             numerator=GoogleAvailableMetricBaseEnum.PURCHASES_VALUE.value,
                             mtype=GoogleMetricTypeEnum.INSIGHT)
    CLICKS = Metric(name=GoogleFieldsMetadata.clicks.name, display_name="Clicks",
                    numerator=GoogleAvailableMetricBaseEnum.CLICKS.value, mtype=GoogleMetricTypeEnum.INSIGHT)

    MULTIPLE_KEYWORDS_PER_ADGROUP = Metric(name="Multiple Keywords Per Adgroup",
                                           display_name="Multiple Keywords Per Adgroup",
                                           numerator=GoogleAvailableMetricBaseEnum.MULTIPLE_KEYWORDS_PER_ADGROUP.value,
                                           mtype=GoogleMetricTypeEnum.KEYWORDS)
