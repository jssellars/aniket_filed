from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricBaseEnum import \
    AvailableMetricBaseEnum
from FacebookDexter.Infrastructure.Domain.Metrics.Metric import Metric
from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum, AggregatorEnum

MILE_MULTIPLIER = 1000
PERCENTAGE_MULTIPLIER = 100


class AvailableMetricEnum(EnumerationBase):
    CPC = Metric(name=FieldsMetadata.cpc_all.name, display_name="CPC", numerator=AvailableMetricBaseEnum.SPEND.value,
                 denominator=AvailableMetricBaseEnum.LINK_CLICKS.value, mtype=MetricTypeEnum.INSIGHT)
    CPM = Metric(name=FieldsMetadata.cpm.name, display_name="CPM", numerator=AvailableMetricBaseEnum.SPEND.value,
                 denominator=AvailableMetricBaseEnum.IMPRESSIONS.value, multiplier=MILE_MULTIPLIER,
                 mtype=MetricTypeEnum.INSIGHT)
    # link_clicks / impressions
    CTR = Metric(name=FieldsMetadata.ctr_all.name, display_name="CTR",
                 numerator=AvailableMetricBaseEnum.LINK_CLICKS.value,
                 denominator=AvailableMetricBaseEnum.IMPRESSIONS.value, mtype=MetricTypeEnum.INSIGHT)
    COST_PER_RESULT = Metric(name=FieldsMetadata.cost_per_result.name, display_name="Cost per result",
                             numerator=AvailableMetricBaseEnum.SPEND.value,
                             denominator=AvailableMetricBaseEnum.RESULTS.value, mtype=MetricTypeEnum.INSIGHT)
    COST_PER_APP_INSTALL = Metric(name=FieldsMetadata.app_install_cost.name, display_name="Cost per app install",
                                  numerator=AvailableMetricBaseEnum.SPEND.value,
                                  denominator=AvailableMetricBaseEnum.APP_INSTALLS.value,
                                  mtype=MetricTypeEnum.INSIGHT)
    COST_PER_PURCHASE = Metric(name=FieldsMetadata.purchases_cost.name, display_name="Cost per purchase",
                               numerator=AvailableMetricBaseEnum.SPEND.value,
                               denominator=AvailableMetricBaseEnum.PURCHASES.value, mtype=MetricTypeEnum.INSIGHT)
    #  total_spent / total_thruplay
    COST_PER_THRUPLAY = Metric(name=FieldsMetadata.cost_per_thru_play.name, display_name="Cost per thru play",
                               numerator=AvailableMetricBaseEnum.SPEND.value,
                               denominator=AvailableMetricBaseEnum.THRUPLAYS.value, mtype=MetricTypeEnum.INSIGHT)
    # frequency =  impressions / reach
    FREQUENCY = Metric(name=FieldsMetadata.frequency.name, display_name="Frequency",
                       numerator=AvailableMetricBaseEnum.IMPRESSIONS.value,
                       denominator=AvailableMetricBaseEnum.REACH.value, mtype=MetricTypeEnum.INSIGHT)
    # conversions / unique clicks
    CR = Metric(name=FieldsMetadata.conversion_rate_ranking.name, display_name="Conversion rate",
                numerator=AvailableMetricBaseEnum.CONVERSIONS.value,
                denominator=AvailableMetricBaseEnum.UNIQUE_CLICKS.value, mtype=MetricTypeEnum.INSIGHT,
                multiplier=1000)
    #  engagement_rate = ( likes + comments + shares + clicks + views) / reach. FB provides this metric
    ENGAGEMENT_RATE = Metric(name=FieldsMetadata.post_engagement.name, display_name="Engagement rate",
                             numerator=[AvailableMetricBaseEnum.POST_ENGAGEMENT.value],
                             denominator=AvailableMetricBaseEnum.REACH.value,
                             mtype=MetricTypeEnum.INSIGHT)
    #  roas = purchase_value / spend
    ROAS = Metric(name=FieldsMetadata.purchase_roas.name, display_name="ROAS",
                  numerator=AvailableMetricBaseEnum.PURCHASES_VALUE.value,
                  denominator=AvailableMetricBaseEnum.SPEND.value, mtype=MetricTypeEnum.INSIGHT)

    # single metrics
    RESULTS = Metric(name=FieldsMetadata.results.name, display_name="Results",
                     numerator=AvailableMetricBaseEnum.RESULTS.value, mtype=MetricTypeEnum.INSIGHT)
    SPEND = Metric(name=FieldsMetadata.amount_spent.name, display_name="Amount spent",
                   numerator=AvailableMetricBaseEnum.SPEND.value,
                   mtype=MetricTypeEnum.INSIGHT)
    AVERAGE_SPEND = Metric(name=FieldsMetadata.amount_spent.name, display_name="Average amount spent",
                           numerator=AvailableMetricBaseEnum.SPEND.value,
                           numerator_aggregator=AggregatorEnum.AVERAGE, mtype=MetricTypeEnum.INSIGHT)
    REACH = Metric(name=FieldsMetadata.reach.name, display_name="Reach",
                   numerator=AvailableMetricBaseEnum.REACH.value,
                   denominator=AvailableMetricBaseEnum.SPEND.value,
                   mtype=MetricTypeEnum.INSIGHT)
    LINK_CLICKS = Metric(name=FieldsMetadata.link_clicks.name, display_name="Link clicks",
                         numerator=AvailableMetricBaseEnum.LINK_CLICKS.value,
                         mtype=MetricTypeEnum.INSIGHT)
    PAGE_LIKES = Metric(name=FieldsMetadata.page_likes.name, display_name="Page likes",
                        numerator=AvailableMetricBaseEnum.PAGE_LIKES.value,
                        mtype=MetricTypeEnum.INSIGHT)
    IMPRESSIONS = Metric(name=FieldsMetadata.impressions.name, display_name="Impressions",
                         numerator=AvailableMetricBaseEnum.IMPRESSIONS.value,
                         denominator=AvailableMetricBaseEnum.SPEND.value,
                         mtype=MetricTypeEnum.INSIGHT)
    PURCHASES = Metric(name=FieldsMetadata.purchases_total.name, display_name="Purchases",
                       numerator=AvailableMetricBaseEnum.PURCHASES.value,
                       mtype=MetricTypeEnum.INSIGHT)
    VIDEO_PLAYS = Metric(name=FieldsMetadata.video_plays.name, display_name="Video plays",
                         numerator=AvailableMetricBaseEnum.VIDEO_PLAYS.value,
                         mtype=MetricTypeEnum.INSIGHT)
    LEADS = Metric(name=FieldsMetadata.leads_total.name, display_name="Leads",
                   numerator=AvailableMetricBaseEnum.LEADS.value, mtype=MetricTypeEnum.INSIGHT)
    RSVPS = Metric(name=FieldsMetadata.event_responses.name, display_name="RSVPs",
                   numerator=AvailableMetricBaseEnum.RSVPS.value, mtype=MetricTypeEnum.INSIGHT)
    APP_INSTALLS = Metric(name=FieldsMetadata.website_app_installs_total.name, display_name="App installs",
                          numerator=AvailableMetricBaseEnum.APP_INSTALLS.value,
                          mtype=MetricTypeEnum.INSIGHT)
    CONVERSIONS = Metric(name=FieldsMetadata.conversions.name, display_name="Conversions",
                         numerator=AvailableMetricBaseEnum.CONVERSIONS.value,
                         mtype=MetricTypeEnum.INSIGHT)
    THRUPLAYS = Metric(name=FieldsMetadata.thru_plays.name, display_name="Thru plays",
                       numerator=AvailableMetricBaseEnum.THRUPLAYS.value,
                       mtype=MetricTypeEnum.INSIGHT)
    UNIQUE_CLICKS = Metric(name=FieldsMetadata.unique_link_clicks.name, display_name="Unique clicks",
                           numerator=AvailableMetricBaseEnum.UNIQUE_CLICKS.value,
                           mtype=MetricTypeEnum.INSIGHT)
    POST_LIKES = Metric(name=FieldsMetadata.post_likes.name, display_name="Post likes",
                        numerator=AvailableMetricBaseEnum.POST_LIKES.value,
                        mtype=MetricTypeEnum.INSIGHT)
    POST_COMMENTS = Metric(name=FieldsMetadata.post_comments.name, display_name="Post comments",
                           numerator=AvailableMetricBaseEnum.POST_COMMENTS.value,
                           mtype=MetricTypeEnum.INSIGHT)
    POST_SHARES = Metric(name=FieldsMetadata.post_shares.name, display_name="Post shares",
                         numerator=AvailableMetricBaseEnum.POST_SHARES.value,
                         mtype=MetricTypeEnum.INSIGHT)
    POST_VIEWS = Metric(name=FieldsMetadata.photo_views.name, display_name="Post views",
                        numerator=AvailableMetricBaseEnum.POST_VIEWS.value,
                        mtype=MetricTypeEnum.INSIGHT)
    PURCHASES_VALUE = Metric(name=FieldsMetadata.purchases_value.name, display_name="Purchases value",
                             numerator=AvailableMetricBaseEnum.PURCHASES_VALUE.value,
                             mtype=MetricTypeEnum.INSIGHT)
    CLICKS = Metric(name=FieldsMetadata.clicks_all.name, display_name="Clicks",
                    numerator=AvailableMetricBaseEnum.CLICKS.value, mtype=MetricTypeEnum.INSIGHT)

    QUALITY_RANKING = Metric(name=FieldsMetadata.quality_ranking.name, display_name="Quality ranking",
                             numerator=AvailableMetricBaseEnum.QUALITY_RANKING.value,
                             mtype=MetricTypeEnum.INSIGHT_CATEGORICAL)

    # structure metrics
    OBJECTIVE = Metric(name=FieldsMetadata.objective.name, display_name="Objective",
                       numerator=AvailableMetricBaseEnum.OBJECTIVE.value,
                       mtype=MetricTypeEnum.STRUCTURE)

    # audience metrics
    AUDIENCE_SIZE = Metric(name=FieldsMetadata.targeting.name, display_name="Estimated audience size",
                           numerator=AvailableMetricBaseEnum.AUDIENCE_SIZE.value,
                           mtype=MetricTypeEnum.AUDIENCE)

    TEXT_OVERLAY = Metric(name="text_overlay", display_name="Text overlay percent",
                          numerator=AvailableMetricBaseEnum.TEXT_OVERLAY.value,
                          mtype=MetricTypeEnum.CREATIVE)

    INTERESTS = Metric(name="interests", display_name="Interests",
                       numerator=AvailableMetricBaseEnum.TEXT_OVERLAY.value,
                       mtype=MetricTypeEnum.INTERESTS)

    PIXEL = Metric(name="pixel", display_name="Has pixel", numerator=AvailableMetricBaseEnum.PIXEL.value,
                   mtype=MetricTypeEnum.PIXEL)

    PROSPECTING_CAMPAIGN = Metric(name="prospecting_campaign", display_name="Prospecting campaign",
                                  numerator=AvailableMetricBaseEnum.PROSPECTING_CAMPAIGN.value,
                                  mtype=MetricTypeEnum.PROSPECTING)

    NUMBER_OF_ADS = Metric(name="number_of_ads", display_name="Number of ads",
                           numerator=AvailableMetricBaseEnum.NUMBER_OF_ADS.value,
                           mtype=MetricTypeEnum.NUMBER_OF_ADS)

    DUPLICATE_AD = Metric(name="duplicate_ad", display_name="Duplicate ad",
                          numerator=AvailableMetricBaseEnum.DUPLICATE_AD.value,
                          mtype=MetricTypeEnum.DUPLICATE_AD)
