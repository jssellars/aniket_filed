import copy

from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogBase import CatalogBase
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from facebook_business.adobjects.campaign import Campaign
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import (video_views, lead_generation, messages,
                                                                            post_likes, page_likes, traffic,
                                                                            app_installs, store_traffic,
                                                                            conversions_leaf, catalog_sales,
                                                                            brand_awareness, reach)


standard_delivery = CatalogNode('standard', 'Standard')
accelerated_delivery = CatalogNode('no_pacing', 'Accelerated')


lowest_cost = CatalogNode(Campaign.BidStrategy.lowest_cost_without_cap, 'Lowest cost', None, None, [standard_delivery])
lowest_cost_with_bid_cap = CatalogNode(Campaign.BidStrategy.lowest_cost_with_bid_cap, 'Lowest cost with bid cap', None, None, [standard_delivery])
target_cost = CatalogNode(Campaign.BidStrategy.target_cost, 'Target Cost', None, None, [standard_delivery])


video_views_bid = copy.deepcopy(video_views)
video_views_bid.children = [lowest_cost]
video_views_bid.description = None

lead_generation_bid = copy.deepcopy(lead_generation)
lead_generation_bid.children = [lowest_cost]
lead_generation_bid.description = None

messages_bid = copy.deepcopy(messages)
messages_bid.children = [lowest_cost]
messages_bid.description = None

post_likes_bid = copy.deepcopy(post_likes)
post_likes_bid.children = [lowest_cost]
post_likes_bid.description = None

page_likes_bid = copy.deepcopy(page_likes)
page_likes_bid.children = [lowest_cost]
page_likes_bid.description = None

traffic_bid = copy.deepcopy(traffic)
traffic_bid.children = [lowest_cost]
traffic_bid.description = None

app_installs_bid = copy.deepcopy(app_installs)
app_installs_bid.children = [lowest_cost]
app_installs_bid.description = None

store_traffic_bid = copy.deepcopy(store_traffic)
store_traffic_bid.children = [lowest_cost]
store_traffic_bid.description = None

conversions_bid = copy.deepcopy(conversions_leaf)
conversions_bid.children = [lowest_cost]
conversions_bid.description = None

catalog_sales_bid = copy.deepcopy(catalog_sales)
catalog_sales_bid.children = [lowest_cost]
catalog_sales_bid.description = None

brand_awareness_bid = copy.deepcopy(brand_awareness)
brand_awareness_bid.children = [lowest_cost]
brand_awareness_bid.description = None

reach_bid = copy.deepcopy(reach)
reach_bid.children = [lowest_cost]
reach_bid.description = None


class CampaignBidStrategyCatalog(CatalogBase):

    video_views = video_views_bid
    lead_generation = lead_generation_bid
    messages = messages_bid
    post_likes = post_likes_bid
    page_likes = page_likes_bid
    traffic = traffic_bid
    app_installs = app_installs_bid
    store_traffic = store_traffic_bid
    conversions = conversions_bid
    catalog_sales = catalog_sales_bid
    brand_awareness = brand_awareness_bid
    reach = reach_bid