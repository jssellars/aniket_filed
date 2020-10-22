from facebook_business.adobjects.adcampaigndeliveryestimate import AdCampaignDeliveryEstimate

from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node
from FacebookCampaignsBuilder.Api.catalogs import billing_event

# https://developers.facebook.com/docs/marketing-api/bidding/overview/billing-events/#buying-type-validation

_optimization_goal = AdCampaignDeliveryEstimate.OptimizationGoal
_event = billing_event.BillingEventForBuyingTypeAuction


class OptimizationGoal(Base):
    ad_recall_lift = Node(_optimization_goal.ad_recall_lift)
    app_downloads = Node(_optimization_goal.app_downloads)
    app_installs = Node(_optimization_goal.app_installs)
    brand_awareness = Node(_optimization_goal.brand_awareness)
    clicks = Node(_optimization_goal.clicks)
    derived_events = Node(_optimization_goal.derived_events)
    engaged_users = Node(_optimization_goal.engaged_users)
    event_responses = Node(_optimization_goal.event_responses)
    impressions = Node(_optimization_goal.impressions)
    landing_page_views = Node(_optimization_goal.landing_page_views)
    lead_generation = Node(_optimization_goal.lead_generation)
    link_clicks = Node(_optimization_goal.link_clicks)
    offer_claims = Node(_optimization_goal.offer_claims)
    offsite_conversions = Node(_optimization_goal.offsite_conversions)
    page_engagement = Node(_optimization_goal.page_engagement)
    page_likes = Node(_optimization_goal.page_likes)
    post_engagement = Node(_optimization_goal.post_engagement)
    reach = Node(_optimization_goal.reach)
    replies = Node(_optimization_goal.replies)
    social_impressions = Node(_optimization_goal.social_impressions)
    thruplay = Node(_optimization_goal.thruplay)
    two_second_continuous_video_views = Node(_optimization_goal.two_second_continuous_video_views)
    value = Node(_optimization_goal.value)
    visit_instagram_profile = Node(_optimization_goal.visit_instagram_profile)


class OptimizationGoalWithBillingEvents(Base):
    app_installs = OptimizationGoal.app_installs.with_children(_event.impressions, _event.app_installs)
    ad_recall_lift = OptimizationGoal.ad_recall_lift.with_children(_event.impressions)
    engaged_users = OptimizationGoal.engaged_users.with_children(_event.impressions)
    event_responses = OptimizationGoal.event_responses.with_children(_event.impressions)
    impressions = OptimizationGoal.impressions.with_children(_event.impressions)
    lead_generation = OptimizationGoal.lead_generation.with_children(_event.impressions)
    link_clicks = OptimizationGoal.link_clicks.with_children(_event.link_clicks, _event.impressions)
    offsite_conversions = OptimizationGoal.offsite_conversions.with_children(_event.impressions)
    page_likes = OptimizationGoal.page_likes.with_children(_event.impressions)
    post_engagement = OptimizationGoal.post_engagement.with_children(_event.impressions)
    reach = OptimizationGoal.reach.with_children(_event.impressions)
    replies = OptimizationGoal.replies.with_children(_event.impressions)
    social_impressions = OptimizationGoal.social_impressions.with_children(_event.impressions)
    thruplay = OptimizationGoal.thruplay.with_children(_event.impressions, _event.thruplay)
    two_second_continuous_video_views = OptimizationGoal.two_second_continuous_video_views.with_children(
        _event.impressions
    )
    value = OptimizationGoal.value.with_children(_event.impressions)
    landing_page_views = OptimizationGoal.landing_page_views.with_children(_event.impressions)
