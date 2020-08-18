import copy

from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.campaign import Campaign

from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogBase import CatalogBase
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import brand_awareness, reach, engagement, \
    video_views, lead_generation, post_likes, page_likes, catalog_sales, conversions_leaf, app_installs, app_traffic, \
    website_traffic

add_to_cart = CatalogNode(AdCreative.CallToActionType.add_to_cart)
apply_now = CatalogNode(AdCreative.CallToActionType.apply_now)
book_travel = CatalogNode(AdCreative.CallToActionType.book_travel)
buy = CatalogNode(AdCreative.CallToActionType.buy)
buy_now = CatalogNode(AdCreative.CallToActionType.buy_now)
buy_tickets = CatalogNode(AdCreative.CallToActionType.buy_tickets)
call = CatalogNode(AdCreative.CallToActionType.call)
call_me = CatalogNode(AdCreative.CallToActionType.call_me)
contact = CatalogNode(AdCreative.CallToActionType.contact)
contact_us = CatalogNode(AdCreative.CallToActionType.contact_us)
donate = CatalogNode(AdCreative.CallToActionType.donate)
donate_now = CatalogNode(AdCreative.CallToActionType.donate_now)
download = CatalogNode(AdCreative.CallToActionType.download)
find_a_group = CatalogNode(AdCreative.CallToActionType.find_a_group)
find_your_groups = CatalogNode(AdCreative.CallToActionType.find_your_groups)
follow_news_storyline = CatalogNode(AdCreative.CallToActionType.follow_news_storyline)
get_directions = CatalogNode(AdCreative.CallToActionType.get_directions)
get_offer = CatalogNode(AdCreative.CallToActionType.get_offer)
get_offer_view = CatalogNode(AdCreative.CallToActionType.get_offer_view)
get_quote = CatalogNode(AdCreative.CallToActionType.get_quote)
get_showtimes = CatalogNode(AdCreative.CallToActionType.get_showtimes)
install_app = CatalogNode(AdCreative.CallToActionType.install_app)
install_mobile_app = CatalogNode(AdCreative.CallToActionType.install_mobile_app)
learn_more = CatalogNode(AdCreative.CallToActionType.learn_more)
like_page = CatalogNode(AdCreative.CallToActionType.like_page)
listen_music = CatalogNode(AdCreative.CallToActionType.listen_music)
listen_now = CatalogNode(AdCreative.CallToActionType.listen_now)
message_page = CatalogNode(AdCreative.CallToActionType.message_page)
mobile_download = CatalogNode(AdCreative.CallToActionType.mobile_download)
moments = CatalogNode(AdCreative.CallToActionType.moments)
no_button = CatalogNode(AdCreative.CallToActionType.no_button)
open_link = CatalogNode(AdCreative.CallToActionType.open_link)
order_now = CatalogNode(AdCreative.CallToActionType.order_now)
play_game = CatalogNode(AdCreative.CallToActionType.play_game)
record_now = CatalogNode(AdCreative.CallToActionType.record_now)
say_thanks = CatalogNode(AdCreative.CallToActionType.say_thanks)
see_menu = CatalogNode(AdCreative.CallToActionType.see_more)
sell_now = CatalogNode(AdCreative.CallToActionType.see_more)
share = CatalogNode(AdCreative.CallToActionType.share)
shop_now = CatalogNode(AdCreative.CallToActionType.shop_now)
sign_up = CatalogNode(AdCreative.CallToActionType.sign_up)
subscribe = CatalogNode(AdCreative.CallToActionType.subscribe)
update_app = CatalogNode(AdCreative.CallToActionType.update_app)
use_app = CatalogNode(AdCreative.CallToActionType.use_app)
use_mobile_app = CatalogNode(AdCreative.CallToActionType.use_mobile_app)
video_annotation = CatalogNode(AdCreative.CallToActionType.video_annotation)
visit_pages_feed = CatalogNode(AdCreative.CallToActionType.visit_pages_feed)
watch_more = CatalogNode(AdCreative.CallToActionType.watch_more)
watch_video = CatalogNode(AdCreative.CallToActionType.watch_video)
whatsapp_message = CatalogNode(AdCreative.CallToActionType.whatsapp_message)


brand_awareness_cta = copy.deepcopy(brand_awareness)
brand_awareness_cta.children = [no_button, message_page, apply_now, book_travel, contact_us, download, get_quote,
                                get_showtimes, learn_more, listen_now, see_menu, shop_now, sign_up, subscribe,
                                watch_more, whatsapp_message]

reach_cta = copy.deepcopy(reach)
reach_cta.children = [no_button, message_page, apply_now, book_travel, contact_us, download, get_quote, get_showtimes,
                      learn_more, listen_now, see_menu, call, shop_now, get_directions, sign_up, subscribe, watch_more,
                      whatsapp_message]

traffic_website_cta = copy.deepcopy(website_traffic)
traffic_website_cta.children = [no_button, apply_now, book_travel, contact_us, download, get_quote, get_showtimes,
                                learn_more, listen_now, see_menu, shop_now, sign_up, subscribe, watch_more,
                                whatsapp_message, get_offer]

post_engagement_cta = copy.deepcopy(post_likes)
post_engagement_cta.children = [no_button, get_quote, learn_more, message_page, shop_now, whatsapp_message]

page_engagement_cta = copy.deepcopy(page_likes)
page_engagement_cta.children = [like_page]

app_installs_cta = copy.deepcopy(app_installs)
app_installs_cta.children = [no_button, play_game, book_travel, download, learn_more, listen_now, shop_now, sign_up,
                             subscribe, watch_more, install_app, use_app]

traffic_app_cta = copy.deepcopy(app_traffic)
traffic_app_cta.children = [no_button, open_link, play_game, use_app, book_travel, learn_more, listen_now, shop_now,
                            subscribe, watch_more]

video_views_cta = copy.deepcopy(video_views)
video_views_cta.children = [message_page, book_travel, download, get_quote, get_showtimes, learn_more, listen_now,
                            shop_now, sign_up, subscribe, watch_more, whatsapp_message]

lead_generation_cta = copy.deepcopy(lead_generation)
lead_generation_cta.children = [apply_now, book_travel, download, get_offer, get_quote, learn_more, sign_up, subscribe]


conversions_cta = copy.deepcopy(conversions_leaf)
conversions_cta.children = [no_button, play_game, apply_now, book_travel, contact_us, download, get_quote,
                            get_showtimes, learn_more, listen_now, see_menu, shop_now, sign_up, subscribe,
                            watch_more, whatsapp_message, get_offer]


catalog_sales_cta = copy.deepcopy(catalog_sales)
catalog_sales_cta.children = [no_button, open_link, message_page, book_travel, download, get_showtimes,
                              learn_more, listen_now, shop_now, sign_up, subscribe]

engagement_cta = copy.deepcopy(engagement)
engagement_cta.children = [post_engagement_cta, page_engagement_cta]


class CTACatalog(CatalogBase):

    A_awareness = CatalogNode('AWARENESS', [brand_awareness_cta, reach_cta])

    B_consideration = CatalogNode('CONSIDERATION', [traffic_website_cta, engagement_cta, video_views_cta,
                                                    lead_generation_cta])

    C_conversions = CatalogNode(Campaign.Objective.conversions, [catalog_sales_cta, conversions_cta])

    D_app_activity = CatalogNode('App Activity',
                                 [traffic_app_cta, app_installs_cta, conversions_cta])
