from Core.Tools.Misc.EnumerationBase import EnumerationBase
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricBaseEnum import \
    AvailableMetricBaseEnum
from GoogleDexter.Infrastructure.Domain.Metrics.Metric import Metric
from GoogleDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum, AggregatorEnum
from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata

MILE_MULTIPLIER = 1000
PERCENTAGE_MULTIPLIER = 100


class AvailableMetricEnum(EnumerationBase):
    CPC = Metric(name="CPC", display_name="CPC",
                 numerator=AvailableMetricBaseEnum.SPEND.value,
                 denominator=AvailableMetricBaseEnum.LINK_CLICKS.value, mtype=MetricTypeEnum.INSIGHT)
    CPM = Metric(name="CPM", display_name="CPM", numerator=AvailableMetricBaseEnum.SPEND.value,
                 denominator=AvailableMetricBaseEnum.IMPRESSIONS.value, multiplier=MILE_MULTIPLIER,
                 mtype=MetricTypeEnum.INSIGHT)
    # link_clicks / impressions
    CTR = Metric(name=GoogleFieldsMetadata.ctr.name, display_name="CTR",
                 numerator=AvailableMetricBaseEnum.LINK_CLICKS.value,
                 denominator=AvailableMetricBaseEnum.IMPRESSIONS.value, mtype=MetricTypeEnum.INSIGHT)
    COST_PER_RESULT = Metric(name=GoogleFieldsMetadata.cost_per_conversion.name, display_name="Cost per result",
                             numerator=AvailableMetricBaseEnum.SPEND.value,
                             denominator=AvailableMetricBaseEnum.RESULTS.value, mtype=MetricTypeEnum.INSIGHT)
    COST_PER_PURCHASE = Metric(name="CPP", display_name="Cost per purchase",
                               numerator=AvailableMetricBaseEnum.SPEND.value,
                               denominator=AvailableMetricBaseEnum.PURCHASES.value, mtype=MetricTypeEnum.INSIGHT)
    # frequency =  impressions / reach
    FREQUENCY = Metric(name="Frequency", display_name="Frequency",
                       numerator=AvailableMetricBaseEnum.IMPRESSIONS.value,
                       denominator=AvailableMetricBaseEnum.REACH.value, mtype=MetricTypeEnum.INSIGHT)
    CR = Metric(name=GoogleFieldsMetadata.conversion_rate.name, display_name="Conversion rate",
                numerator=AvailableMetricBaseEnum.CONVERSIONS.value,
                denominator=AvailableMetricBaseEnum.LINK_CLICKS.value, mtype=MetricTypeEnum.INSIGHT)
    #  roas = purchase_value / spend
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
    # COST_PER_APP_INSTALL = Metric(name=GoogleFieldsMetadata.app_install_cost.name, display_name="Cost per app install",
    #                               numerator=AvailableMetricBaseEnum.SPEND.value,
    #                               denominator=AvailableMetricBaseEnum.APP_INSTALLS.value,
    #                               mtype=MetricTypeEnum.INSIGHT)
    # COST_PER_THRUPLAY = Metric(name=GoogleFieldsMetadata.cost_per_thru_play.name, display_name="Cost per thru play",
    #                            numerator=AvailableMetricBaseEnum.SPEND.value,
    #                            denominator=AvailableMetricBaseEnum.THRUPLAYS.value, mtype=MetricTypeEnum.INSIGHT)
    # conversions / unique clicks --> conversions / link clicks
    #  engagement_rate = ( likes + comments + shares + clicks + views) / reach. FB provides this metric
    # ENGAGEMENT_RATE = Metric(name=GoogleFieldsMetadata.post_engagement.name, display_name="Engagement rate",
    #                          numerator=[AvailableMetricBaseEnum.POST_ENGAGEMENT.value],
    #                          denominator=AvailableMetricBaseEnum.REACH.value,
    #                          mtype=MetricTypeEnum.INSIGHT)

    # single metrics
    RESULTS = Metric(name=GoogleFieldsMetadata.conversions.name, display_name="Results",
                     numerator=AvailableMetricBaseEnum.RESULTS.value, mtype=MetricTypeEnum.INSIGHT)
    SPEND = Metric(name=GoogleFieldsMetadata.cost.name, display_name="Amount spent",
                   numerator=AvailableMetricBaseEnum.SPEND.value,
                   mtype=MetricTypeEnum.INSIGHT)
    AVERAGE_SPEND = Metric(name=GoogleFieldsMetadata.cost.name, display_name="Average amount spent",
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
    # PAGE_LIKES = Metric(name=GoogleFieldsMetadata.page_likes.name, display_name="Page likes",
    #                     numerator=AvailableMetricBaseEnum.PAGE_LIKES.value,
    #                     mtype=MetricTypeEnum.INSIGHT)
    # VIDEO_PLAYS = Metric(name=GoogleFieldsMetadata.video_plays.name, display_name="Video plays",
    #                      numerator=AvailableMetricBaseEnum.VIDEO_PLAYS.value,
    #                      mtype=MetricTypeEnum.INSIGHT)
    # RSVPS = Metric(name=GoogleFieldsMetadata.event_responses.name, display_name="RSVPs",
    #                numerator=AvailableMetricBaseEnum.RSVPS.value, mtype=MetricTypeEnum.INSIGHT)
    # APP_INSTALLS = Metric(name=GoogleFieldsMetadata.website_app_installs_total.name, display_name="App installs",
    #                       numerator=AvailableMetricBaseEnum.APP_INSTALLS.value,
    #                       mtype=MetricTypeEnum.INSIGHT)
    # THRUPLAYS = Metric(name=GoogleFieldsMetadata.thru_plays.name, display_name="Thru plays",
    #                    numerator=AvailableMetricBaseEnum.THRUPLAYS.value,
    #                    mtype=MetricTypeEnum.INSIGHT)
    # UNIQUE_CLICKS = Metric(name=GoogleFieldsMetadata.unique_link_clicks.name, display_name="Unique clicks",
    #                        numerator=AvailableMetricBaseEnum.UNIQUE_CLICKS.value,
    #                        mtype=MetricTypeEnum.INSIGHT)
    # POST_LIKES = Metric(name=GoogleFieldsMetadata.post_likes.name, display_name="Post likes",
    #                     numerator=AvailableMetricBaseEnum.POST_LIKES.value,
    #                     mtype=MetricTypeEnum.INSIGHT)
    # POST_COMMENTS = Metric(name=GoogleFieldsMetadata.post_comments.name, display_name="Post comments",
    #                        numerator=AvailableMetricBaseEnum.POST_COMMENTS.value,
    #                        mtype=MetricTypeEnum.INSIGHT)
    # # POST_SHARES = Metric(name=GoogleFieldsMetadata.post_shares.name, display_name="Post shares",
    #                      numerator=AvailableMetricBaseEnum.POST_SHARES.value,
    #                      mtype=MetricTypeEnum.INSIGHT)
    # POST_VIEWS = Metric(name=GoogleFieldsMetadata.photo_views.name, display_name="Post views",
    #                     numerator=AvailableMetricBaseEnum.POST_VIEWS.value,
    #                     mtype=MetricTypeEnum.INSIGHT)

    # QUALITY_RANKING = Metric(name=GoogleFieldsMetadata.quality_ranking.name, display_name="Quality ranking",
    #                          numerator=AvailableMetricBaseEnum.QUALITY_RANKING.value,
    #                          mtype=MetricTypeEnum.INSIGHT_CATEGORICAL)

    # structure metrics
    # OBJECTIVE = Metric(name=GoogleFieldsMetadata.objective.name, display_name="Objective",
    #                    numerator=AvailableMetricBaseEnum.OBJECTIVE.value,
    #                    mtype=MetricTypeEnum.STRUCTURE)

    # INTERESTS = Metric(name="interests", display_name="Interests",
    #                    numerator=AvailableMetricBaseEnum.TEXT_OVERLAY.value,
    #                    mtype=MetricTypeEnum.INTERESTS)
