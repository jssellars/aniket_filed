from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.campaign import Campaign

from PotterFacebookCampaignsBuilder.Api.catalogs import objectives
from PotterFacebookCampaignsBuilder.Api.catalogs.base import Base
from PotterFacebookCampaignsBuilder.Api.catalogs.node import Node

_action = AdCreative.CallToActionType


brand_awareness = objectives.brand_awareness.with_children(
    _action.no_button,
    _action.message_page,
    _action.apply_now,
    _action.book_travel,
    _action.contact_us,
    _action.download,
    _action.get_quote,
    _action.get_showtimes,
    _action.learn_more,
    _action.listen_now,
    _action.see_more,
    _action.shop_now,
    _action.sign_up,
    _action.subscribe,
    _action.watch_more,
    _action.whatsapp_message,
)
reach = objectives.reach.with_children(
    _action.no_button,
    _action.message_page,
    _action.apply_now,
    _action.book_travel,
    _action.contact_us,
    _action.download,
    _action.get_quote,
    _action.get_showtimes,
    _action.learn_more,
    _action.listen_now,
    _action.see_more,
    _action.call,
    _action.shop_now,
    _action.get_directions,
    _action.sign_up,
    _action.subscribe,
    _action.watch_more,
    _action.whatsapp_message,
)
traffic_website = objectives.website_traffic.with_children(
    _action.no_button,
    _action.apply_now,
    _action.book_travel,
    _action.contact_us,
    _action.download,
    _action.get_quote,
    _action.get_showtimes,
    _action.learn_more,
    _action.listen_now,
    _action.see_more,
    _action.shop_now,
    _action.sign_up,
    _action.subscribe,
    _action.watch_more,
    _action.whatsapp_message,
    _action.get_offer,
)
post_engagement = objectives.post_likes.with_children(
    _action.no_button,
    _action.get_quote,
    _action.learn_more,
    _action.message_page,
    _action.shop_now,
    _action.whatsapp_message,
)
page_engagement = objectives.page_likes.with_children(_action.like_page)
app_installs = objectives.app_installs.with_children(
    _action.no_button,
    _action.play_game,
    _action.book_travel,
    _action.download,
    _action.learn_more,
    _action.listen_now,
    _action.shop_now,
    _action.sign_up,
    _action.subscribe,
    _action.watch_more,
    _action.install_app,
    _action.use_app,
)
traffic_app = objectives.app_traffic.with_children(
    _action.no_button,
    _action.open_link,
    _action.play_game,
    _action.use_app,
    _action.book_travel,
    _action.learn_more,
    _action.listen_now,
    _action.shop_now,
    _action.subscribe,
    _action.watch_more,
)
video_views = objectives.video_views.with_children(
    _action.message_page,
    _action.book_travel,
    _action.download,
    _action.get_quote,
    _action.get_showtimes,
    _action.learn_more,
    _action.listen_now,
    _action.shop_now,
    _action.sign_up,
    _action.subscribe,
    _action.watch_more,
    _action.whatsapp_message,
)
lead_generation = objectives.lead_generation.with_children(
    _action.apply_now,
    _action.book_travel,
    _action.download,
    _action.get_offer,
    _action.get_quote,
    _action.learn_more,
    _action.sign_up,
    _action.subscribe,
)
conversions = objectives.conversions_leaf.with_children(
    _action.no_button,
    _action.play_game,
    _action.apply_now,
    _action.book_travel,
    _action.contact_us,
    _action.download,
    _action.get_quote,
    _action.get_showtimes,
    _action.learn_more,
    _action.listen_now,
    _action.see_more,
    _action.shop_now,
    _action.sign_up,
    _action.subscribe,
    _action.watch_more,
    _action.whatsapp_message,
    _action.get_offer,
)
catalog_sales = objectives.catalog_sales.with_children(
    _action.no_button,
    _action.open_link,
    _action.message_page,
    _action.book_travel,
    _action.download,
    _action.get_showtimes,
    _action.learn_more,
    _action.listen_now,
    _action.shop_now,
    _action.sign_up,
    _action.subscribe,
)
engagement = objectives.engagement.with_children(post_engagement, page_engagement)


class CTA(Base):
    A_awareness = Node("AWARENESS", brand_awareness, reach)
    B_consideration = Node("CONSIDERATION", traffic_website, engagement, video_views, lead_generation)
    C_conversions = Node(Campaign.Objective.conversions, catalog_sales, conversions)
    D_app_activity = Node("App Activity", traffic_app, app_installs, conversions)
