from facebook_business.adobjects.adset import AdSet

from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node
from FacebookCampaignsBuilder.Api.catalogs.buying_type import BuyingType

# https://developers.facebook.com/docs/marketing-api/bidding/overview/billing-events/#buying-type-validation

_billing_event = AdSet.BillingEvent
buying_types = "BUYING_TYPES"


class BillingEvent(Base):
    app_installs = Node(_billing_event.app_installs)
    clicks = Node(_billing_event.clicks)
    impressions = Node(_billing_event.impressions)
    link_clicks = Node(_billing_event.link_clicks)
    offer_claims = Node(_billing_event.offer_claims)
    page_likes = Node(_billing_event.page_likes)
    post_engagement = Node(_billing_event.post_engagement)
    thruplay = Node(_billing_event.thruplay)


class BillingEventForBuyingTypeAuction(Base):
    app_installs = BillingEvent.app_installs.with_children(BuyingType.auction)
    impressions = BillingEvent.impressions.with_children(BuyingType.auction)
    link_clicks = BillingEvent.link_clicks.with_children(BuyingType.auction)
    page_likes = BillingEvent.page_likes.with_children(BuyingType.auction)
    post_engagement = BillingEvent.post_engagement.with_children(BuyingType.auction)
    thruplay = BillingEvent.thruplay.with_children(BuyingType.auction)


class BillingEventForBuyingTypeReserved(Base):
    app_installs = BillingEvent.app_installs.with_children(BuyingType.reserved)


class BillingEventForBuyingTypeFixedCpm(Base):
    app_installs = BillingEvent.app_installs.with_children(BuyingType.fixed_cpm)
