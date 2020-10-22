from facebook_business.adobjects.campaign import Campaign

from FacebookCampaignsBuilder.Api.catalogs import objectives
from FacebookCampaignsBuilder.Api.catalogs.base import Base
from FacebookCampaignsBuilder.Api.catalogs.node import Node

standard_delivery = Node("standard")
accelerated_delivery = Node("no_pacing")

lowest_cost = Node(Campaign.BidStrategy.lowest_cost_without_cap, standard_delivery)
lowest_cost_with_bid_cap = Node(Campaign.BidStrategy.lowest_cost_with_bid_cap, standard_delivery)
target_cost = Node(Campaign.BidStrategy.target_cost, standard_delivery)


class BidStrategy(Base):
    video_views = objectives.video_views.with_children(lowest_cost)
    lead_generation = objectives.lead_generation.with_children(lowest_cost)
    messages = objectives.messages.with_children(lowest_cost)
    post_likes = objectives.post_likes.with_children(lowest_cost)
    page_likes = objectives.page_likes.with_children(lowest_cost)
    website_traffic = objectives.website_traffic.with_children(lowest_cost)
    app_traffic = objectives.app_traffic.with_children(lowest_cost)
    app_installs = objectives.app_installs.with_children(lowest_cost)
    store_traffic = objectives.store_traffic.with_children(lowest_cost)
    conversions = objectives.conversions_leaf.with_children(lowest_cost)
    catalog_sales = objectives.catalog_sales.with_children(lowest_cost)
    brand_awareness = objectives.brand_awareness.with_children(lowest_cost)
    reach = objectives.reach.with_children(lowest_cost)
