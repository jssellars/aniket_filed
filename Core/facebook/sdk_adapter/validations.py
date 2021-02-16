import collections
from enum import Enum

from typing import Dict, Any

from Core.facebook.sdk_adapter.ad_objects.ad_campaign_delivery_estimate import OptimizationGoal
from Core.facebook.sdk_adapter.ad_objects.ad_creative import CallToActionType
from Core.facebook.sdk_adapter.ad_objects.ad_insights import (
    ActionAttributionWindowClick,
    ActionAttributionWindowView,
)
from Core.facebook.sdk_adapter.ad_objects.ad_preview import AdFormat
from Core.facebook.sdk_adapter.ad_objects.ad_set import BillingEvent, PacingType
from Core.facebook.sdk_adapter.ad_objects.campaign import (
    BidStrategy,
    Objective,
    ObjectiveWithDestination,
)
from Core.facebook.sdk_adapter.ad_objects.content_delivery_report import Placement
from Core.facebook.sdk_adapter.ad_objects.reach_frequency_prediction import BuyingType
from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform
from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group#objective_creative
# https://www.facebook.com/business/ads-guide/
# https://www.facebook.com/business/ads-guide/image/facebook-feed
# https://www.facebook.com/business/ads-guide/video/audience-network-native/app-installs
# https://www.facebook.com/business/ads-guide/carousel/facebook-feed/traffic
# https://www.facebook.com/business/ads-guide/collection/facebook-feed/website-conversions
# https://www.facebook.com/business/help/410873986524407

# TODO: include data from OBJECTIVE_X_PLACEMENT_X_CTA
from Core.facebook.sdk_adapter.validation_models import JointCat

OBJECTIVE_X_CALL_TO_ACTION_TYPE = {
    Objective.APP_INSTALLS: [
        CallToActionType.BOOK_TRAVEL,  # Book Now
        CallToActionType.DOWNLOAD,  # Download
        CallToActionType.INSTALL_APP,  # Install Now
        CallToActionType.LEARN_MORE,  # Learn More
        CallToActionType.LISTEN_NOW,  # Listen Now
        CallToActionType.NO_BUTTON,
        CallToActionType.PLAY_GAME,  # Play Game
        CallToActionType.SHOP_NOW,  # Shop Now
        CallToActionType.SIGN_UP,  # Sign Up
        CallToActionType.SUBSCRIBE,  # Subscribe
        CallToActionType.USE_APP,  # Use App
        CallToActionType.WATCH_MORE,  # Watch More
    ],
    Objective.BRAND_AWARENESS: [
        CallToActionType.APPLY_NOW,  # Apply Now
        CallToActionType.BOOK_TRAVEL,  # Book Now
        CallToActionType.CONTACT_US,  # Contact Us
        CallToActionType.DOWNLOAD,  # Download
        CallToActionType.GET_QUOTE,  # Get Quote
        CallToActionType.GET_SHOWTIMES,  # Get Showtimes
        CallToActionType.LEARN_MORE,  # Learn More
        CallToActionType.LISTEN_NOW,  # Listen Now
        CallToActionType.MESSAGE_PAGE,  # Send Message
        CallToActionType.NO_BUTTON,
        CallToActionType.REQUEST_TIME,  # Request Time
        CallToActionType.SEE_MORE,  # See Menu
        CallToActionType.SHOP_NOW,  # Shop Now
        CallToActionType.SIGN_UP,  # Sign Up
        CallToActionType.SUBSCRIBE,  # Subscribe
        CallToActionType.WATCH_MORE,  # Watch More
        CallToActionType.WHATSAPP_MESSAGE,  # Send WhatsApp Message
    ],
    Objective.CONVERSIONS: [
        # Donate Now  # TODO: find matching value in enum
        CallToActionType.APPLY_NOW,  # Apply Now
        CallToActionType.BOOK_TRAVEL,  # Book Now
        CallToActionType.CONTACT_US,  # Contact Us
        # CallToActionType.DOWNLOAD,  # TODO: see if we still need old catalog value
        CallToActionType.GET_OFFER,  # Get Offer
        CallToActionType.GET_QUOTE,  # Get Quote
        # CallToActionType.GET_SHOWTIMES,  # TODO: see if we still need old catalog value
        CallToActionType.LEARN_MORE,  # Learn More
        # CallToActionType.LISTEN_NOW,  # TODO: see if we still need old catalog value
        CallToActionType.MESSAGE_PAGE,  # Send Message
        CallToActionType.NO_BUTTON,
        CallToActionType.PLAY_GAME,  # Play Game
        # CallToActionType.SEE_MORE,  # TODO: see if we still need old catalog value
        CallToActionType.SHOP_NOW,  # Shop Now
        CallToActionType.SIGN_UP,  # Sign Up
        CallToActionType.SUBSCRIBE,  # Subscribe
        # CallToActionType.WATCH_MORE,  # TODO: see if we still need old catalog value
        # CallToActionType.WHATSAPP_MESSAGE,  # TODO: see if we still need old catalog value
    ],
    Objective.LEAD_GENERATION: [
        CallToActionType.APPLY_NOW,  # Apply Now
        CallToActionType.BOOK_TRAVEL,  # Book Now
        CallToActionType.DOWNLOAD,  # Download
        CallToActionType.GET_OFFER,  # Get Offer
        CallToActionType.GET_QUOTE,  # Get Quote
        CallToActionType.LEARN_MORE,  # Learn More
        CallToActionType.SIGN_UP,  # Sign Up
        CallToActionType.SUBSCRIBE,  # Subscribe
    ],
    Objective.EVENT_RESPONSES: [
        # View Event  # TODO: find matching value in enum
    ],
    Objective.LINK_CLICKS: [
        # Donate Now  # TODO: find matching value in enum
        CallToActionType.APPLY_NOW,  # Apply Now
        CallToActionType.BOOK_TRAVEL,  # Book Now
        CallToActionType.BUY_TICKETS,  # Buy Tickets
        # CallToActionType.CALL,  # Call Now
        CallToActionType.CONTACT_US,  # Contact Us
        CallToActionType.DOWNLOAD,  # Download
        CallToActionType.GET_OFFER,  # Get Offer
        CallToActionType.GET_QUOTE,  # Get Quote
        CallToActionType.GET_SHOWTIMES,  # Get Showtimes
        CallToActionType.LEARN_MORE,  # Learn More
        CallToActionType.LISTEN_NOW,  # Listen Now
        CallToActionType.REQUEST_TIME,  # Request Time
        CallToActionType.SEE_MORE,  # See Menu
        CallToActionType.SHOP_NOW,  # Shop Now
        CallToActionType.SIGN_UP,  # Sign Up
        CallToActionType.SUBSCRIBE,  # Subscribe
        CallToActionType.WATCH_MORE,  # Watch More
    ],
    # TODO: see how to use info below, in old catalogs definition style,
    #  not found in current API docs
    # Objective.LINK_CLICKS_X_APP: [
    #     CallToActionType.BOOK_TRAVEL,
    #     CallToActionType.LEARN_MORE,
    #     CallToActionType.LISTEN_NOW,
    #     CallToActionType.NO_BUTTON,
    #     CallToActionType.OPEN_LINK,
    #     CallToActionType.PLAY_GAME,
    #     CallToActionType.SHOP_NOW,
    #     CallToActionType.SUBSCRIBE,
    #     CallToActionType.USE_APP,
    #     CallToActionType.WATCH_MORE,
    # ],
    # Objective.LINK_CLICKS_X_WEBSITE: [
    #     CallToActionType.APPLY_NOW,
    #     CallToActionType.BOOK_TRAVEL,
    #     CallToActionType.CONTACT_US,
    #     CallToActionType.DOWNLOAD,
    #     CallToActionType.GET_OFFER,
    #     CallToActionType.GET_QUOTE,
    #     CallToActionType.GET_SHOWTIMES,
    #     CallToActionType.LEARN_MORE,
    #     CallToActionType.LISTEN_NOW,
    #     CallToActionType.NO_BUTTON,
    #     CallToActionType.SEE_MORE,
    #     CallToActionType.SHOP_NOW,
    #     CallToActionType.SIGN_UP,
    #     CallToActionType.SUBSCRIBE,
    #     CallToActionType.WATCH_MORE,
    #     CallToActionType.WHATSAPP_MESSAGE,
    # ],
    Objective.MESSAGES: [
        # Donate Now  # TODO: find matching value in enum
        CallToActionType.APPLY_NOW,  # Apply Now
        CallToActionType.BOOK_TRAVEL,  # Book Now
        CallToActionType.CONTACT_US,  # Contact Us
        CallToActionType.GET_OFFER,  # Get Offer
        CallToActionType.GET_QUOTE,  # Get Quote
        CallToActionType.LEARN_MORE,  # Learn More
        CallToActionType.MESSAGE_PAGE,  # Send Message
        CallToActionType.SHOP_NOW,  # Shop Now
        CallToActionType.SIGN_UP,  # Sign Up
        CallToActionType.SUBSCRIBE,  # Subscribe
    ],
    Objective.PAGE_LIKES: [
        CallToActionType.LIKE_PAGE,
    ],  # Like Page
    Objective.POST_ENGAGEMENT: [
        CallToActionType.GET_QUOTE,  # Get Quote
        CallToActionType.LEARN_MORE,  # Learn More
        CallToActionType.MESSAGE_PAGE,  # Send Message
        CallToActionType.NO_BUTTON,
        CallToActionType.SHOP_NOW,  # Shop Now
        CallToActionType.WHATSAPP_MESSAGE,  # Send WhatsApp Message
    ],
    Objective.PRODUCT_CATALOG_SALES: [
        # Donate Now  # TODO: find matching value in enum
        CallToActionType.BOOK_TRAVEL,  # Book Now
        CallToActionType.DOWNLOAD,  # Download
        CallToActionType.GET_SHOWTIMES,  # Get Showtimes
        CallToActionType.LEARN_MORE,  # Learn More
        CallToActionType.LISTEN_NOW,  # Listen Now
        # CallToActionType.MESSAGE_PAGE,  # TODO: see if we still need old catalog value
        CallToActionType.NO_BUTTON,
        CallToActionType.OPEN_LINK,  # Open Link
        CallToActionType.SHOP_NOW,  # Shop Now
        CallToActionType.SIGN_UP,  # Sign Up
        CallToActionType.SUBSCRIBE,  # Subscribe
    ],
    Objective.REACH: [
        CallToActionType.APPLY_NOW,  # Apply Now
        CallToActionType.BOOK_TRAVEL,  # Book Now
        # CallToActionType.CALL,  # TODO: see if we still need old catalog value
        CallToActionType.CONTACT_US,  # Contact Us
        CallToActionType.DOWNLOAD,  # Download
        CallToActionType.GET_DIRECTIONS,  # Get Directions
        CallToActionType.GET_QUOTE,  # Get Quote
        CallToActionType.GET_SHOWTIMES,  # Get Showtimes
        CallToActionType.LEARN_MORE,  # Learn More
        CallToActionType.LISTEN_NOW,  # Listen Now
        CallToActionType.MESSAGE_PAGE,  # Send Message
        CallToActionType.NO_BUTTON,
        CallToActionType.REQUEST_TIME,  # Request Time
        # Save  # TODO: find matching value in enum
        CallToActionType.SEE_MORE,  # See Menu
        CallToActionType.SHOP_NOW,  # Shop Now
        CallToActionType.SIGN_UP,  # Sign Up
        CallToActionType.SUBSCRIBE,  # Subscribe
        CallToActionType.WATCH_MORE,  # Watch More
        CallToActionType.WHATSAPP_MESSAGE,  # Send WhatsApp Message
    ],
    Objective.LOCAL_AWARENESS: [
        # CallToActionType.CALL,  # Call Now
        CallToActionType.GET_DIRECTIONS,  # Get Directions
        CallToActionType.LEARN_MORE,  # Learn More
        CallToActionType.MESSAGE_PAGE,  # Send Message
        CallToActionType.ORDER_NOW,  # Order Now
        CallToActionType.SHOP_NOW,  # Shop Now
    ],
    Objective.VIDEO_VIEWS: [
        CallToActionType.BOOK_TRAVEL,  # Book Now
        CallToActionType.DOWNLOAD,  # Download
        CallToActionType.GET_QUOTE,  # Get Quote
        CallToActionType.GET_SHOWTIMES,  # Get Showtimes
        CallToActionType.LEARN_MORE,  # Learn More
        CallToActionType.LISTEN_NOW,  # Listen Now
        CallToActionType.MESSAGE_PAGE,  # Send Message
        CallToActionType.SHOP_NOW,  # Shop Now
        CallToActionType.SIGN_UP,  # Sign Up
        CallToActionType.SUBSCRIBE,  # Subscribe
        CallToActionType.WATCH_MORE,  # Watch More
        CallToActionType.WHATSAPP_MESSAGE,  # Send WhatsApp Message
    ],
}

PLACEMENT_X_AD_FORMAT = PLATFORM_X_POSITION_X_AD_FORMAT = {
    # TODO: ??? mobile should also be in instagram ???
    Placement.FACEBOOK_FEED: [
        AdFormat.DESKTOP_FEED_STANDARD,
        AdFormat.MOBILE_FEED_STANDARD,
    ],
    Placement.FACEBOOK_RIGHT_COLUMN: [AdFormat.RIGHT_COLUMN_STANDARD],
    Placement.FACEBOOK_INSTANT_ARTICLES: [AdFormat.INSTANT_ARTICLE_STANDARD, AdFormat.INSTANT_ARTICLE_RECIRCULATION_AD],
    Placement.FACEBOOK_IN_STREAM_VIDEO: [AdFormat.INSTREAM_VIDEO_DESKTOP, AdFormat.INSTREAM_VIDEO_MOBILE],
    Placement.FACEBOOK_MARKETPLACE: [AdFormat.MARKETPLACE_MOBILE],
    Placement.FACEBOOK_STORIES: [AdFormat.FACEBOOK_STORY_MOBILE],
    # TODO: ??? mobile_fullwidth not certain ???
    Placement.FACEBOOK_SEARCH_RESULTS: [AdFormat.MOBILE_MEDIUM_RECTANGLE, AdFormat.MOBILE_FULLWIDTH],
    Placement.FACEBOOK_VIDEO_FEEDS: [AdFormat.SUGGESTED_VIDEO_DESKTOP, AdFormat.SUGGESTED_VIDEO_MOBILE],
    Placement.INSTAGRAM_STORIES: [AdFormat.INSTAGRAM_STORY],
    Placement.INSTAGRAM_FEED: [AdFormat.INSTAGRAM_STANDARD],
    Placement.INSTAGRAM_EXPLORE: [AdFormat.INSTAGRAM_EXPLORE_CONTEXTUAL, AdFormat.INSTAGRAM_EXPLORE_IMMERSIVE],
    # TODO: BANNER and INTERSTITIAL apparently not represented in the Placement
    Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [
        AdFormat.MOBILE_NATIVE,
        AdFormat.MOBILE_BANNER,
        AdFormat.MOBILE_INTERSTITIAL,
        AdFormat.MOBILE_MEDIUM_RECTANGLE,
    ],
    Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [
        AdFormat.AUDIENCE_NETWORK_REWARDED_VIDEO,
        AdFormat.AUDIENCE_NETWORK_INSTREAM_VIDEO,
        AdFormat.AUDIENCE_NETWORK_INSTREAM_VIDEO_MOBILE,
        AdFormat.AUDIENCE_NETWORK_OUTSTREAM_VIDEO,
    ],
    # TODO: ??? find SPONSORED_MESSAGE mapping to AdFormat
    Placement.MESSENGER_INBOX: [AdFormat.MESSENGER_MOBILE_INBOX_MEDIA],
    Placement.MESSENGER_STORIES: [AdFormat.MESSENGER_MOBILE_STORY_MEDIA],
}

# TODO: add Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__
OBJECTIVE_X_PLACEMENT_X_DEVICE_PLATFORM = OBJECTIVE_X_PLATFORM_X_POSITION_X_DEVICE_PLATFORM = {
    Objective.APP_INSTALLS: {
        Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_INSTANT_ARTICLES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_VIDEO_FEEDS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.INSTAGRAM_FEED: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_EXPLORE: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_STORIES: [DevicePlatform.MOBILE],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [DevicePlatform.MOBILE],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [DevicePlatform.MOBILE],
    },
    Objective.BRAND_AWARENESS: {
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_VIDEO_FEEDS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_INSTANT_ARTICLES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_FEED: [DevicePlatform.MOBILE],
        # Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        # Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
    },
    Objective.CONVERSIONS: {
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_INSTANT_ARTICLES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_VIDEO_FEEDS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_MARKETPLACE: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_SEARCH_RESULTS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_RIGHT_COLUMN: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.INSTAGRAM_FEED: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_EXPLORE: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_STORIES: [DevicePlatform.MOBILE],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [DevicePlatform.DESKTOP],
        # Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.DESKTOP],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [DevicePlatform.DESKTOP],
    },
    Objective.LEAD_GENERATION: {
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_FEED: [DevicePlatform.MOBILE],
    },
    Objective.LINK_CLICKS: {
        Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_INSTANT_ARTICLES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_MARKETPLACE: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_RIGHT_COLUMN: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_SEARCH_RESULTS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_VIDEO_FEEDS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.INSTAGRAM_FEED: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_EXPLORE: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_STORIES: [DevicePlatform.MOBILE],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        # Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
    },
    Objective.LOCAL_AWARENESS: {
        Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_INSTANT_ARTICLES: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_MARKETPLACE: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_SEARCH_RESULTS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_VIDEO_FEEDS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
    },
    Objective.PAGE_LIKES: {
        Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_INSTANT_ARTICLES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_MARKETPLACE: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_SEARCH_RESULTS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_VIDEO_FEEDS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
    },
    Objective.POST_ENGAGEMENT: {
        # Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_INSTANT_ARTICLES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_MARKETPLACE: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_SEARCH_RESULTS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_VIDEO_FEEDS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.INSTAGRAM_FEED: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_EXPLORE: [DevicePlatform.MOBILE],
        # Placement.INSTAGRAM_STORIES: [DevicePlatform.MOBILE],
    },
    Objective.PRODUCT_CATALOG_SALES: {
        Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_INSTANT_ARTICLES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_MARKETPLACE: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_RIGHT_COLUMN: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_SEARCH_RESULTS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_VIDEO_FEEDS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.INSTAGRAM_FEED: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_EXPLORE: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_STORIES: [DevicePlatform.MOBILE],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        # Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
    },
    Objective.REACH: {
        Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_INSTANT_ARTICLES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_MARKETPLACE: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_SEARCH_RESULTS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_VIDEO_FEEDS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.INSTAGRAM_FEED: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_EXPLORE: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_STORIES: [DevicePlatform.MOBILE],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        # Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
    },
    Objective.VIDEO_VIEWS: {
        Placement.FACEBOOK_STORIES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_FEED: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_INSTANT_ARTICLES: [DevicePlatform.MOBILE],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_MARKETPLACE: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_SEARCH_RESULTS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.FACEBOOK_VIDEO_FEEDS: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.INSTAGRAM_FEED: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_EXPLORE: [DevicePlatform.MOBILE],
        Placement.INSTAGRAM_STORIES: [DevicePlatform.MOBILE],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        # Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
    },
}


# https://www.facebook.com/business/help/279271845888065


@cat_enum
class MediaFormat(Enum):
    IMAGE = Cat("IMAGE", display_name="Single Image")
    CAROUSEL = Cat("CAROUSEL")
    COLLECTION = Cat("COLLECTION")
    SLIDESHOW = Cat("SLIDESHOW")
    VIDEO = Cat("VIDEO")
    # TODO: old catalog - '6', displayName: 'Use existing post'
    EXISTING_POST = Cat("EXISTING_POST")


_mf_img = MediaFormat.IMAGE
_mf_vid = MediaFormat.VIDEO
_mf_car = MediaFormat.CAROUSEL
_mf_col = MediaFormat.COLLECTION

OBJECTIVE_X_PLACEMENT_X_MEDIA_FORMAT = {
    # old catalogs: image, video, carousel
    Objective.BRAND_AWARENESS: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_INSTANT_ARTICLES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [_mf_vid],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_VIDEO_FEEDS: [_mf_vid],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_EXPLORE: [_mf_img, _mf_vid],
        Placement.MESSENGER_STORIES: [_mf_img, _mf_vid],
    },
    # old catalogs: image, video, carousel
    Objective.REACH: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_INSTANT_ARTICLES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [_mf_vid],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_VIDEO_FEEDS: [_mf_vid],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_EXPLORE: [_mf_img, _mf_vid],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [_mf_img, _mf_vid, _mf_car],
        Placement.MESSENGER_STORIES: [_mf_img, _mf_vid],
    },
    # old catalogs: image, video, carousel
    Objective.LINK_CLICKS: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid, _mf_car, _mf_col],
        Placement.FACEBOOK_RIGHT_COLUMN: [_mf_img, _mf_car],
        Placement.FACEBOOK_INSTANT_ARTICLES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [_mf_vid],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_VIDEO_FEEDS: [_mf_vid],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car, _mf_col],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [_mf_img, _mf_vid, _mf_car],
        Placement.MESSENGER_INBOX: [_mf_img, _mf_car],
        Placement.MESSENGER_STORIES: [_mf_img, _mf_vid],
    },
    # old catalogs: image, video
    Objective.POST_ENGAGEMENT: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid],
        Placement.FACEBOOK_INSTANT_ARTICLES: [_mf_img, _mf_vid],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [_mf_vid],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_VIDEO_FEEDS: [_mf_vid],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid],
        Placement.INSTAGRAM_EXPLORE: [_mf_img, _mf_vid],
    },
    # old catalogs: image, video, existing_post
    Objective.PAGE_LIKES: {Placement.FACEBOOK_FEED: [_mf_img, _mf_vid]},
    # old catalogs: image, video
    Objective.EVENT_RESPONSES: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
    },
    # old catalogs: image, video, carousel
    Objective.APP_INSTALLS: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_INSTANT_ARTICLES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [_mf_vid],
        Placement.FACEBOOK_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_VIDEO_FEEDS: [_mf_vid],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_EXPLORE: [_mf_img, _mf_vid],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [_mf_img, _mf_vid, _mf_car],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [_mf_vid],
        Placement.MESSENGER_INBOX: [_mf_img, _mf_car],
        Placement.MESSENGER_STORIES: [_mf_img, _mf_vid],
    },
    # old catalogs: video, existing_post
    Objective.VIDEO_VIEWS: {
        Placement.FACEBOOK_FEED: [_mf_vid],
        Placement.FACEBOOK_INSTANT_ARTICLES: [_mf_vid],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [_mf_vid],
        Placement.FACEBOOK_MARKETPLACE: [_mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_VIDEO_FEEDS: [_mf_vid],
        Placement.INSTAGRAM_STORIES: [_mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_vid],
        Placement.INSTAGRAM_EXPLORE: [_mf_img, _mf_vid],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [_mf_vid],
        Placement.MESSENGER_STORIES: [_mf_vid],
    },
    # old catalogs: image, video, carousel
    Objective.LEAD_GENERATION: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_INSTANT_ARTICLES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [_mf_vid],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_EXPLORE: [_mf_img, _mf_vid],
    },
    # Default: REPLIES / Other valid: REPLIES (Click-to-Messenger), IMPRESSIONS (Sponsored Messages)
    # TODO: see how to include Click-to-Messenger and Sponsored Messages in the structure,
    Objective.MESSAGES: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_car],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_EXPLORE: [_mf_img, _mf_vid],
        Placement.SPONSORED_MESSAGE: [_mf_img],
        Placement.MESSENGER_INBOX: [_mf_img, _mf_car],
    },
    # old catalogs: image, video, carousel
    Objective.CONVERSIONS: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid, _mf_car, _mf_col],
        Placement.FACEBOOK_RIGHT_COLUMN: [_mf_img, _mf_car],
        Placement.FACEBOOK_INSTANT_ARTICLES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [_mf_vid],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_VIDEO_FEEDS: [_mf_vid],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car, _mf_col],
        Placement.INSTAGRAM_EXPLORE: [_mf_img, _mf_vid],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [_mf_img, _mf_vid, _mf_car],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [_mf_vid],
        Placement.MESSENGER_INBOX: [_mf_img, _mf_car],
        Placement.MESSENGER_STORIES: [_mf_img, _mf_vid],
    },
    # old catalogs: image, carousel
    Objective.PRODUCT_CATALOG_SALES: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_car, _mf_col],
        Placement.FACEBOOK_RIGHT_COLUMN: [_mf_img, _mf_car],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_car],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_EXPLORE: [_mf_img],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [_mf_img, _mf_car],
        Placement.MESSENGER_INBOX: [_mf_img, _mf_car],
    },
    Objective.LOCAL_AWARENESS: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid, _mf_car, _mf_col],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car, _mf_col],
    },
}

OBJECTIVE_X_PLACEMENT = {
    # old catalogs: image, video, carousel
    Objective.BRAND_AWARENESS: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_INSTANT_ARTICLES,
        Placement.FACEBOOK_IN_STREAM_VIDEO,
        Placement.FACEBOOK_MARKETPLACE,
        Placement.FACEBOOK_STORIES,
        Placement.FACEBOOK_SEARCH_RESULTS,
        Placement.FACEBOOK_VIDEO_FEEDS,
        Placement.INSTAGRAM_STORIES,
        Placement.INSTAGRAM_FEED,
        Placement.INSTAGRAM_EXPLORE,
        Placement.MESSENGER_STORIES,
    ],
    # old catalogs: image, video, carousel
    Objective.REACH: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_INSTANT_ARTICLES,
        Placement.FACEBOOK_IN_STREAM_VIDEO,
        Placement.FACEBOOK_MARKETPLACE,
        Placement.FACEBOOK_STORIES,
        Placement.FACEBOOK_SEARCH_RESULTS,
        Placement.FACEBOOK_VIDEO_FEEDS,
        Placement.INSTAGRAM_STORIES,
        Placement.INSTAGRAM_FEED,
        Placement.INSTAGRAM_EXPLORE,
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
        Placement.MESSENGER_STORIES,
    ],
    # old catalogs: image, video, carousel
    Objective.LINK_CLICKS: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_RIGHT_COLUMN,
        Placement.FACEBOOK_INSTANT_ARTICLES,
        Placement.FACEBOOK_IN_STREAM_VIDEO,
        Placement.FACEBOOK_MARKETPLACE,
        Placement.FACEBOOK_STORIES,
        Placement.FACEBOOK_SEARCH_RESULTS,
        Placement.FACEBOOK_VIDEO_FEEDS,
        Placement.INSTAGRAM_STORIES,
        Placement.INSTAGRAM_FEED,
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
        Placement.MESSENGER_INBOX,
        Placement.MESSENGER_STORIES,
    ],
    # old catalogs: image, video
    Objective.POST_ENGAGEMENT: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_INSTANT_ARTICLES,
        Placement.FACEBOOK_IN_STREAM_VIDEO,
        Placement.FACEBOOK_SEARCH_RESULTS,
        Placement.FACEBOOK_VIDEO_FEEDS,
        Placement.INSTAGRAM_FEED,
        Placement.INSTAGRAM_EXPLORE,
    ],
    # old catalogs: image, video, existing_post
    Objective.PAGE_LIKES: [Placement.FACEBOOK_FEED],
    # old catalogs: image, video
    Objective.EVENT_RESPONSES: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_MARKETPLACE,
    ],
    # old catalogs: image, video, carousel
    Objective.APP_INSTALLS: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_INSTANT_ARTICLES,
        Placement.FACEBOOK_IN_STREAM_VIDEO,
        Placement.FACEBOOK_STORIES,
        Placement.FACEBOOK_SEARCH_RESULTS,
        Placement.FACEBOOK_VIDEO_FEEDS,
        Placement.INSTAGRAM_STORIES,
        Placement.INSTAGRAM_FEED,
        Placement.INSTAGRAM_EXPLORE,
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
        Placement.MESSENGER_INBOX,
        Placement.MESSENGER_STORIES,
    ],
    # old catalogs: video, existing_post
    Objective.VIDEO_VIEWS: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_INSTANT_ARTICLES,
        Placement.FACEBOOK_IN_STREAM_VIDEO,
        Placement.FACEBOOK_MARKETPLACE,
        Placement.FACEBOOK_STORIES,
        Placement.FACEBOOK_SEARCH_RESULTS,
        Placement.FACEBOOK_VIDEO_FEEDS,
        Placement.INSTAGRAM_STORIES,
        Placement.INSTAGRAM_FEED,
        Placement.INSTAGRAM_EXPLORE,
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
        Placement.MESSENGER_STORIES,
    ],
    # old catalogs: image, video, carousel
    Objective.LEAD_GENERATION: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_INSTANT_ARTICLES,
        Placement.FACEBOOK_IN_STREAM_VIDEO,
        Placement.FACEBOOK_MARKETPLACE,
        Placement.FACEBOOK_STORIES,
        Placement.FACEBOOK_SEARCH_RESULTS,
        Placement.INSTAGRAM_STORIES,
        Placement.INSTAGRAM_FEED,
        Placement.INSTAGRAM_EXPLORE,
    ],
    # Default: REPLIES / Other valid: REPLIES (Click-to-Messenger), IMPRESSIONS (Sponsored Messages)
    # TODO: see how to include Click-to-Messenger and Sponsored Messages in the structure,
    Objective.MESSAGES: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_MARKETPLACE,
        Placement.FACEBOOK_STORIES,
        Placement.FACEBOOK_SEARCH_RESULTS,
        Placement.INSTAGRAM_STORIES,
        Placement.INSTAGRAM_FEED,
        Placement.INSTAGRAM_EXPLORE,
        Placement.SPONSORED_MESSAGE,
        Placement.MESSENGER_INBOX,
    ],
    # old catalogs: image, video, carousel
    Objective.CONVERSIONS: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_RIGHT_COLUMN,
        Placement.FACEBOOK_INSTANT_ARTICLES,
        Placement.FACEBOOK_IN_STREAM_VIDEO,
        Placement.FACEBOOK_MARKETPLACE,
        Placement.FACEBOOK_STORIES,
        Placement.FACEBOOK_SEARCH_RESULTS,
        Placement.FACEBOOK_VIDEO_FEEDS,
        Placement.INSTAGRAM_STORIES,
        Placement.INSTAGRAM_FEED,
        Placement.INSTAGRAM_EXPLORE,
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
        Placement.MESSENGER_INBOX,
        Placement.MESSENGER_STORIES,
    ],
    # old catalogs: image, carousel
    Objective.PRODUCT_CATALOG_SALES: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_RIGHT_COLUMN,
        Placement.FACEBOOK_MARKETPLACE,
        Placement.FACEBOOK_STORIES,
        Placement.FACEBOOK_SEARCH_RESULTS,
        Placement.INSTAGRAM_STORIES,
        Placement.INSTAGRAM_FEED,
        Placement.INSTAGRAM_EXPLORE,
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
        Placement.MESSENGER_INBOX,
    ],
    Objective.LOCAL_AWARENESS: [
        Placement.FACEBOOK_FEED,
        Placement.FACEBOOK_MARKETPLACE,
        Placement.FACEBOOK_STORIES,
        Placement.INSTAGRAM_STORIES,
        Placement.INSTAGRAM_FEED,
    ],
}

PLACEMENT_X_MEDIA_FORMAT = {
    # old catalogs: image, video, carousel
    Placement.FACEBOOK_FEED: [_mf_img, _mf_vid, _mf_car],
    Placement.FACEBOOK_RIGHT_COLUMN: [_mf_img, _mf_car],
    Placement.FACEBOOK_INSTANT_ARTICLES: [_mf_img, _mf_vid, _mf_car],
    Placement.FACEBOOK_IN_STREAM_VIDEO: [_mf_vid],
    Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
    Placement.FACEBOOK_STORIES: [_mf_img, _mf_vid, _mf_car],
    Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
    Placement.FACEBOOK_VIDEO_FEEDS: [_mf_vid],
    Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
    Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car],
    Placement.INSTAGRAM_EXPLORE: [_mf_img, _mf_vid],
    Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [_mf_img, _mf_vid, _mf_car],
    Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [_mf_vid],
    Placement.MESSENGER_INBOX: [_mf_img, _mf_car],
    Placement.MESSENGER_STORIES: [_mf_img, _mf_vid],
}

# Source: https://developers.facebook.com/docs/marketing-api/bidding/overview/bid-strategy#bid-strategy
BID_STRATEGY_X_OBJECTIVE = {
    BidStrategy.COST_CAP: [
        Objective.APP_INSTALLS,
        Objective.CONVERSIONS,
        Objective.EVENT_RESPONSES,
        Objective.LEAD_GENERATION,
        Objective.LINK_CLICKS,
        Objective.MESSAGES,
        Objective.PAGE_LIKES,
        Objective.POST_ENGAGEMENT,
        Objective.PRODUCT_CATALOG_SALES,
        Objective.VIDEO_VIEWS,
    ],
    BidStrategy.LOWEST_COST_WITHOUT_CAP: [
        Objective.APP_INSTALLS,
        Objective.CONVERSIONS,
        Objective.EVENT_RESPONSES,
        Objective.LEAD_GENERATION,
        Objective.LINK_CLICKS,
        Objective.MESSAGES,
        Objective.PAGE_LIKES,
        Objective.POST_ENGAGEMENT,
        Objective.PRODUCT_CATALOG_SALES,
        Objective.REACH,
        Objective.STORE_VISITS,
        Objective.VIDEO_VIEWS,
    ],
    BidStrategy.LOWEST_COST_WITH_BID_CAP: [
        Objective.APP_INSTALLS,
        Objective.CONVERSIONS,
        Objective.EVENT_RESPONSES,
        Objective.LEAD_GENERATION,
        Objective.LINK_CLICKS,
        Objective.MESSAGES,
        Objective.PAGE_LIKES,
        Objective.POST_ENGAGEMENT,
        Objective.PRODUCT_CATALOG_SALES,
        Objective.REACH,
        Objective.STORE_VISITS,
        Objective.VIDEO_VIEWS,
    ],
    BidStrategy.LOWEST_COST_WITH_MIN_ROAS: [
        Objective.APP_INSTALLS,
        Objective.CONVERSIONS,
        Objective.PRODUCT_CATALOG_SALES,
    ],
}

BID_STRATEGY_X_PACING_TYPE = {
    BidStrategy.COST_CAP: [PacingType.STANDARD],
    BidStrategy.LOWEST_COST_WITHOUT_CAP: [PacingType.STANDARD],
    BidStrategy.LOWEST_COST_WITH_BID_CAP: [PacingType.STANDARD],
    BidStrategy.LOWEST_COST_WITH_MIN_ROAS: [PacingType.STANDARD],
}

BUYING_TYPE_X_BILLING_EVENT = {
    BuyingType.RESERVED: [BillingEvent.APP_INSTALLS],
    BuyingType.FIXED_CPM: [BillingEvent.APP_INSTALLS],
    BuyingType.AUCTION: [
        BillingEvent.APP_INSTALLS,
        BillingEvent.IMPRESSIONS,
        BillingEvent.LINK_CLICKS,
        BillingEvent.PAGE_LIKES,
        BillingEvent.POST_ENGAGEMENT,
        BillingEvent.THRUPLAY,
    ],
}

# Source: https://developers.facebook.com/docs/marketing-api/bidding/overview/billing-events#opt_bids
OPTIMIZATION_GOAL_X_BILLING_EVENT = {
    OptimizationGoal.AD_RECALL_LIFT: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.APP_INSTALLS: {
        BillingEvent.IMPRESSIONS: [BuyingType.AUCTION],
        BillingEvent.APP_INSTALLS: [BuyingType.AUCTION],
    },
    OptimizationGoal.ENGAGED_USERS: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.EVENT_RESPONSES: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.IMPRESSIONS: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.LANDING_PAGE_VIEWS: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.LEAD_GENERATION: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.LINK_CLICKS: {
        BillingEvent.IMPRESSIONS: [BuyingType.AUCTION],
        BillingEvent.LINK_CLICKS: [BuyingType.AUCTION],
    },
    OptimizationGoal.OFFSITE_CONVERSIONS: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.PAGE_LIKES: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.POST_ENGAGEMENT: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.REACH: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.REPLIES: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.SOCIAL_IMPRESSIONS: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.THRUPLAY: {
        BillingEvent.IMPRESSIONS: [BuyingType.AUCTION],
        BillingEvent.THRUPLAY: [BuyingType.AUCTION],
    },
    OptimizationGoal.TWO_SECOND_CONTINUOUS_VIDEO_VIEWS: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
    OptimizationGoal.VALUE: {BillingEvent.IMPRESSIONS: [BuyingType.AUCTION]},
}


# Source: https://developers.facebook.com/docs/marketing-api/bidding/overview#opt
# TODO: find a more readable way of defining default values
# the default is the first value, and the order is as is
OBJECTIVE_WITH_DESTINATION_X_OPTIMIZATION_GOAL = {
    # TODO: no good value for DestinationType
    # ObjectivePromotionTarget.INSTANT_EXPERIENCES_APP
    # ObjectiveWithDestination.APP_INSTALLS_X_UNDEFINED: [
    #     # first is default
    #     OptimizationGoal.APP_INSTALLS,
    #     OptimizationGoal.IMPRESSIONS,
    #     OptimizationGoal.POST_ENGAGEMENT,
    # ],
    # ObjectivePromotionTarget.MOBILE_APP
    ObjectiveWithDestination.APP_INSTALLS_X_UNDEFINED: [
        # first is default
        OptimizationGoal.APP_INSTALLS,
        OptimizationGoal.OFFSITE_CONVERSIONS,
        OptimizationGoal.LINK_CLICKS,
        OptimizationGoal.REACH,
        OptimizationGoal.VALUE,
    ],
    ObjectiveWithDestination.BRAND_AWARENESS_X_UNDEFINED: [
        # first is default
        OptimizationGoal.AD_RECALL_LIFT,
    ],
    ObjectiveWithDestination.CONVERSIONS_X_UNDEFINED: [
        # first is default
        OptimizationGoal.OFFSITE_CONVERSIONS,
        OptimizationGoal.VALUE,
        OptimizationGoal.LANDING_PAGE_VIEWS,
        OptimizationGoal.LINK_CLICKS,
        OptimizationGoal.REACH,
        OptimizationGoal.IMPRESSIONS,
        # These are commented out, since as of 20/01/2021
        # FB platform only has the above Optimization Goals for this Objective
        # OptimizationGoal.POST_ENGAGEMENT,
        # OptimizationGoal.SOCIAL_IMPRESSIONS,
    ],
    # ObjectivePromotionTarget.EVENT
    ObjectiveWithDestination.EVENT_RESPONSES_X_UNDEFINED: [
        # first is default
        OptimizationGoal.EVENT_RESPONSES,
        OptimizationGoal.IMPRESSIONS,
        OptimizationGoal.REACH,
    ],
    # ObjectivePromotionTarget.PAGE_POST
    # TODO: no good value for DestinationType
    # ObjectiveWithDestination.EVENT_RESPONSES_X_UNDEFINED: [
    #     # first is default
    #     OptimizationGoal.EVENT_RESPONSES,
    #     OptimizationGoal.IMPRESSIONS,
    #     OptimizationGoal.POST_ENGAGEMENT,
    #     OptimizationGoal.REACH,
    # ],
    ObjectiveWithDestination.LEAD_GENERATION_X_UNDEFINED: [
        # first is default
        OptimizationGoal.LEAD_GENERATION,
    ],
    # ObjectivePromotionTarget.UNDEFINED
    ObjectiveWithDestination.LINK_CLICKS_X_WEBSITE: [
        # first is default
        OptimizationGoal.LINK_CLICKS,
        OptimizationGoal.IMPRESSIONS,
        OptimizationGoal.POST_ENGAGEMENT,
        OptimizationGoal.REACH,
        OptimizationGoal.LANDING_PAGE_VIEWS,
    ],
    # ObjectivePromotionTarget.INSTANT_EXPERIENCES_APP
    # TODO: no good value for DestinationType
    # ObjectiveWithDestination.LINK_CLICKS_X_UNDEFINED: [
    #     # first is default
    #     OptimizationGoal.ENGAGED_USERS,
    #     OptimizationGoal.APP_INSTALLS,
    #     OptimizationGoal.IMPRESSIONS,
    #     OptimizationGoal.POST_ENGAGEMENT,
    #     OptimizationGoal.REACH,
    # ],
    # ObjectivePromotionTarget.MOBILE_APP
    ObjectiveWithDestination.LINK_CLICKS_X_APP: [
        # first is default
        OptimizationGoal.LINK_CLICKS,
        OptimizationGoal.IMPRESSIONS,
        OptimizationGoal.REACH,
        OptimizationGoal.OFFSITE_CONVERSIONS,
    ],
    ObjectiveWithDestination.MESSAGES_X_UNDEFINED: [
        # first is default
        OptimizationGoal.REPLIES,
        OptimizationGoal.IMPRESSIONS,
    ],
    ObjectiveWithDestination.PAGE_LIKES_X_UNDEFINED: [
        # first is default
        OptimizationGoal.PAGE_LIKES,
        # These are commented out, since as of 20/01/2021
        # FB platform only has Page Likes as Optimization Goal for this Objective
        # OptimizationGoal.IMPRESSIONS,
        # OptimizationGoal.POST_ENGAGEMENT,
        # OptimizationGoal.REACH,
    ],
    ObjectiveWithDestination.POST_ENGAGEMENT_X_UNDEFINED: [
        # first is default
        OptimizationGoal.POST_ENGAGEMENT,
        OptimizationGoal.IMPRESSIONS,
        OptimizationGoal.REACH,
        OptimizationGoal.LINK_CLICKS,
    ],
    ObjectiveWithDestination.PRODUCT_CATALOG_SALES_X_UNDEFINED: [
        # first is default
        OptimizationGoal.OFFSITE_CONVERSIONS,
        OptimizationGoal.IMPRESSIONS,
        OptimizationGoal.POST_ENGAGEMENT,
        OptimizationGoal.REACH,
        OptimizationGoal.LINK_CLICKS,
    ],
    ObjectiveWithDestination.REACH_X_UNDEFINED: [
        # first is default
        OptimizationGoal.REACH,
        OptimizationGoal.IMPRESSIONS,
    ],
    ObjectiveWithDestination.VIDEO_VIEWS_X_UNDEFINED: [
        # first is default
        OptimizationGoal.THRUPLAY,
        OptimizationGoal.TWO_SECOND_CONTINUOUS_VIDEO_VIEWS,
    ],
}

# https://developers.facebook.com/docs/marketing-api/reference/ad-campaign-group#attribution_spec

# TODO: see how to include this rule, adding all the combinations to the rule seems excessive
# For all other optimization_goal and objective combinations,
# you can only use 1-day click for attribution_spec.


OBJECTIVE_X_OPTIMIZATION_GOAL_X_ACTION_ATTRIBUTION_WINDOW_CLICK_X_ACTION_ATTRIBUTION_WINDOW_VIEW = {
    Objective.CONVERSIONS: {
        OptimizationGoal.OFFSITE_CONVERSIONS: {
            ActionAttributionWindowClick.VALUE_1D: [
                ActionAttributionWindowView.NONE,
                ActionAttributionWindowView.VALUE_1D,
            ],
            ActionAttributionWindowClick.VALUE_7D: [
                ActionAttributionWindowView.NONE,
                ActionAttributionWindowView.VALUE_1D,
            ],
        },
        # TODO: see hwo to use this, the optimization goal doesn't exist in the SDK
        # OptimizationGoal.INCREMENTAL_OFFSITE_CONVERSIONS: {
        #     ActionAttributionWindowClick.NONE: [
        #         ActionAttributionWindowView.NONE,
        #     ],
        # },
    },
    Objective.PRODUCT_CATALOG_SALES: {
        OptimizationGoal.OFFSITE_CONVERSIONS: {
            ActionAttributionWindowClick.VALUE_1D: [
                ActionAttributionWindowView.NONE,
                ActionAttributionWindowView.VALUE_1D,
            ],
            ActionAttributionWindowClick.VALUE_7D: [
                ActionAttributionWindowView.NONE,
                ActionAttributionWindowView.VALUE_1D,
            ],
        },
    },
    Objective.APP_INSTALLS: {
        OptimizationGoal.OFFSITE_CONVERSIONS: {
            ActionAttributionWindowClick.VALUE_1D: [ActionAttributionWindowView.NONE]
        },
        OptimizationGoal.APP_INSTALLS: {
            ActionAttributionWindowClick.VALUE_1D: [
                ActionAttributionWindowView.NONE,
                ActionAttributionWindowView.VALUE_1D,
            ],
        },
    },
    Objective.LINK_CLICKS: {
        OptimizationGoal.OFFSITE_CONVERSIONS: {
            ActionAttributionWindowClick.VALUE_1D: [ActionAttributionWindowView.NONE],
            ActionAttributionWindowClick.VALUE_7D: [ActionAttributionWindowView.NONE],
        },
    },
}

JOINT_CATS = dict(
    OBJECTIVE_X_CALL_TO_ACTION_TYPE=JointCat.from_dict(OBJECTIVE_X_CALL_TO_ACTION_TYPE, Objective, CallToActionType),
    PLACEMENT_X_AD_FORMAT=JointCat.from_dict(PLACEMENT_X_AD_FORMAT, Placement, AdFormat),
    OBJECTIVE_X_PLACEMENT_X_DEVICE_PLATFORM=JointCat.from_dict(
        OBJECTIVE_X_PLACEMENT_X_DEVICE_PLATFORM, Objective, Placement, DevicePlatform
    ),
    BID_STRATEGY_X_OBJECTIVE=JointCat.from_dict(BID_STRATEGY_X_OBJECTIVE, BidStrategy, Objective),
    BID_STRATEGY_X_PACING_TYPE=JointCat.from_dict(BID_STRATEGY_X_PACING_TYPE, BidStrategy, PacingType),
    BUYING_TYPE_X_BILLING_EVENT=JointCat.from_dict(BUYING_TYPE_X_BILLING_EVENT, BuyingType, BillingEvent),
    OPTIMIZATION_GOAL_X_BILLING_EVENT=JointCat.from_dict(
        OPTIMIZATION_GOAL_X_BILLING_EVENT, OptimizationGoal, BillingEvent
    ),
    OBJECTIVE_WITH_DESTINATION_X_OPTIMIZATION_GOAL=JointCat.from_dict(
        OBJECTIVE_WITH_DESTINATION_X_OPTIMIZATION_GOAL, ObjectiveWithDestination, OptimizationGoal
    ),
    OBJECTIVE_X_OPTIMIZATION_GOAL_X_ACTION_ATTRIBUTION_WINDOW_CLICK_X_ACTION_ATTRIBUTION_WINDOW_VIEW=JointCat.from_dict(
        OBJECTIVE_X_OPTIMIZATION_GOAL_X_ACTION_ATTRIBUTION_WINDOW_CLICK_X_ACTION_ATTRIBUTION_WINDOW_VIEW,
        Objective,
        OptimizationGoal,
        ActionAttributionWindowClick,
        ActionAttributionWindowView,
    ),
)


def reverse_dict_items(cat_dict: Dict) -> Dict[Any, set]:
    result = collections.defaultdict(set)
    for k, v in cat_dict.items():
        for entry in v:
            result[entry].add(k)
    return result


PLACEMENT_X_OBJECTIVE = reverse_dict_items(OBJECTIVE_X_PLACEMENT)
MEDIA_FORMAT_X_PLACEMENT = reverse_dict_items(PLACEMENT_X_MEDIA_FORMAT)
AD_FORMAT_X_PLACEMENT = reverse_dict_items(PLACEMENT_X_AD_FORMAT)
CALL_TO_ACTION_TYPE_X_OBJECTIVE = reverse_dict_items(OBJECTIVE_X_CALL_TO_ACTION_TYPE)
