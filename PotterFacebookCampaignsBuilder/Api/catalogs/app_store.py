from facebook_business.adobjects.adaccountmatchedsearchapplicationsedgedata import (
    AdAccountMatchedSearchApplicationsEdgeData,
)
from PotterFacebookCampaignsBuilder.Api.catalogs.base import Base
from PotterFacebookCampaignsBuilder.Api.catalogs.node import Node

_app_store = AdAccountMatchedSearchApplicationsEdgeData.AppStore


class AppStore(Base):
    amazon_app_store = Node(_app_store.amazon_app_store)
    fb_android_store = Node(_app_store.fb_android_store)
    fb_canvas = Node(_app_store.fb_canvas)
    fb_gameroom = Node(_app_store.fb_gameroom)
    google_play = Node(_app_store.google_play)
    instant_game = Node(_app_store.instant_game)
    itunes = Node(_app_store.itunes)
    itunes_ipad = Node(_app_store.itunes_ipad)
    roku_store = Node(_app_store.roku_store)
    windows_10_store = Node(_app_store.windows_10_store)
    windows_store = Node(_app_store.windows_store)
