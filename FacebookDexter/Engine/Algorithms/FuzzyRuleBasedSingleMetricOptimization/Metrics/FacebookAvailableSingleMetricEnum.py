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
                 denominator=FacebookAvailableSingleMetricsEnum.LINK_CLICKS.value,
                 mtype=FacebookMetricTypeEnum.INSIGHT)
    CPM = Metric(name=FieldsMetadata.cpm.name, display_name="CPM",
                 numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                 denominator=FacebookAvailableSingleMetricsEnum.IMPRESSIONS.value, multiplier=MILE_MULTIPLIER,
                 mtype=FacebookMetricTypeEnum.INSIGHT)
    # link_clicks / impressions
    CTR = Metric(name=FieldsMetadata.ctr_all.name, display_name="CTR",
                 numerator=FacebookAvailableSingleMetricsEnum.LINK_CLICKS.value,
                 denominator=FacebookAvailableSingleMetricsEnum.IMPRESSIONS.value,
                 mtype=FacebookMetricTypeEnum.INSIGHT)
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
    # total_spent / total_thruplay
    COST_PER_THRUPLAY = Metric(name=FieldsMetadata.cost_per_thru_play.name, display_name="Cost per thru play",
                               numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                               denominator=FacebookAvailableSingleMetricsEnum.THRUPLAYS.value,
                               mtype=FacebookMetricTypeEnum.INSIGHT)
    # frequency =  impressions / reach
    FREQUENCY = Metric(name=FieldsMetadata.frequency.name, display_name="Frequency",
                       numerator=FacebookAvailableSingleMetricsEnum.IMPRESSIONS.value,
                       denominator=FacebookAvailableSingleMetricsEnum.REACH.value,
                       mtype=FacebookMetricTypeEnum.INSIGHT)
    # conversions / unique clicks
    CR = Metric(name=FieldsMetadata.conversion_rate_ranking.name, display_name="Conversion rate",
                numerator=FacebookAvailableSingleMetricsEnum.CONVERSIONS.value,
                denominator=FacebookAvailableSingleMetricsEnum.UNIQUE_CLICKS.value,
                mtype=FacebookMetricTypeEnum.INSIGHT,
                multiplier=1000)
    # engagement_rate = ( likes + comments + shares + clicks + views) / reach. FB provides this metric
    ENGAGEMENT_RATE = Metric(name=FieldsMetadata.post_engagement.name, display_name="Engagement rate",
                             numerator=[FacebookAvailableSingleMetricsEnum.POST_ENGAGEMENT.value],
                             denominator=FacebookAvailableSingleMetricsEnum.REACH.value,
                             mtype=FacebookMetricTypeEnum.INSIGHT)
    # roas = purchase_value / spend
    ROAS = Metric(name=FieldsMetadata.purchase_roas.name, display_name="ROAS",
                  numerator=FacebookAvailableSingleMetricsEnum.PURCHASES_VALUE.value,
                  denominator=FacebookAvailableSingleMetricsEnum.SPEND.value, mtype=FacebookMetricTypeEnum.INSIGHT)
    COST_PER_UNIQUE_CONTENT_VIEW = Metric(name="cost_per_unique_content_view",
                                          display_name="Cost per unique content view",
                                          numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                                          denominator=FacebookAvailableSingleMetricsEnum.CONTENT_VIEWS_UNIQUE.value,
                                          mtype=FacebookMetricTypeEnum.INSIGHT)
    COST_PER_UNIQUE_ADD_TO_CARTS = Metric(name='cost_per_unique_add_to_carts',
                                          display_name="Cost per unique add to carts",
                                          numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                                          denominator=FacebookAvailableSingleMetricsEnum.ADDS_TO_CART_UNIQUE.value,
                                          mtype=FacebookMetricTypeEnum.INSIGHT)
    COST_PER_UNIQUE_CHECKOUTS_INITIATED = Metric(name="cost_per_unique_checkouts_initiated",
                                                 display_name="Cost per unique checkouts initiated",
                                                 numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                                                 denominator=FacebookAvailableSingleMetricsEnum.CHECKOUTS_INITIATED_UNIQUE.value,
                                                 mtype=FacebookMetricTypeEnum.INSIGHT)
    COST_PER_UNIQUE_CLICKS_ALL = Metric(name='cost_per_unique_clicks_all',
                                        display_name="Cost per unique clicks all",
                                        numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                                        denominator=FacebookAvailableSingleMetricsEnum.UNIQUE_CLICKS_ALL.value,
                                        mtype=FacebookMetricTypeEnum.INSIGHT)
    COST_PER_ADD_TO_CART = Metric(name='cost_per_add_to_cart',
                                  display_name="Cost per add to cart",
                                  numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                                  denominator=FacebookAvailableSingleMetricsEnum.ADDS_TO_CART.value,
                                  mtype=FacebookMetricTypeEnum.INSIGHT)
    COST_PER_CHECKOUT = Metric(name='cost_per_checkout',
                               display_name="Cost per checkout",
                               numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                               denominator=FacebookAvailableSingleMetricsEnum.CHECKOUTS_INITIATED.value,
                               mtype=FacebookMetricTypeEnum.INSIGHT)
    COST_PER_3S_VIDEO_VIEWS = Metric(name='cost_per_3_s_video_views',
                                     display_name="Cost per 3 s video views",
                                     numerator=FacebookAvailableSingleMetricsEnum.SPEND.value,
                                     denominator=FacebookAvailableSingleMetricsEnum.VIDEO_PLAYS_3S.value,
                                     mtype=FacebookMetricTypeEnum.INSIGHT)
    LANDING_PAGE_CONVERSION_RATE = Metric(name='landing_page_conversion_rate',
                                          display_name="Landing page conversion rate",
                                          numerator=FacebookAvailableSingleMetricsEnum.CONVERSIONS.value,
                                          denominator=FacebookAvailableSingleMetricsEnum.LINK_CLICKS.value,
                                          multiplier=PERCENTAGE_MULTIPLIER,
                                          mtype=FacebookMetricTypeEnum.INSIGHT)
    ADD_TO_CART_AVERAGE_VALUE = Metric(name='add_to_cart_average_value',
                                       display_name="Add to cart average value",
                                       numerator=FacebookAvailableSingleMetricsEnum.ADDS_TO_CART_VALUE.value,
                                       denominator=FacebookAvailableSingleMetricsEnum.ADDS_TO_CART.value,
                                       mtype=FacebookMetricTypeEnum.INSIGHT)
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

    VIDEO_PLAYS_3S = Metric(name=FieldsMetadata.video_plays_3s.name, display_name='Video plays 3s',
                            numerator=FacebookAvailableSingleMetricsEnum.VIDEO_PLAYS_3S.value,
                            mtype=FacebookMetricTypeEnum.INSIGHT)
    VIDEO_PLAYS_95P = Metric(name=FieldsMetadata.video_plays_95p.name, display_name='Video plays 95%',
                             numerator=FacebookAvailableSingleMetricsEnum.VIDEO_PLAYS_95P.value,
                             mtype=FacebookMetricTypeEnum.INSIGHT)
    VIDEO_AVERAGE_PLAY_TIME = Metric(name=FieldsMetadata.video_average_play_time.name,
                                     display_name='Video play average play time',
                                     numerator=FacebookAvailableSingleMetricsEnum.VIDEO_AVERAGE_PLAY_TIME.value,
                                     mtype=FacebookMetricTypeEnum.INSIGHT)
    ADDS_TO_CART = Metric(name=FieldsMetadata.adds_to_cart_total.name, display_name='Adds to cart',
                          numerator=FacebookAvailableSingleMetricsEnum.ADDS_TO_CART.value,
                          mtype=FacebookMetricTypeEnum.INSIGHT)
    ADDS_TO_CART_VALUE = Metric(name=FieldsMetadata.adds_to_cart_value.name, display_name='Adds to cart value',
                                numerator=FacebookAvailableSingleMetricsEnum.ADDS_TO_CART_VALUE.value,
                                mtype=FacebookMetricTypeEnum.INSIGHT)
    CHECKOUTS_INITIATED_VALUE = Metric(name=FieldsMetadata.website_checkouts_initiated_value.name,
                                       display_name='Checkouts initiated value',
                                       numerator=FacebookAvailableSingleMetricsEnum.CHECKOUTS_INITIATED_VALUE.value,
                                       mtype=FacebookMetricTypeEnum.INSIGHT)
    UNIQUE_CLICKS_ALL = Metric(name=FieldsMetadata.unique_clicks_all.name, display_name='Unique clicks',
                               numerator=FacebookAvailableSingleMetricsEnum.UNIQUE_CLICKS_ALL.value,
                               mtype=FacebookMetricTypeEnum.INSIGHT)
    UNIQUE_CTR_ALL = Metric(name=FieldsMetadata.unique_ctr_all.name, display_name='Unique CTR',
                            numerator=FacebookAvailableSingleMetricsEnum.UNIQUE_CTR_ALL.value,
                            mtype=FacebookMetricTypeEnum.INSIGHT)
    MESSAGING_CONVERSATIONS_STARTED = Metric(name=FieldsMetadata.messaging_conversations_started.name,
                                             display_name='Messaging conversations started',
                                             numerator=FacebookAvailableSingleMetricsEnum.MESSAGING_CONVERSATIONS_STARTED.value,
                                             mtype=FacebookMetricTypeEnum.INSIGHT)
    UNIQUE_LINK_CTR = Metric(name=FieldsMetadata.unique_link_click_through_rate.name, display_name='Unique link CTR',
                             numerator=FacebookAvailableSingleMetricsEnum.UNIQUE_LINK_CTR.value,
                             mtype=FacebookMetricTypeEnum.INSIGHT)
    CONTENT_VIEWS_UNIQUE = Metric(name=FieldsMetadata.content_views_unique_total.name,
                                  display_name='Content views unique',
                                  numerator=FacebookAvailableSingleMetricsEnum.CONTENT_VIEWS_UNIQUE.value,
                                  mtype=FacebookMetricTypeEnum.INSIGHT)

    ADDS_TO_CART_UNIQUE = Metric(name=FieldsMetadata.adds_to_cart_unique.name, display_name='Adds to cart unique',
                                 numerator=FacebookAvailableSingleMetricsEnum.ADDS_TO_CART_UNIQUE.value,
                                 mtype=FacebookMetricTypeEnum.INSIGHT)
    CHECKOUTS_INITIATED_UNIQUE = Metric(name=FieldsMetadata.checkouts_initiated_unique_total.name,
                                        display_name='Checkouts initiated unique',
                                        numerator=FacebookAvailableSingleMetricsEnum.CHECKOUTS_INITIATED_UNIQUE.value,
                                        mtype=FacebookMetricTypeEnum.INSIGHT)
    WEBSITE_PURCHASES_VALUE = Metric(name=FieldsMetadata.website_purchases_value.name, display_name='Purchases value',
                                     numerator=FacebookAvailableSingleMetricsEnum.WEBSITE_PURCHASES_VALUE.value,
                                     mtype=FacebookMetricTypeEnum.INSIGHT)
    PHOTO_VIEWS = Metric(name=FieldsMetadata.photo_views.name, display_name='Photo views',
                         numerator=FacebookAvailableSingleMetricsEnum.PHOTO_VIEWS.value,
                         mtype=FacebookMetricTypeEnum.INSIGHT)

    CHECKOUTS_INITIATED = Metric(name=FieldsMetadata.website_checkouts_initiated_total.name,
                                 display_name='Checkouts initiated',
                                 numerator=FacebookAvailableSingleMetricsEnum.CHECKOUTS_INITIATED.value,
                                 mtype=FacebookMetricTypeEnum.INSIGHT)

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
