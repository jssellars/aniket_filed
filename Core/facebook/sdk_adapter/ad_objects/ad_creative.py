from enum import Enum

from facebook_business.adobjects.adcreative import AdCreative

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# https://developers.facebook.com/docs/marketing-api/dynamic-product-ads/ads-management/#deep-link

_applink_treatment = AdCreative.ApplinkTreatment


@cat_enum
class ApplinkTreatment(Enum):
    DEEPLINK_WITH_APPSTORE_FALLBACK = Cat(_applink_treatment.deeplink_with_appstore_fallback)
    DEEPLINK_WITH_WEB_FALLBACK = Cat(_applink_treatment.deeplink_with_web_fallback)
    WEB_ONLY = Cat(_applink_treatment.web_only)


# https://developers.facebook.com/docs/marketing-api/reference/ad-creative-link-data-call-to-action/

_cta = AdCreative.CallToActionType


@cat_enum
class CallToActionType(Enum):
    ADD_TO_CART = Cat(_cta.add_to_cart)
    APPLY_NOW = Cat(_cta.apply_now)
    BOOK_TRAVEL = Cat(_cta.book_travel, display_name="Book Now")
    BUY = Cat(_cta.buy)
    BUY_NOW = Cat(_cta.buy_now)
    BUY_TICKETS = Cat(_cta.buy_tickets)
    CALL = Cat(_cta.call, display_name="Call Now")
    CALL_ME = Cat(_cta.call_me)
    CONTACT = Cat(_cta.contact)
    CONTACT_US = Cat(_cta.contact_us)
    DONATE = Cat(_cta.donate)
    DONATE_NOW = Cat(_cta.donate_now)
    DOWNLOAD = Cat(_cta.download)
    EVENT_RSVP = Cat(_cta.event_rsvp)
    FIND_A_GROUP = Cat(_cta.find_a_group)
    FIND_YOUR_GROUPS = Cat(_cta.find_your_groups)
    FOLLOW_NEWS_STORYLINE = Cat(_cta.follow_news_storyline)
    FOLLOW_PAGE = Cat("FOLLOW_PAGE")
    FOLLOW_USER = Cat(_cta.follow_user)
    GET_DIRECTIONS = Cat(_cta.get_directions)
    GET_OFFER = Cat(_cta.get_offer)
    GET_OFFER_VIEW = Cat(_cta.get_offer_view)
    GET_QUOTE = Cat(_cta.get_quote)
    GET_SHOWTIMES = Cat(_cta.get_showtimes)
    INSTALL_APP = Cat(_cta.install_app, display_name="Install Now")
    INSTALL_MOBILE_APP = Cat(_cta.install_mobile_app)
    LEARN_MORE = Cat(_cta.learn_more)
    LIKE_PAGE = Cat(_cta.like_page, display_name="Like")
    LISTEN_MUSIC = Cat(_cta.listen_music)
    LISTEN_NOW = Cat(_cta.listen_now)
    MESSAGE_PAGE = Cat(_cta.message_page, display_name="Send Message")
    MOBILE_DOWNLOAD = Cat(_cta.mobile_download)
    MOMENTS = Cat(_cta.moments)
    NO_BUTTON = Cat(_cta.no_button)
    OPEN_LINK = Cat(_cta.open_link)
    ORDER_NOW = Cat(_cta.order_now)
    PAY_TO_ACCESS = Cat(_cta.pay_to_access)
    PLAY_GAME = Cat(_cta.play_game)
    PURCHASE_GIFT_CARDS = Cat(_cta.purchase_gift_cards)
    RECORD_NOW = Cat(_cta.record_now)
    REFER_FRIENDS = Cat("REFER_FRIENDS")
    REQUEST_TIME = Cat(_cta.request_time)
    SAY_THANKS = Cat(_cta.say_thanks)
    SEE_MORE = Cat(_cta.see_more, display_name="See Menu")
    SELL_NOW = Cat(_cta.sell_now)
    SEND_A_GIFT = Cat("SEND_A_GIFT")
    SHARE = Cat(_cta.share)
    SHOP_NOW = Cat(_cta.shop_now)
    SIGN_UP = Cat(_cta.sign_up)
    SOTTO_SUBSCRIBE = Cat(_cta.sotto_subscribe)
    SUBSCRIBE = Cat(_cta.subscribe)
    SWIPE_UP_PRODUCT = Cat("SWIPE_UP_PRODUCT")
    SWIPE_UP_SHOP = Cat("SWIPE_UP_SHOP")
    UPDATE_APP = Cat(_cta.update_app)
    USE_APP = Cat(_cta.use_app)
    USE_MOBILE_APP = Cat(_cta.use_mobile_app)
    VIDEO_ANNOTATION = Cat(_cta.video_annotation)
    VISIT_PAGES_FEED = Cat(_cta.visit_pages_feed)
    WATCH_MORE = Cat(_cta.watch_more)
    WATCH_VIDEO = Cat(_cta.watch_video)
    WHATSAPP_MESSAGE = Cat(_cta.whatsapp_message)
    WOODHENGE_SUPPORT = Cat(_cta.woodhenge_support)
