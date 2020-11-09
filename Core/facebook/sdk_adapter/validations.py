from enum import Enum

from Core.facebook.sdk_adapter.ad_objects.ad_campaign_delivery_estimate import OptimizationGoal
from Core.facebook.sdk_adapter.ad_objects.ad_creative import CallToActionType
from Core.facebook.sdk_adapter.ad_objects.ad_preview import AdFormat
from Core.facebook.sdk_adapter.ad_objects.ad_set import BillingEvent, PacingType
from Core.facebook.sdk_adapter.ad_objects.campaign import BidStrategy, Objective
from Core.facebook.sdk_adapter.ad_objects.content_delivery_report import Placement
from Core.facebook.sdk_adapter.ad_objects.reach_frequency_prediction import BuyingType
from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform
from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum


OBJECTIVE_X_CALL_TO_ACTION_TYPE = {
    Objective.APP_INSTALLS: [
        CallToActionType.NO_BUTTON,
        CallToActionType.PLAY_GAME,
        CallToActionType.BOOK_TRAVEL,
        CallToActionType.DOWNLOAD,
        CallToActionType.LEARN_MORE,
        CallToActionType.LISTEN_NOW,
        CallToActionType.SHOP_NOW,
        CallToActionType.SIGN_UP,
        CallToActionType.SUBSCRIBE,
        CallToActionType.WATCH_MORE,
        CallToActionType.INSTALL_APP,
        CallToActionType.USE_APP,
    ],
    Objective.BRAND_AWARENESS: [
        CallToActionType.NO_BUTTON,
        CallToActionType.MESSAGE_PAGE,
        CallToActionType.APPLY_NOW,
        CallToActionType.BOOK_TRAVEL,
        CallToActionType.CONTACT_US,
        CallToActionType.DOWNLOAD,
        CallToActionType.GET_QUOTE,
        CallToActionType.GET_SHOWTIMES,
        CallToActionType.LEARN_MORE,
        CallToActionType.LISTEN_NOW,
        CallToActionType.SEE_MORE,
        CallToActionType.SHOP_NOW,
        CallToActionType.SIGN_UP,
        CallToActionType.SUBSCRIBE,
        CallToActionType.WATCH_MORE,
        CallToActionType.WHATSAPP_MESSAGE,
    ],
    Objective.CONVERSIONS: [
        CallToActionType.NO_BUTTON,
        CallToActionType.PLAY_GAME,
        CallToActionType.APPLY_NOW,
        CallToActionType.BOOK_TRAVEL,
        CallToActionType.CONTACT_US,
        CallToActionType.DOWNLOAD,
        CallToActionType.GET_QUOTE,
        CallToActionType.GET_SHOWTIMES,
        CallToActionType.LEARN_MORE,
        CallToActionType.LISTEN_NOW,
        CallToActionType.SEE_MORE,
        CallToActionType.SHOP_NOW,
        CallToActionType.SIGN_UP,
        CallToActionType.SUBSCRIBE,
        CallToActionType.WATCH_MORE,
        CallToActionType.WHATSAPP_MESSAGE,
        CallToActionType.GET_OFFER,
    ],
    Objective.LEAD_GENERATION: [
        CallToActionType.APPLY_NOW,
        CallToActionType.BOOK_TRAVEL,
        CallToActionType.DOWNLOAD,
        CallToActionType.GET_OFFER,
        CallToActionType.GET_QUOTE,
        CallToActionType.LEARN_MORE,
        CallToActionType.SIGN_UP,
        CallToActionType.SUBSCRIBE,
    ],
    # TODO: name X name
    # Objective.LINK_CLICKS_X_APP: [
    #     CallToActionType.NO_BUTTON,
    #     CallToActionType.OPEN_LINK,
    #     CallToActionType.PLAY_GAME,
    #     CallToActionType.USE_APP,
    #     CallToActionType.BOOK_TRAVEL,
    #     CallToActionType.LEARN_MORE,
    #     CallToActionType.LISTEN_NOW,
    #     CallToActionType.SHOP_NOW,
    #     CallToActionType.SUBSCRIBE,
    #     CallToActionType.WATCH_MORE,
    # ],
    # TODO: name X name
    # Objective.LINK_CLICKS_X_WEBSITE: [
    #     CallToActionType.NO_BUTTON,
    #     CallToActionType.APPLY_NOW,
    #     CallToActionType.BOOK_TRAVEL,
    #     CallToActionType.CONTACT_US,
    #     CallToActionType.DOWNLOAD,
    #     CallToActionType.GET_QUOTE,
    #     CallToActionType.GET_SHOWTIMES,
    #     CallToActionType.LEARN_MORE,
    #     CallToActionType.LISTEN_NOW,
    #     CallToActionType.SEE_MORE,
    #     CallToActionType.SHOP_NOW,
    #     CallToActionType.SIGN_UP,
    #     CallToActionType.SUBSCRIBE,
    #     CallToActionType.WATCH_MORE,
    #     CallToActionType.WHATSAPP_MESSAGE,
    #     CallToActionType.GET_OFFER,
    # ],
    Objective.PAGE_LIKES: [CallToActionType.LIKE_PAGE],
    Objective.POST_ENGAGEMENT: [
        CallToActionType.NO_BUTTON,
        CallToActionType.GET_QUOTE,
        CallToActionType.LEARN_MORE,
        CallToActionType.MESSAGE_PAGE,
        CallToActionType.SHOP_NOW,
        CallToActionType.WHATSAPP_MESSAGE,
    ],
    Objective.PRODUCT_CATALOG_SALES: [
        CallToActionType.NO_BUTTON,
        CallToActionType.OPEN_LINK,
        CallToActionType.MESSAGE_PAGE,
        CallToActionType.BOOK_TRAVEL,
        CallToActionType.DOWNLOAD,
        CallToActionType.GET_SHOWTIMES,
        CallToActionType.LEARN_MORE,
        CallToActionType.LISTEN_NOW,
        CallToActionType.SHOP_NOW,
        CallToActionType.SIGN_UP,
        CallToActionType.SUBSCRIBE,
    ],
    Objective.REACH: [
        CallToActionType.NO_BUTTON,
        CallToActionType.MESSAGE_PAGE,
        CallToActionType.APPLY_NOW,
        CallToActionType.BOOK_TRAVEL,
        CallToActionType.CONTACT_US,
        CallToActionType.DOWNLOAD,
        CallToActionType.GET_QUOTE,
        CallToActionType.GET_SHOWTIMES,
        CallToActionType.LEARN_MORE,
        CallToActionType.LISTEN_NOW,
        CallToActionType.SEE_MORE,
        CallToActionType.CALL,
        CallToActionType.SHOP_NOW,
        CallToActionType.GET_DIRECTIONS,
        CallToActionType.SIGN_UP,
        CallToActionType.SUBSCRIBE,
        CallToActionType.WATCH_MORE,
        CallToActionType.WHATSAPP_MESSAGE,
    ],
    Objective.VIDEO_VIEWS: [
        CallToActionType.MESSAGE_PAGE,
        CallToActionType.BOOK_TRAVEL,
        CallToActionType.DOWNLOAD,
        CallToActionType.GET_QUOTE,
        CallToActionType.GET_SHOWTIMES,
        CallToActionType.LEARN_MORE,
        CallToActionType.LISTEN_NOW,
        CallToActionType.SHOP_NOW,
        CallToActionType.SIGN_UP,
        CallToActionType.SUBSCRIBE,
        CallToActionType.WATCH_MORE,
        CallToActionType.WHATSAPP_MESSAGE,
    ],
}


PLACEMENT_X_AD_FORMAT = PLATFORM_X_POSITION_X_AD_FORMAT = {
    # TODO: ??? mobile should also be in instagram ???
    Placement.FACEBOOK_FEED: [
        AdFormat.DESKTOP_FEED_STANDARD,
        AdFormat.MOBILE_FEED_BASIC,
        AdFormat.MOBILE_FEED_STANDARD,
        AdFormat.WATCH_FEED_MOBILE,
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


# TODO: see if this structure is useful, i.e. if OBJECTIVE_X_DEVICE_PLATFORM is selected somewhere before placement
# TODO: add Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__
# OBJECTIVE_X_DEVICE_PLATFORM_X_PLACEMENT = OBJECTIVE_X_DEVICE_PLATFORM_X_PLATFORM_X_POSITION = {
#     Objective.APP_INSTALLS: {
#         DevicePlatform.MOBILE: [
#             Placement.FACEBOOK_STORIES,
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_INSTANT_ARTICLES,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.INSTAGRAM_FEED,
#             Placement.INSTAGRAM_EXPLORE,
#             Placement.INSTAGRAM_STORIES,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
#         ],
#         DevicePlatform.DESKTOP: [Placement.FACEBOOK_FEED, Placement.FACEBOOK_VIDEO_FEEDS],
#     },
#     Objective.BRAND_AWARENESS: {
#         DevicePlatform.MOBILE: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.FACEBOOK_INSTANT_ARTICLES,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_STORIES,
#             Placement.INSTAGRAM_FEED,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#         ],
#         DevicePlatform.DESKTOP: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#         ],
#     },
#     Objective.CONVERSIONS: {
#         DevicePlatform.MOBILE: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_INSTANT_ARTICLES,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_STORIES,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_RIGHT_COLUMN,
#             Placement.INSTAGRAM_FEED,
#             Placement.INSTAGRAM_EXPLORE,
#             Placement.INSTAGRAM_STORIES,
#         ],
#         DevicePlatform.DESKTOP: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.FACEBOOK_RIGHT_COLUMN,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#             Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
#         ],
#     },
#     Objective.LEAD_GENERATION: {
#         DevicePlatform.MOBILE: [Placement.FACEBOOK_FEED, Placement.FACEBOOK_STORIES, Placement.INSTAGRAM_FEED],
#         DevicePlatform.DESKTOP: [Placement.FACEBOOK_FEED],
#     },
#     Objective.LINK_CLICKS: {
#         DevicePlatform.MOBILE: [
#             Placement.FACEBOOK_STORIES,
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_INSTANT_ARTICLES,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_RIGHT_COLUMN,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.INSTAGRAM_FEED,
#             Placement.INSTAGRAM_EXPLORE,
#             Placement.INSTAGRAM_STORIES,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#             Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
#         ],
#         DevicePlatform.DESKTOP: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_RIGHT_COLUMN,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#             Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
#         ],
#     },
#     Objective.LOCAL_AWARENESS: {
#         DevicePlatform.MOBILE: [
#             Placement.FACEBOOK_STORIES,
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_INSTANT_ARTICLES,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#         ],
#         DevicePlatform.DESKTOP: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#         ],
#     },
#     Objective.PAGE_LIKES: {
#         DevicePlatform.MOBILE: [
#             Placement.FACEBOOK_STORIES,
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_INSTANT_ARTICLES,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#         ],
#         DevicePlatform.DESKTOP: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#         ],
#     },
#     Objective.POST_ENGAGEMENT: {
#         DevicePlatform.MOBILE: [
#             Placement.FACEBOOK_STORIES,
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_INSTANT_ARTICLES,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.INSTAGRAM_FEED,
#             Placement.INSTAGRAM_EXPLORE,
#             Placement.INSTAGRAM_STORIES,
#         ],
#         DevicePlatform.DESKTOP: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#         ],
#     },
#     Objective.PRODUCT_CATALOG_SALES: {
#         DevicePlatform.MOBILE: [
#             Placement.FACEBOOK_STORIES,
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_INSTANT_ARTICLES,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_RIGHT_COLUMN,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.INSTAGRAM_FEED,
#             Placement.INSTAGRAM_EXPLORE,
#             Placement.INSTAGRAM_STORIES,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#             Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
#         ],
#         DevicePlatform.DESKTOP: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_RIGHT_COLUMN,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#             Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
#         ],
#     },
#     Objective.REACH: {
#         DevicePlatform.MOBILE: [
#             Placement.FACEBOOK_STORIES,
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_INSTANT_ARTICLES,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.INSTAGRAM_FEED,
#             Placement.INSTAGRAM_EXPLORE,
#             Placement.INSTAGRAM_STORIES,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#             Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
#         ],
#         DevicePlatform.DESKTOP: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#             Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
#         ],
#     },
#     Objective.VIDEO_VIEWS: {
#         DevicePlatform.MOBILE: [
#             Placement.FACEBOOK_STORIES,
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_INSTANT_ARTICLES,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.INSTAGRAM_FEED,
#             Placement.INSTAGRAM_EXPLORE,
#             Placement.INSTAGRAM_STORIES,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#             Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
#         ],
#         DevicePlatform.DESKTOP: [
#             Placement.FACEBOOK_FEED,
#             Placement.FACEBOOK_IN_STREAM_VIDEO,
#             Placement.FACEBOOK_MARKETPLACE,
#             Placement.FACEBOOK_SEARCH_RESULTS,
#             Placement.FACEBOOK_VIDEO_FEEDS,
#             Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
#             Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__,
#             Placement.AUDIENCE_NETWORK_REWARDED_VIDEO,
#         ],
#     },
# }

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
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
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
        Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.DESKTOP],
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
        Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
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
        Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
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
        Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
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
        Placement.__AUDIENCE_NETWORK__INSTREAM_VIDEO__: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [DevicePlatform.MOBILE, DevicePlatform.DESKTOP],
    },
}


# https://www.facebook.com/business/help/279271845888065

# TODO: see if following data from old catalogs are relevant

# image = (str(FiledAdFormatEnum.IMAGE.value))
# video = (str(FiledAdFormatEnum.VIDEO.value))
# carousel = (str(FiledAdFormatEnum.CAROUSEL.value))
# existing_post = (str(FiledAdFormatEnum.EXISTING_POST.value))
#
# class AdFormat(Base):
#     brand_awareness = objectives.brand_awareness.with_children(image, video, carousel)
#     reach = objectives.reach.with_children(image, video, carousel)
#     website_traffic = objectives.website_traffic.with_children(image, video, carousel)
#     page_likes = objectives.page_likes.with_children(image, video, existing_post)
#     post_likes = objectives.post_likes.with_children(image, video)
#     event_responses = objectives.event_responses.with_children(image, video)
#     app_installs = objectives.app_installs.with_children(image, video, carousel)
#     traffic_for_apps = objectives.app_traffic.with_children(image, video, carousel)
#     # Existing post only works with a video post. This should be validated on FE when the post is selected I think
#     video_views = objectives.video_views.with_children(video, existing_post)
#     lead_generation = objectives.lead_generation.with_children(image, video, carousel)
#     conversions = objectives.conversions_leaf.with_children(image, video, carousel)
#     catalog_sales = objectives.catalog_sales.with_children(image, carousel)

# _media_format = GraphAPIAdPreviewBuilderHandler.FiledAdFormatEnum
#
# _mf_img = _media_format.IMAGE.name
# _mf_vid = _media_format.VIDEO.name
# _mf_car = _media_format.CAROUSEL.name
# _mf_col = _media_format.COLLECTION.name

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
    Objective.STORE_TRAFFIC: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid, _mf_car, _mf_col],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car, _mf_col],
    },
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
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_INTERSTITIAL: [_mf_img, _mf_vid, _mf_car],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [_mf_vid],
        Placement.MESSENGER_INBOX: [_mf_img, _mf_car],
        Placement.MESSENGER_STORIES: [_mf_img, _mf_vid],
    },
    Objective.CATALOG_SALES: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_car, _mf_col],
        Placement.FACEBOOK_RIGHT_COLUMN: [_mf_img, _mf_car],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_STORIES: [_mf_car],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_STORIES: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid, _mf_car],
        Placement.INSTAGRAM_EXPLORE: [_mf_img],
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_INTERSTITIAL: [_mf_img, _mf_car],
        Placement.MESSENGER_INBOX: [_mf_img, _mf_car],
    },
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
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_INTERSTITIAL: [_mf_img, _mf_vid, _mf_car],
        Placement.MESSENGER_STORIES: [_mf_img, _mf_vid],
    },
    Objective.APP_TRAFFIC: {
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
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_INTERSTITIAL: [_mf_img, _mf_vid, _mf_car],
        Placement.MESSENGER_INBOX: [_mf_img, _mf_car],
        Placement.MESSENGER_STORIES: [_mf_img, _mf_vid],
    },
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
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_INTERSTITIAL: [_mf_img, _mf_vid, _mf_car],
        Placement.AUDIENCE_NETWORK_REWARDED_VIDEO: [_mf_vid],
        Placement.MESSENGER_INBOX: [_mf_img, _mf_car],
        Placement.MESSENGER_STORIES: [_mf_img, _mf_vid],
    },
    Objective.PAGE_LIKES: {Placement.FACEBOOK_FEED: [_mf_img, _mf_vid]},
    Objective.EVENT_RESPONSES: {
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid],
        Placement.FACEBOOK_MARKETPLACE: [_mf_img, _mf_vid, _mf_car],
    },
    # TODO: Objective.ENGAGEMENT doesn't exist, use components
    Objective.ENGAGEMENT: {
        # post_likes,
        # page_likes,
        Placement.FACEBOOK_FEED: [_mf_img, _mf_vid],
        Placement.FACEBOOK_INSTANT_ARTICLES: [_mf_img, _mf_vid],
        Placement.FACEBOOK_IN_STREAM_VIDEO: [_mf_vid],
        Placement.FACEBOOK_SEARCH_RESULTS: [_mf_img, _mf_vid, _mf_car],
        Placement.FACEBOOK_VIDEO_FEEDS: [_mf_vid],
        Placement.INSTAGRAM_FEED: [_mf_img, _mf_vid],
        Placement.INSTAGRAM_EXPLORE: [_mf_img, _mf_vid],
    },
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
        Placement.AUDIENCE_NETWORK_NATIVE_BANNER_INTERSTITIAL: [_mf_vid],
        Placement.MESSENGER_STORIES: [_mf_vid],
    },
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
}


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
    BidStrategy.TARGET_COST: [
        Objective.APP_INSTALLS,
        Objective.CONVERSIONS,
        Objective.LEAD_GENERATION,
        Objective.PRODUCT_CATALOG_SALES,
        Objective.STORE_VISITS,
    ],
    BidStrategy.LOWEST_COST_WITH_MIN_ROAS: [
        Objective.APP_INSTALLS,
        Objective.CONVERSIONS,
        Objective.PRODUCT_CATALOG_SALES,
    ],
}


class BidStrategyXPacingType(Enum):
    COST_CAP_X_STANDARD = Cat(None, BidStrategy.COST_CAP, PacingType.STANDARD)
    LOWEST_COST_WITHOUT_CAP_X_STANDARD = Cat(None, BidStrategy.LOWEST_COST_WITHOUT_CAP, PacingType.STANDARD)
    LOWEST_COST_WITH_BID_CAP_X_STANDARD = Cat(None, BidStrategy.LOWEST_COST_WITH_BID_CAP, PacingType.STANDARD)
    TARGET_COST_X_STANDARD = Cat(None, BidStrategy.TARGET_COST, PacingType.STANDARD)
    LOWEST_COST_WITH_MIN_ROAS_X_STANDARD = Cat(None, BidStrategy.LOWEST_COST_WITH_MIN_ROAS, PacingType.STANDARD)

    _ignore_ = ["joint_fields"]
    joint_fields = [BidStrategy, PacingType]


BID_STRATEGY_X_PACING_TYPE = {
    BidStrategy.COST_CAP: [PacingType.STANDARD],
    BidStrategy.LOWEST_COST_WITHOUT_CAP: [PacingType.STANDARD],
    BidStrategy.LOWEST_COST_WITH_BID_CAP: [PacingType.STANDARD],
    BidStrategy.TARGET_COST: [PacingType.STANDARD],
    BidStrategy.LOWEST_COST_WITH_MIN_ROAS: [PacingType.STANDARD],
}


class BillingEventXBuyingType(Enum):
    APP_INSTALLS_X_RESERVED = Cat(None, BillingEvent.APP_INSTALLS, BuyingType.RESERVED)
    APP_INSTALLS_X_FIXED_CPM = Cat(None, BillingEvent.APP_INSTALLS, BuyingType.FIXED_CPM)
    APP_INSTALLS_X_AUCTION = Cat(None, BillingEvent.APP_INSTALLS, BuyingType.AUCTION)
    IMPRESSIONS_X_AUCTION = Cat(None, BillingEvent.IMPRESSIONS, BuyingType.AUCTION)
    LINK_CLICKS_X_AUCTION = Cat(None, BillingEvent.LINK_CLICKS, BuyingType.AUCTION)
    PAGE_LIKES_X_AUCTION = Cat(None, BillingEvent.PAGE_LIKES, BuyingType.AUCTION)
    POST_ENGAGEMENT_X_AUCTION = Cat(None, BillingEvent.POST_ENGAGEMENT, BuyingType.AUCTION)
    THRUPLAY_X_AUCTION = Cat(None, BillingEvent.THRUPLAY, BuyingType.AUCTION)

    _ignore_ = ["joint_fields"]
    joint_fields = [BillingEvent, BuyingType]


BUYING_TYPE_X_BILLING_EVENT = {
    BuyingType.RESERVED: BillingEvent.APP_INSTALLS,
    BuyingType.FIXED_CPM: BillingEvent.APP_INSTALLS,
    BuyingType.AUCTION: [
        BillingEvent.APP_INSTALLS,
        BillingEvent.IMPRESSIONS,
        BillingEvent.LINK_CLICKS,
        BillingEvent.PAGE_LIKES,
        BillingEvent.POST_ENGAGEMENT,
        BillingEvent.THRUPLAY,
    ],
}


OPTIMIZATION_GOAL_X_BILLING_EVENT = {
    OptimizationGoal.AD_RECALL_LIFT: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.APP_INSTALLS: [
        BillingEventXBuyingType.IMPRESSIONS_X_AUCTION,
        BillingEventXBuyingType.APP_INSTALLS_X_AUCTION,
    ],
    OptimizationGoal.ENGAGED_USERS: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.EVENT_RESPONSES: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.IMPRESSIONS: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.LANDING_PAGE_VIEWS: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.LEAD_GENERATION: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.LINK_CLICKS: [
        BillingEventXBuyingType.LINK_CLICKS_X_AUCTION,
        BillingEventXBuyingType.IMPRESSIONS_X_AUCTION,
    ],
    OptimizationGoal.OFFSITE_CONVERSIONS: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.PAGE_LIKES: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.POST_ENGAGEMENT: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.REACH: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.REPLIES: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.SOCIAL_IMPRESSIONS: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.THRUPLAY: [
        BillingEventXBuyingType.IMPRESSIONS_X_AUCTION,
        BillingEventXBuyingType.THRUPLAY_X_AUCTION,
    ],
    OptimizationGoal.TWO_SECOND_CONTINUOUS_VIDEO_VIEWS: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
    OptimizationGoal.VALUE: [BillingEventXBuyingType.IMPRESSIONS_X_AUCTION],
}


# https://developers.facebook.com/docs/marketing-api/bidding/overview#opt

goals = "OPTIMIZATON_GOALS_FOR_ALL"
goals_instant_experiences_app = "OPTIMIZATON_GOALS_FOR_INSTANT_EXPERIENCES_APP"
goals_mobile_app = "OPTIMIZATON_GOALS_FOR_MOBILE_APP"
goals_event = "OPTIMIZATON_GOALS_FOR_EVENT"
goals_page_post = "OPTIMIZATON_GOALS_FOR_PAGE_POST"

OBJECTIVE_X_OPTIMIZATION_GOAL = {
    Objective.CONVERSIONS: (
        goals,
        OptimizationGoal.OFFSITE_CONVERSIONS,
        OptimizationGoal.IMPRESSIONS,
        OptimizationGoal.POST_ENGAGEMENT,
        OptimizationGoal.REACH,
        OptimizationGoal.SOCIAL_IMPRESSIONS,
        OptimizationGoal.VALUE,
        OptimizationGoal.LANDING_PAGE_VIEWS,
        OptimizationGoal.LINK_CLICKS,
    ),
    Objective.CATALOG_SALES: (
        goals,
        OptimizationGoal.OFFSITE_CONVERSIONS,
        OptimizationGoal.IMPRESSIONS,
        OptimizationGoal.POST_ENGAGEMENT,
        OptimizationGoal.OFFSITE_CONVERSIONS,
        OptimizationGoal.REACH,
        OptimizationGoal.LINK_CLICKS,
    ),
    Objective.BRAND_AWARENESS: (goals, OptimizationGoal.AD_RECALL_LIFT,),
    Objective.REACH: (goals, OptimizationGoal.REACH, OptimizationGoal.IMPRESSIONS),
    Objective.APP_TRAFFIC: (
        (
            goals,
            OptimizationGoal.LINK_CLICKS,
            OptimizationGoal.IMPRESSIONS,
            OptimizationGoal.POST_ENGAGEMENT,
            OptimizationGoal.REACH,
            OptimizationGoal.LANDING_PAGE_VIEWS,
        ),
        (
            goals_instant_experiences_app,
            OptimizationGoal.ENGAGED_USERS,
            OptimizationGoal.APP_INSTALLS,
            OptimizationGoal.IMPRESSIONS,
            OptimizationGoal.POST_ENGAGEMENT,
            OptimizationGoal.REACH,
        ),
        (
            goals_mobile_app,
            OptimizationGoal.LINK_CLICKS,
            OptimizationGoal.IMPRESSIONS,
            OptimizationGoal.REACH,
            OptimizationGoal.OFFSITE_CONVERSIONS,
        ),
    ),
    Objective.POST_ENGAGEMENT: (
        goals,
        OptimizationGoal.POST_ENGAGEMENT,
        OptimizationGoal.IMPRESSIONS,
        OptimizationGoal.REACH,
        OptimizationGoal.LINK_CLICKS,
    ),
    Objective.PAGE_LIKES: (
        goals,
        OptimizationGoal.PAGE_LIKES,
        OptimizationGoal.IMPRESSIONS,
        OptimizationGoal.POST_ENGAGEMENT,
        OptimizationGoal.REACH,
    ),
    Objective.EVENT_RESPONSES: (
        (goals_event, OptimizationGoal.EVENT_RESPONSES, OptimizationGoal.IMPRESSIONS, OptimizationGoal.REACH),
        (
            goals_page_post,
            OptimizationGoal.EVENT_RESPONSES,
            OptimizationGoal.IMPRESSIONS,
            OptimizationGoal.POST_ENGAGEMENT,
            OptimizationGoal.REACH,
        ),
    ),
    Objective.APP_INSTALLS: (
        (
            goals_instant_experiences_app,
            OptimizationGoal.APP_INSTALLS,
            OptimizationGoal.IMPRESSIONS,
            OptimizationGoal.POST_ENGAGEMENT,
        ),
        (
            goals_mobile_app,
            OptimizationGoal.APP_INSTALLS,
            OptimizationGoal.OFFSITE_CONVERSIONS,
            OptimizationGoal.LINK_CLICKS,
            OptimizationGoal.REACH,
            OptimizationGoal.VALUE,
        ),
    ),
    Objective.VIDEO_VIEWS: (goals, OptimizationGoal.THRUPLAY, OptimizationGoal.TWO_SECOND_CONTINUOUS_VIDEO_VIEWS),
    Objective.LEAD_GENERATION: (goals, OptimizationGoal.LEAD_GENERATION),
    Objective.MESSAGES: (goals, OptimizationGoal.REPLIES, OptimizationGoal.IMPRESSIONS),
}
