from enum import Enum

from facebook_business.adobjects.adaccountmatchedsearchapplicationsedgedata import (
    AdAccountMatchedSearchApplicationsEdgeData,
)

from Core.facebook.sdk_adapter.catalog_models import Cat, cat_enum

# https://developers.facebook.com/docs/marketing-api/reference/ad-account/matched_search_applications

_app_store = AdAccountMatchedSearchApplicationsEdgeData.AppStore


@cat_enum
class AppStore(Enum):
    AMAZON_APP_STORE = Cat(_app_store.amazon_app_store)
    FB_ANDROID_STORE = Cat(_app_store.fb_android_store)
    FB_CANVAS = Cat(_app_store.fb_canvas)
    FB_GAMEROOM = Cat(_app_store.fb_gameroom)
    GOOGLE_PLAY = Cat(_app_store.google_play)
    INSTANT_GAME = Cat(_app_store.instant_game)
    ITUNES = Cat(_app_store.itunes)
    ITUNES_IPAD = Cat(_app_store.itunes_ipad)
    ROKU_STORE = Cat(_app_store.roku_store)
    WINDOWS_10_STORE = Cat(_app_store.windows_10_store)
    WINDOWS_STORE = Cat(_app_store.windows_store)

    OCULUS_APP_STORE = Cat("OCULUS_APP_STORE")
