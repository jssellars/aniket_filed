from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogBase import CatalogBase
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from facebook_business.adobjects.campaign import Campaign

# Conversions children
store_traffic = CatalogNode(Campaign.Objective.local_awareness)

conversions_leaf = CatalogNode(Campaign.Objective.conversions)

catalog_sales = CatalogNode(Campaign.Objective.product_catalog_sales)

# Awareness Children
brand_awareness = CatalogNode(Campaign.Objective.brand_awareness)

reach = CatalogNode(Campaign.Objective.reach)

# App Activity children

app_traffic = CatalogNode(Campaign.Objective.link_clicks)
app_installs = CatalogNode(Campaign.Objective.app_installs)


# engagement children
post_likes = CatalogNode(Campaign.Objective.post_engagement)
page_likes = CatalogNode(Campaign.Objective.page_likes)
# event responses is not selectable yet
event_responses = CatalogNode(Campaign.Objective.event_responses)

# Consideration Children
engagement = CatalogNode('ENGAGEMENT', [post_likes, page_likes])
video_views = CatalogNode(Campaign.Objective.video_views)

lead_generation = CatalogNode(Campaign.Objective.lead_generation)

messages = CatalogNode(Campaign.Objective.messages)

website_traffic = CatalogNode(Campaign.Objective.link_clicks)


class ObjectivesCatalog(CatalogBase):

    A_awareness = CatalogNode('AWARENESS', [brand_awareness, reach])

    # The messages objective is also conceptually here, but we do not support it (yet)
    B_consideration = CatalogNode('CONSIDERATION', [website_traffic, engagement, video_views, lead_generation])

    # The store traffic objective is also conceptually here, but we do not support it (yet)
    C_conversions = CatalogNode(Campaign.Objective.conversions, [catalog_sales, conversions_leaf])

    D_app_activity = CatalogNode('App Activity', [app_traffic, app_installs, conversions_leaf])


