import copy

from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.campaign import Campaign

from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogBase import CatalogBase
from Potter.FacebookCampaignsBuilder.Api.Catalogs.CatalogNode import CatalogNode
from Potter.FacebookCampaignsBuilder.Api.Catalogs.ObjectivesCatalog import brand_awareness, reach, engagement, \
    video_views, lead_generation, post_likes, page_likes, catalog_sales, conversions_leaf, app_installs, app_traffic, \
    website_traffic

add_to_cart = CatalogNode(AdCreative.CallToActionType.add_to_cart, 'Add to Cart')
apply_now = CatalogNode(AdCreative.CallToActionType.apply_now, 'Apply Now')
book_travel = CatalogNode(AdCreative.CallToActionType.book_travel, 'Book Now')
buy = CatalogNode(AdCreative.CallToActionType.buy, 'Buy')
buy_now = CatalogNode(AdCreative.CallToActionType.buy_now, 'Buy Now')
buy_tickets = CatalogNode(AdCreative.CallToActionType.buy_tickets, 'Buy Tickets')
call = CatalogNode(AdCreative.CallToActionType.call, 'Call Now')
call_me = CatalogNode(AdCreative.CallToActionType.call_me, 'Call Me')
contact = CatalogNode(AdCreative.CallToActionType.contact, 'Contact')
contact_us = CatalogNode(AdCreative.CallToActionType.contact_us, 'Contact Us')
donate = CatalogNode(AdCreative.CallToActionType.donate, 'Donate')
donate_now = CatalogNode(AdCreative.CallToActionType.donate_now, 'Donate Now')
download = CatalogNode(AdCreative.CallToActionType.download, 'Download')
find_a_group = CatalogNode(AdCreative.CallToActionType.find_a_group, 'Find a Group')
find_your_groups = CatalogNode(AdCreative.CallToActionType.find_your_groups, 'Find Your Groups')
follow_news_storyline = CatalogNode(AdCreative.CallToActionType.follow_news_storyline, 'Follow News Storyline')
get_directions = CatalogNode(AdCreative.CallToActionType.get_directions, 'Get Directions')
get_offer = CatalogNode(AdCreative.CallToActionType.get_offer, 'Get Offer')
get_offer_view = CatalogNode(AdCreative.CallToActionType.get_offer_view, 'Get Offer View')
get_quote = CatalogNode(AdCreative.CallToActionType.get_quote, 'Get Quote')
get_showtimes = CatalogNode(AdCreative.CallToActionType.get_showtimes, 'Get Showtimes')
install_app = CatalogNode(AdCreative.CallToActionType.install_app, 'Install Now')
install_mobile_app = CatalogNode(AdCreative.CallToActionType.install_mobile_app, 'Install Now')
learn_more = CatalogNode(AdCreative.CallToActionType.learn_more, 'Learn More')
like_page = CatalogNode(AdCreative.CallToActionType.like_page, 'Like')
listen_music = CatalogNode(AdCreative.CallToActionType.listen_music, 'Listen Music')
listen_now = CatalogNode(AdCreative.CallToActionType.listen_now, 'Listen Now')
message_page = CatalogNode(AdCreative.CallToActionType.message_page, 'Send Message')
mobile_download = CatalogNode(AdCreative.CallToActionType.mobile_download, 'Mobile Download')
moments = CatalogNode(AdCreative.CallToActionType.moments, 'Moments')
no_button = CatalogNode(AdCreative.CallToActionType.no_button, 'No Button')
open_link = CatalogNode(AdCreative.CallToActionType.open_link, 'Open Link')
order_now = CatalogNode(AdCreative.CallToActionType.order_now, 'Order Now')
play_game = CatalogNode(AdCreative.CallToActionType.play_game, 'Play Game')
record_now = CatalogNode(AdCreative.CallToActionType.record_now, 'Record Now')
say_thanks = CatalogNode(AdCreative.CallToActionType.say_thanks, 'Say thanks')
see_menu = CatalogNode(AdCreative.CallToActionType.see_more, 'See Menu')
sell_now = CatalogNode(AdCreative.CallToActionType.see_more, 'Sell Now')
share = CatalogNode(AdCreative.CallToActionType.share, 'Share')
shop_now = CatalogNode(AdCreative.CallToActionType.shop_now, 'Shop Now')
sign_up = CatalogNode(AdCreative.CallToActionType.sign_up, 'Sign Up')
subscribe = CatalogNode(AdCreative.CallToActionType.subscribe, 'Subscribe')
update_app = CatalogNode(AdCreative.CallToActionType.update_app, 'Update App')
use_app = CatalogNode(AdCreative.CallToActionType.use_app, 'Use App')
use_mobile_app = CatalogNode(AdCreative.CallToActionType.use_mobile_app, 'Use Mobile App')
video_annotation = CatalogNode(AdCreative.CallToActionType.video_annotation, 'Video Annotation')
visit_pages_feed = CatalogNode(AdCreative.CallToActionType.visit_pages_feed, 'Visit Pages Feed')
watch_more = CatalogNode(AdCreative.CallToActionType.watch_more, 'Watch More')
watch_video = CatalogNode(AdCreative.CallToActionType.watch_video, 'Watch Video')
whatsapp_message = CatalogNode(AdCreative.CallToActionType.whatsapp_message, 'Send Whatsapp Message')


brand_awareness_cta = copy.deepcopy(brand_awareness)
brand_awareness_cta.image_name = None
brand_awareness_cta.description = None
brand_awareness_cta.children = [no_button, message_page, apply_now, book_travel, contact_us, download, get_quote,
                                get_showtimes, learn_more, listen_now, see_menu, shop_now, sign_up, subscribe,
                                watch_more, whatsapp_message]

reach_cta = copy.deepcopy(reach)
reach_cta.image_name = None
reach_cta.description = None
reach_cta.children = [no_button, message_page, apply_now, book_travel, contact_us, download, get_quote, get_showtimes,
                      learn_more, listen_now, see_menu, call, shop_now, get_directions, sign_up, subscribe, watch_more,
                      whatsapp_message]

traffic_website_cta = copy.deepcopy(website_traffic)
traffic_website_cta.image_name = None
traffic_website_cta.description = None
traffic_website_cta.children = [no_button, apply_now, book_travel, contact_us, download, get_quote, get_showtimes,
                                learn_more, listen_now, see_menu, shop_now, sign_up, subscribe, watch_more,
                                whatsapp_message, get_offer]

post_engagement_cta = copy.deepcopy(post_likes)
post_engagement_cta.image_name = None
post_engagement_cta.description = None
post_engagement_cta.children = [no_button, get_quote, learn_more, message_page, shop_now, whatsapp_message]

page_engagement_cta = copy.deepcopy(page_likes)
page_engagement_cta.image_name = None
page_engagement_cta.description = None
page_engagement_cta.children = [like_page]

app_installs_cta = copy.deepcopy(app_installs)
app_installs_cta.image_name = None
app_installs_cta.description = None
app_installs_cta.children = [no_button, play_game, book_travel, download, learn_more, listen_now, shop_now, sign_up,
                             subscribe, watch_more, install_app, use_app]

traffic_app_cta = copy.deepcopy(app_traffic)
traffic_app_cta.image_name = None
traffic_app_cta.description = None
traffic_app_cta.children = [no_button, open_link, play_game, use_app, book_travel, learn_more, listen_now, shop_now,
                            subscribe, watch_more]

video_views_cta = copy.deepcopy(video_views)
video_views_cta.image_name = None
video_views_cta.description = None
video_views_cta.children = [message_page, book_travel, download, get_quote, get_showtimes, learn_more, listen_now,
                            shop_now, sign_up, subscribe, watch_more, whatsapp_message]

lead_generation_cta = copy.deepcopy(lead_generation)
lead_generation_cta.image_name = None
lead_generation_cta.description = None
lead_generation_cta.children = [apply_now, book_travel, download, get_offer, get_quote, learn_more, sign_up, subscribe]


conversions_cta = copy.deepcopy(conversions_leaf)
conversions_cta.image_name = None
conversions_cta.description = None
conversions_cta.children = [no_button, play_game, apply_now, book_travel, contact_us, download, get_quote,
                            get_showtimes, learn_more, listen_now, see_menu, shop_now, sign_up, subscribe,
                            watch_more, whatsapp_message, get_offer]


catalog_sales_cta = copy.deepcopy(catalog_sales)
catalog_sales_cta.description = None
catalog_sales_cta.image_name = None
catalog_sales_cta.children = [no_button, open_link, message_page, book_travel, download, get_showtimes,
                              learn_more, listen_now, shop_now, sign_up, subscribe]

engagement_cta = copy.deepcopy(engagement)
engagement_cta.description = None
engagement_cta.image_name = None
engagement_cta.children = [post_engagement_cta, page_engagement_cta]


class CTACatalog(CatalogBase):

    A_awareness = CatalogNode('AWARENESS', 'Awareness', 'awareness', None, [brand_awareness_cta, reach_cta])

    B_consideration = CatalogNode('CONSIDERATION', 'Consideration', 'consideration', None, [traffic_website_cta,
                                                                                            engagement_cta,
                                                                                            video_views_cta,
                                                                                            lead_generation_cta])

    C_conversions = CatalogNode(Campaign.Objective.conversions, 'Conversions', 'conversions',
                              None, [catalog_sales_cta, conversions_cta])

    D_app_activity = CatalogNode('App Activity', 'App Activity', 'appactivity', None,
                                 [traffic_app_cta, app_installs_cta, conversions_cta])
