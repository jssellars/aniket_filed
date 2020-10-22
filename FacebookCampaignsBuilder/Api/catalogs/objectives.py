from facebook_business.adobjects.campaign import Campaign

from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node
from FacebookCampaignsBuilder.Api.catalogs import optimization_goal


# https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group#parameters-2
# https://www.facebook.com/business/help/1438417719786914
# https://developers.facebook.com/docs/marketing-api/bidding/overview#opt

_objective = Campaign.Objective
_goal = optimization_goal.OptimizationGoalWithBillingEvents
goals = "OPTIMIZATON_GOALS_FOR_ALL"
goals_instant_experiences_app = "OPTIMIZATON_GOALS_FOR_INSTANT_EXPERIENCES_APP"
goals_mobile_app = "OPTIMIZATON_GOALS_FOR_MOBILE_APP"
goals_event = "OPTIMIZATON_GOALS_FOR_EVENT"
goals_page_post = "OPTIMIZATON_GOALS_FOR_PAGE_POST"

# Conversions
store_traffic = Node(_objective.local_awareness)
conversions_leaf = Node(
    _objective.conversions,
    Node(
        goals,
        _goal.offsite_conversions,
        _goal.impressions,
        _goal.post_engagement,
        _goal.reach,
        _goal.social_impressions,
        _goal.value,
        _goal.landing_page_views,
        _goal.link_clicks,
    ),
)
catalog_sales = Node(
    _objective.product_catalog_sales,
    Node(
        goals,
        _goal.offsite_conversions,
        _goal.impressions,
        _goal.post_engagement,
        _goal.offsite_conversions,
        _goal.reach,
        _goal.link_clicks,
    ),
)

# Awareness
brand_awareness = Node(_objective.brand_awareness, Node(goals, _goal.ad_recall_lift))
reach = Node(_objective.reach, Node(goals, _goal.reach, _goal.impressions))

# App Activity
app_traffic = Node(
    _objective.link_clicks,
    Node(goals, _goal.link_clicks, _goal.impressions, _goal.post_engagement, _goal.reach, _goal.landing_page_views),
    Node(
        goals_instant_experiences_app,
        _goal.engaged_users,
        _goal.app_installs,
        _goal.impressions,
        _goal.post_engagement,
        _goal.reach,
    ),
    Node(goals_mobile_app, _goal.link_clicks, _goal.impressions, _goal.reach, _goal.offsite_conversions),
)
app_installs = Node(
    _objective.app_installs,
    Node(goals_instant_experiences_app, _goal.app_installs, _goal.impressions, _goal.post_engagement),
    Node(goals_mobile_app, _goal.app_installs, _goal.offsite_conversions, _goal.link_clicks, _goal.reach, _goal.value),
)

# Engagement
post_likes = Node(
    _objective.post_engagement, Node(goals, _goal.post_engagement, _goal.impressions, _goal.reach, _goal.link_clicks)
)
page_likes = Node(
    _objective.page_likes, Node(goals, _goal.page_likes, _goal.impressions, _goal.post_engagement, _goal.reach)
)

# Event responses - not selectable yet
event_responses = Node(
    _objective.event_responses,
    Node(goals_event, _goal.event_responses, _goal.impressions, _goal.reach),
    Node(goals_page_post, _goal.event_responses, _goal.impressions, _goal.post_engagement, _goal.reach),
)

# Consideration
engagement = Node("ENGAGEMENT", post_likes, page_likes)
video_views = Node(_objective.video_views, Node(goals, _goal.thruplay, _goal.two_second_continuous_video_views))
lead_generation = Node(_objective.lead_generation, Node(goals, _goal.lead_generation))
# Default: REPLIES / Other valid: REPLIES (Click-to-Messenger), IMPRESSIONS (Sponsored Messages)
# TODO: see how to include Click-to-Messenger and Sponsored Messages in the structure
messages = Node(_objective.messages, Node(goals, _goal.replies, _goal.impressions))
website_traffic = app_traffic


class Objectives(Base):
    A_awareness = Node("AWARENESS", brand_awareness, reach)
    # The messages objective is also conceptually here, but we do not support it (yet)
    B_consideration = Node("CONSIDERATION", website_traffic, engagement, video_views, lead_generation)
    # The store traffic objective is also conceptually here, but we do not support it (yet)
    C_conversions = Node(_objective.conversions, catalog_sales, conversions_leaf)
    D_app_activity = Node("App Activity", app_traffic, app_installs, conversions_leaf)
