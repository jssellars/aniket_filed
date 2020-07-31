from Core.Dexter.Infrastructure.Domain.Metrics.Metric import Metric
from Core.Dexter.Infrastructure.Domain.Metrics.MetricEnums import AggregatorEnum
from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedSingleMetricOptimization.Metrics.FacebookAvailableSingleMetricsEnum import \
    FacebookAvailableSingleMetricsEnum
from FacebookDexter.Infrastructure.Domain.Metrics.FacebookMetricEnums import FacebookMetricTypeEnum

MILE_MULTIPLIER = 1000
PERCENTAGE_MULTIPLIER = 100


class FacebookAvailableSingleMetricEnum(EnumerationBase):
    CPC = Metric(name=FieldsMetadata.cpc_all.name, display_name="CPC",
                 numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                 denominator=FacebookAvailableSingleMetricsEnum.LINK_CLICKS.value, mtype=FacebookMetricTypeEnum.INSIGHT)
    CPM = Metric(name=FieldsMetadata.cpm.name, display_name="CPM", numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                 denominator=FacebookAvailableSingleMetricsEnum.IMPRESSIONS.value, multiplier=MILE_MULTIPLIER,
                 mtype=FacebookMetricTypeEnum.INSIGHT)
    # link_clicks / impressions
    CTR = Metric(name=FieldsMetadata.ctr_all.name, display_name="CTR",
                 numerator=FacebookAvailableSingleMetricsEnum.LINK_CLICKS.value,
                 denominator=FacebookAvailableSingleMetricsEnum.IMPRESSIONS.value, mtype=FacebookMetricTypeEnum.INSIGHT)
    COST_PER_RESULT = Metric(name=FieldsMetadata.cost_per_result.name, display_name="Cost per result",
                             numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                             denominator=FacebookAvailableSingleMetricsEnum.RESULTS.value,
                             mtype=FacebookMetricTypeEnum.INSIGHT)
    COST_PER_APP_INSTALL = Metric(name=FieldsMetadata.app_install_cost.name, display_name="Cost per app install",
                                  numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                                  denominator=FacebookAvailableSingleMetricsEnum.APP_INSTALLS.value,
                                  mtype=FacebookMetricTypeEnum.INSIGHT)
    COST_PER_PURCHASE = Metric(name=FieldsMetadata.purchases_cost.name, display_name="Cost per purchase",
                               numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                               denominator=FacebookAvailableSingleMetricsEnum.PURCHASES.value,
                               mtype=FacebookMetricTypeEnum.INSIGHT)
    #  total_spent / total_thruplay
    COST_PER_THRUPLAY = Metric(name=FieldsMetadata.cost_per_thru_play.name, display_name="Cost per thru play",
                               numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                               denominator=FacebookAvailableSingleMetricsEnum.THRUPLAYS.value,
                               mtype=FacebookMetricTypeEnum.INSIGHT)
    # frequency =  impressions / reach
    FREQUENCY = Metric(name=FieldsMetadata.frequency.name, display_name="Frequency",
                       numerator=FacebookAvailableSingleMetricsEnum.IMPRESSIONS.value,
                       denominator=FacebookAvailableSingleMetricsEnum.REACH.value, mtype=FacebookMetricTypeEnum.INSIGHT)
    # conversions / unique clicks
    CR = Metric(name=FieldsMetadata.conversion_rate_ranking.name, display_name="Conversion rate",
                numerator=FacebookAvailableSingleMetricsEnum.CONVERSIONS.value,
                denominator=FacebookAvailableSingleMetricsEnum.UNIQUE_CLICKS.value, mtype=FacebookMetricTypeEnum.INSIGHT,
                multiplier=1000)
    #  engagement_rate = ( likes + comments + shares + clicks + views) / reach. FB provides this metric
    ENGAGEMENT_RATE = Metric(name=FieldsMetadata.post_engagement.name, display_name="Engagement rate",
                             numerator=[FacebookAvailableSingleMetricsEnum.POST_ENGAGEMENT.value],
                             denominator=FacebookAvailableSingleMetricsEnum.REACH.value,
                             mtype=FacebookMetricTypeEnum.INSIGHT)
    #  roas = purchase_value / spend
    ROAS = Metric(name=FieldsMetadata.purchase_roas.name, display_name="ROAS",
                  numerator=FacebookAvailableSingleMetricsEnum.PURCHASES_VALUE.value,
                  denominator=FacebookAvailableSingleMetricsEnum.SPEND.value, mtype=FacebookMetricTypeEnum.INSIGHT)

    # single metrics
    RESULTS = Metric(name=FieldsMetadata.results.name, display_name="Results",
                     numerator=FacebookAvailableSingleMetricsEnum.RESULTS.value, mtype=FacebookMetricTypeEnum.INSIGHT)
    SPEND = Metric(name=FieldsMetadata.amount_spent.name, display_name="Amount spent",
                   numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                   mtype=FacebookMetricTypeEnum.INSIGHT)
    AVERAGE_SPEND = Metric(name=FieldsMetadata.amount_spent.name, display_name="Average amount spent",
                           numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                           numerator_aggregator=AggregatorEnum.AVERAGE, mtype=FacebookMetricTypeEnum.INSIGHT)
    REACH = Metric(name=FieldsMetadata.reach.name, display_name="Reach",
                   numerator=FacebookAvailableSingleMetricsEnum.REACH.value,
                   denominator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                   mtype=FacebookMetricTypeEnum.INSIGHT)
    LINK_CLICKS = Metric(name=FieldsMetadata.link_clicks.name, display_name="Link clicks",
                         numerator=FacebookAvailableSingleMetricsEnum.LINK_CLICKS.value,
                         mtype=FacebookMetricTypeEnum.INSIGHT)
    PAGE_LIKES = Metric(name=FieldsMetadata.page_likes.name, display_name="Page likes",
                        numerator=FacebookAvailableSingleMetricsEnum.PAGE_LIKES.value,
                        mtype=FacebookMetricTypeEnum.INSIGHT)
    IMPRESSIONS = Metric(name=FieldsMetadata.impressions.name, display_name="Impressions",
                         numerator=FacebookAvailableSingleMetricsEnum.IMPRESSIONS.value,
                         # denominator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                         mtype=FacebookMetricTypeEnum.INSIGHT)
    PURCHASES = Metric(name=FieldsMetadata.purchases_total.name, display_name="Purchases",
                       numerator=FacebookAvailableSingleMetricsEnum.PURCHASES.value,
                       mtype=FacebookMetricTypeEnum.INSIGHT)
    VIDEO_PLAYS = Metric(name=FieldsMetadata.video_plays.name, display_name="Video plays",
                         numerator=FacebookAvailableSingleMetricsEnum.VIDEO_PLAYS.value,
                         mtype=FacebookMetricTypeEnum.INSIGHT)
    LEADS = Metric(name=FieldsMetadata.leads_total.name, display_name="Leads",
                   numerator=FacebookAvailableSingleMetricsEnum.LEADS.value, mtype=FacebookMetricTypeEnum.INSIGHT)
    RSVPS = Metric(name=FieldsMetadata.event_responses.name, display_name="RSVPs",
                   numerator=FacebookAvailableSingleMetricsEnum.RSVPS.value, mtype=FacebookMetricTypeEnum.INSIGHT)
    APP_INSTALLS = Metric(name=FieldsMetadata.website_app_installs_total.name, display_name="App installs",
                          numerator=FacebookAvailableSingleMetricsEnum.APP_INSTALLS.value,
                          mtype=FacebookMetricTypeEnum.INSIGHT)
    CONVERSIONS = Metric(name=FieldsMetadata.conversions.name, display_name="Conversions",
                         numerator=FacebookAvailableSingleMetricsEnum.CONVERSIONS.value,
                         mtype=FacebookMetricTypeEnum.INSIGHT)
    THRUPLAYS = Metric(name=FieldsMetadata.thru_plays.name, display_name="Thru plays",
                       numerator=FacebookAvailableSingleMetricsEnum.THRUPLAYS.value,
                       mtype=FacebookMetricTypeEnum.INSIGHT)
    UNIQUE_CLICKS = Metric(name=FieldsMetadata.unique_link_clicks.name, display_name="Unique clicks",
                           numerator=FacebookAvailableSingleMetricsEnum.UNIQUE_CLICKS.value,
                           mtype=FacebookMetricTypeEnum.INSIGHT)
    POST_LIKES = Metric(name=FieldsMetadata.post_likes.name, display_name="Post likes",
                        numerator=FacebookAvailableSingleMetricsEnum.POST_LIKES.value,
                        mtype=FacebookMetricTypeEnum.INSIGHT)
    POST_COMMENTS = Metric(name=FieldsMetadata.post_comments.name, display_name="Post comments",
                           numerator=FacebookAvailableSingleMetricsEnum.POST_COMMENTS.value,
                           mtype=FacebookMetricTypeEnum.INSIGHT)
    POST_SHARES = Metric(name=FieldsMetadata.post_shares.name, display_name="Post shares",
                         numerator=FacebookAvailableSingleMetricsEnum.POST_SHARES.value,
                         mtype=FacebookMetricTypeEnum.INSIGHT)
    POST_VIEWS = Metric(name=FieldsMetadata.photo_views.name, display_name="Post views",
                        numerator=FacebookAvailableSingleMetricsEnum.POST_VIEWS.value,
                        mtype=FacebookMetricTypeEnum.INSIGHT)
    PURCHASES_VALUE = Metric(name=FieldsMetadata.purchases_value.name, display_name="Purchases value",
                             numerator=FacebookAvailableSingleMetricsEnum.PURCHASES_VALUE.value,
                             mtype=FacebookMetricTypeEnum.INSIGHT)
    CLICKS = Metric(name=FieldsMetadata.clicks_all.name, display_name="Clicks",
                    numerator=FacebookAvailableSingleMetricsEnum.CLICKS.value, mtype=FacebookMetricTypeEnum.INSIGHT)

    QUALITY_RANKING = Metric(name=FieldsMetadata.quality_ranking.name, display_name="Quality ranking",
                             numerator=FacebookAvailableSingleMetricsEnum.QUALITY_RANKING.value,
                             mtype=FacebookMetricTypeEnum.INSIGHT_CATEGORICAL)

    # structure metrics
    OBJECTIVE = Metric(name=FieldsMetadata.objective.name, display_name="Objective",
                       numerator=FacebookAvailableSingleMetricsEnum.OBJECTIVE.value,
                       mtype=FacebookMetricTypeEnum.STRUCTURE)

    # audience metrics
    AUDIENCE_SIZE = Metric(name=FieldsMetadata.targeting.name, display_name="Estimated audience size",
                           numerator=FacebookAvailableSingleMetricsEnum.AUDIENCE_SIZE.value,
                           mtype=FacebookMetricTypeEnum.AUDIENCE)

    TEXT_OVERLAY = Metric(name="text_overlay", display_name="Text overlay percent",
                          numerator=FacebookAvailableSingleMetricsEnum.TEXT_OVERLAY.value,
                          mtype=FacebookMetricTypeEnum.CREATIVE)

    INTERESTS = Metric(name="interests", display_name="Interests",
                       numerator=FacebookAvailableSingleMetricsEnum.TEXT_OVERLAY.value,
                       mtype=FacebookMetricTypeEnum.INTERESTS)

    PIXEL = Metric(name="pixel", display_name="Has pixel", numerator=FacebookAvailableSingleMetricsEnum.PIXEL.value,
                   mtype=FacebookMetricTypeEnum.PIXEL)

    PROSPECTING_CAMPAIGN = Metric(name="prospecting_campaign", display_name="Prospecting campaign",
                                  numerator=FacebookAvailableSingleMetricsEnum.PROSPECTING_CAMPAIGN.value,
                                  mtype=FacebookMetricTypeEnum.PROSPECTING)

    NUMBER_OF_ADS = Metric(name="number_of_ads", display_name="Number of ads",
                           numerator=FacebookAvailableSingleMetricsEnum.NUMBER_OF_ADS.value,
                           mtype=FacebookMetricTypeEnum.NUMBER_OF_ADS)

    DUPLICATE_AD = Metric(name="duplicate_ad", display_name="Duplicate ad",
                          numerator=FacebookAvailableSingleMetricsEnum.DUPLICATE_AD.value,
                          mtype=FacebookMetricTypeEnum.DUPLICATE_AD)
