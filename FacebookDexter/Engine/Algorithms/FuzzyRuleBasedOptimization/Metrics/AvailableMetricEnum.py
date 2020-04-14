from enum import Enum

from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricBaseEnum import AvailableMetricBaseEnum
from FacebookDexter.Infrastructure.Domain.Metrics.Metric import Metric
from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum

MILE_MULTIPLIER = 1000
PERCENTAGE_MULTIPLIER = 100


# todo: check if the metric name corresponds with what we have in the database for each metric. This will need further verification after Turing metrics are
#  all implemented
class AvailableMetricEnum(Enum):
    CPC = Metric(name=FieldsMetadata.all_cpc.name, display_name="CPC", numerator=AvailableMetricBaseEnum.SPEND.value,
                 denominator=AvailableMetricBaseEnum.LINK_CLICKS.value, mtype=MetricTypeEnum.INSIGHT)
    CPM = Metric(name=FieldsMetadata.cpm.name, display_name="CPM", numerator=AvailableMetricBaseEnum.SPEND.value,
                 denominator=AvailableMetricBaseEnum.IMPRESSIONS.value, multiplier=MILE_MULTIPLIER, mtype=MetricTypeEnum.INSIGHT)
    # link_clicks / impressions
    CTR = Metric(name=FieldsMetadata.all_ctr.name, display_name="CTR", numerator=AvailableMetricBaseEnum.LINK_CLICKS.value,
                 denominator=AvailableMetricBaseEnum.IMPRESSIONS.value, mtype=MetricTypeEnum.INSIGHT)
    COST_PER_RESULT = Metric(name=FieldsMetadata.cost_per_result.name, display_name="Cost per result", numerator=AvailableMetricBaseEnum.SPEND.value,
                             denominator=AvailableMetricBaseEnum.RESULTS.value, mtype=MetricTypeEnum.INSIGHT)
    COST_PER_APP_INSTALL = Metric(name=FieldsMetadata.cost_per_app_install.name, display_name="Cost per app install",
                                  numerator=AvailableMetricBaseEnum.SPEND.value, denominator=AvailableMetricBaseEnum.APP_INSTALLS.value,
                                  mtype=MetricTypeEnum.INSIGHT)
    COST_PER_PURCHASE = Metric(name=FieldsMetadata.cost_per_purchase.name, display_name="Cost per purchase", numerator=AvailableMetricBaseEnum.SPEND.value,
                               denominator=AvailableMetricBaseEnum.PURCHASES.value, mtype=MetricTypeEnum.INSIGHT)
    #  total_spent / total_thruplay
    COST_PER_THRUPLAY = Metric(name=FieldsMetadata.cost_per_thruplay.name, display_name="Cost per thru play", numerator=AvailableMetricBaseEnum.SPEND.value,
                               denominator=AvailableMetricBaseEnum.THRUPLAYS.value, mtype=MetricTypeEnum.INSIGHT)
    # frequency =  impressions / reach
    FREQUENCY = Metric(name=FieldsMetadata.frequency.name, display_name="Frequency", numerator=AvailableMetricBaseEnum.IMPRESSIONS.value,
                       denominator=AvailableMetricBaseEnum.REACH.value, mtype=MetricTypeEnum.INSIGHT)
    # conversions / unique clicks
    CR = Metric(name=FieldsMetadata.conversion_rate.name, display_name="Conversion rate", numerator=AvailableMetricBaseEnum.CONVERSIONS.value,
                denominator=AvailableMetricBaseEnum.UNIQUE_CLICKS.value, mtype=MetricTypeEnum.INSIGHT)
    #  engagement_rate = ( likes + comments + shares + clicks + views) / reach
    ENGAGEMENT_RATE = Metric(name=FieldsMetadata.engagement.name, display_name="Engagement",
                             numerator=[AvailableMetricBaseEnum.POST_LIKES.value,
                                        AvailableMetricBaseEnum.POST_COMMENTS.value,
                                        AvailableMetricBaseEnum.POST_SHARES.value,
                                        AvailableMetricBaseEnum.POST_VIEWS.value,
                                        AvailableMetricBaseEnum.CLICKS.value],
                             denominator=AvailableMetricBaseEnum.REACH.value,
                             mtype=MetricTypeEnum.INSIGHT)
    #  roas = purchase_value / spend
    ROAS = Metric(name=FieldsMetadata.purchase_roas.name, display_name="ROAS", numerator=AvailableMetricBaseEnum.PURCHASES_VALUE.value,
                  denominator=AvailableMetricBaseEnum.SPEND.value, mtype=MetricTypeEnum.INSIGHT)

    # single metrics
    RESULTS = Metric(name=FieldsMetadata.results.name, display_name="Results", numerator=AvailableMetricBaseEnum.RESULTS.value, mtype=MetricTypeEnum.INSIGHT)
    SPEND = Metric(name=FieldsMetadata.spend.name, display_name="Amount spent", numerator=AvailableMetricBaseEnum.SPEND.value, mtype=MetricTypeEnum.INSIGHT)
    REACH = Metric(name=FieldsMetadata.reach.name, display_name="Reach", numerator=AvailableMetricBaseEnum.REACH.value, mtype=MetricTypeEnum.INSIGHT)
    LINK_CLICKS = Metric(name=FieldsMetadata.link_click.name, display_name="Link clicks", numerator=AvailableMetricBaseEnum.LINK_CLICKS.value,
                         mtype=MetricTypeEnum.INSIGHT)
    PAGE_LIKES = Metric(name=FieldsMetadata.page_like.name, display_name="Page likes", numerator=AvailableMetricBaseEnum.PAGE_LIKES.value,
                        mtype=MetricTypeEnum.INSIGHT)
    IMPRESSIONS = Metric(name=FieldsMetadata.impressions.name, display_name="Impressions", numerator=AvailableMetricBaseEnum.IMPRESSIONS.value,
                         mtype=MetricTypeEnum.INSIGHT)
    PURCHASES = Metric(name=FieldsMetadata.purchases.name, display_name="Purchases", numerator=AvailableMetricBaseEnum.PURCHASES.value,
                       mtype=MetricTypeEnum.INSIGHT)
    VIDEO_PLAYS = Metric(name=FieldsMetadata.video_play.name, display_name="Video plays", numerator=AvailableMetricBaseEnum.VIDEO_PLAYS.value,
                         mtype=MetricTypeEnum.INSIGHT)
    LEADS = Metric(name=FieldsMetadata.leads.name, display_name="Leads", numerator=AvailableMetricBaseEnum.LEADS.value, mtype=MetricTypeEnum.INSIGHT)
    RSVPS = Metric(name=FieldsMetadata.event_responses.name, display_name="RSVPs", numerator=AvailableMetricBaseEnum.RSVPS.value, mtype=MetricTypeEnum.INSIGHT)
    APP_INSTALLS = Metric(name=FieldsMetadata.app_installs.name, display_name="App installs", numerator=AvailableMetricBaseEnum.APP_INSTALLS.value,
                          mtype=MetricTypeEnum.INSIGHT)
    CONVERSIONS = Metric(name=FieldsMetadata.conversions.name, display_name="Conversions", numerator=AvailableMetricBaseEnum.CONVERSIONS.value,
                         mtype=MetricTypeEnum.INSIGHT)
    THRUPLAYS = Metric(name=FieldsMetadata.thruplay.name, display_name="Thru plays", numerator=AvailableMetricBaseEnum.THRUPLAYS.value,
                       mtype=MetricTypeEnum.INSIGHT)
    UNIQUE_CLICKS = Metric(name=FieldsMetadata.unique_click.name, display_name="Unique clicks", numerator=AvailableMetricBaseEnum.UNIQUE_CLICKS.value,
                           mtype=MetricTypeEnum.INSIGHT)
    POST_LIKES = Metric(name=FieldsMetadata.post_likes.name, display_name="Post likes", numerator=AvailableMetricBaseEnum.POST_LIKES.value,
                        mtype=MetricTypeEnum.INSIGHT)
    POST_COMMENTS = Metric(name=FieldsMetadata.post_comment.name, display_name="Post comments", numerator=AvailableMetricBaseEnum.POST_COMMENTS.value,
                           mtype=MetricTypeEnum.INSIGHT)
    POST_SHARES = Metric(name=FieldsMetadata.post_share.name, display_name="Post shares", numerator=AvailableMetricBaseEnum.POST_SHARES.value,
                         mtype=MetricTypeEnum.INSIGHT)
    POST_VIEWS = Metric(name=FieldsMetadata.post_views.name, display_name="Post views", numerator=AvailableMetricBaseEnum.POST_VIEWS.value,
                        mtype=MetricTypeEnum.INSIGHT)  #  todo: what are  post views ??
    PURCHASES_VALUE = Metric(name=FieldsMetadata.purchases_value.name, display_name="Purchases value", numerator=AvailableMetricBaseEnum.PURCHASES_VALUE.value,
                             mtype=MetricTypeEnum.INSIGHT)
    CLICKS = Metric(name=FieldsMetadata.all_clicks.name, display_name="Clicks", numerator=AvailableMetricBaseEnum.CLICKS.value, mtype=MetricTypeEnum.INSIGHT)

    RELEVANCY_SCORE = Metric(name=FieldsMetadata.relevancy_score.name, display_name="Relevancy score",
                             numerator=AvailableMetricBaseEnum.RELEVANCY_SCORE.value, mtype=MetricTypeEnum.INSIGHT)

    # structure metrics
    OBJECTIVE = Metric(name=FieldsMetadata.objective.name, display_name="Objective", numerator=AvailableMetricBaseEnum.OBJECTIVE.value,
                       mtype=MetricTypeEnum.STRUCTURE)

    # audience metrics
    AUDIENCE_SIZE = Metric(name="audience_size", display_name="Estimated audience size", numerator=AvailableMetricBaseEnum.AUDIENCE_SIZE.value,
                           mtype=MetricTypeEnum.AUDIENCE)