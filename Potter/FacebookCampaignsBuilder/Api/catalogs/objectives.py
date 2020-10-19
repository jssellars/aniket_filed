from facebook_business.adobjects.campaign import Campaign

from Potter.FacebookCampaignsBuilder.Api.catalogs.base import Base
from Potter.FacebookCampaignsBuilder.Api.catalogs.node import Node

_objective = Campaign.Objective

# Conversions children
store_traffic = Node(_objective.local_awareness)
conversions_leaf = Node(_objective.conversions)
catalog_sales = Node(_objective.product_catalog_sales)

# Awareness Children
brand_awareness = Node(_objective.brand_awareness)
reach = Node(_objective.reach)

# App Activity children
app_traffic = Node(_objective.link_clicks)
app_installs = Node(_objective.app_installs)

# Engagement children
post_likes = Node(_objective.post_engagement)
page_likes = Node(_objective.page_likes)

# Event responses is not selectable yet
event_responses = Node(_objective.event_responses)

# Consideration Children
engagement = Node("ENGAGEMENT", post_likes, page_likes)
video_views = Node(_objective.video_views)
lead_generation = Node(_objective.lead_generation)
messages = Node(_objective.messages)
website_traffic = Node(_objective.link_clicks)


class Objectives(Base):
    A_awareness = Node("AWARENESS", brand_awareness, reach)
    # The messages objective is also conceptually here, but we do not support it (yet)
    B_consideration = Node("CONSIDERATION", website_traffic, engagement, video_views, lead_generation)
    # The store traffic objective is also conceptually here, but we do not support it (yet)
    C_conversions = Node(_objective.conversions, catalog_sales, conversions_leaf)
    D_app_activity = Node("App Activity", app_traffic, app_installs, conversions_leaf)
