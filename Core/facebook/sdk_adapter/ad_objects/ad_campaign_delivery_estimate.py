from enum import Enum

from facebook_business.adobjects.adcampaigndeliveryestimate import AdCampaignDeliveryEstimate

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# https://developers.facebook.com/docs/marketing-api/bidding/overview/billing-events/#buying-type-validation

_optimization_goal = AdCampaignDeliveryEstimate.OptimizationGoal


@cat_enum
class OptimizationGoal(Enum):
    AD_RECALL_LIFT = Cat(_optimization_goal.ad_recall_lift)
    APP_DOWNLOADS = Cat(_optimization_goal.app_downloads)  # no billing events?
    APP_INSTALLS = Cat(_optimization_goal.app_installs)
    BRAND_AWARENESS = Cat(_optimization_goal.brand_awareness)  # no billing events?
    CLICKS = Cat(_optimization_goal.clicks)  # no billing events?
    DERIVED_EVENTS = Cat(_optimization_goal.derived_events)  # no billing events?
    ENGAGED_USERS = Cat(_optimization_goal.engaged_users)
    EVENT_RESPONSES = Cat(_optimization_goal.event_responses)
    IMPRESSIONS = Cat(_optimization_goal.impressions)
    LANDING_PAGE_VIEWS = Cat(_optimization_goal.landing_page_views)
    LEAD_GENERATION = Cat(_optimization_goal.lead_generation)
    LINK_CLICKS = Cat(_optimization_goal.link_clicks)
    OFFER_CLAIMS = Cat(_optimization_goal.offer_claims)  # no billing events?
    OFFSITE_CONVERSIONS = Cat(_optimization_goal.offsite_conversions)
    PAGE_ENGAGEMENT = Cat(_optimization_goal.page_engagement)  # no billing events?
    PAGE_LIKES = Cat(_optimization_goal.page_likes)
    POST_ENGAGEMENT = Cat(_optimization_goal.post_engagement)
    REACH = Cat(_optimization_goal.reach)
    REPLIES = Cat(_optimization_goal.replies)
    SOCIAL_IMPRESSIONS = Cat(_optimization_goal.social_impressions)
    THRUPLAY = Cat(_optimization_goal.thruplay)
    TWO_SECOND_CONTINUOUS_VIDEO_VIEWS = Cat(_optimization_goal.two_second_continuous_video_views)
    VALUE = Cat(_optimization_goal.value)
    VISIT_INSTAGRAM_PROFILE = Cat(_optimization_goal.visit_instagram_profile)  # no billing events?
