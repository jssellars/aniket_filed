from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from Turing.Api.Catalogs.BusinessViews.ViewAppEngagement import ViewCampaignAppEngagement, ViewAdSetAppEngagement, ViewAdAppEngagement
from Turing.Api.Catalogs.BusinessViews.ViewBiddingAndOptimization import ViewCampaignBiddingAndOptimization, ViewAdSetBiddingAndOptimization, ViewAdBiddingAndOptimization
from Turing.Api.Catalogs.BusinessViews.ViewCarouselEngagement import ViewCampaignCarouselEngagement, ViewAdSetCarouselEngagement, ViewAdCarouselEngagement
from Turing.Api.Catalogs.BusinessViews.ViewCrossDevice import ViewCampaignCrossDevice, ViewAdSetCrossDevice, ViewAdCrossDevice
from Turing.Api.Catalogs.BusinessViews.ViewDelivery import ViewCampaignDelivery, ViewAdSetDelivery, ViewAdDelivery
from Turing.Api.Catalogs.BusinessViews.ViewEngagement import ViewCampaignEngagement, ViewAdSetEngagement, ViewAdEngagement
from Turing.Api.Catalogs.BusinessViews.ViewPerformance import ViewCampaignPerformance, ViewAdSetPerformance, ViewAdPerformance, ViewCampaignFallback
from Turing.Api.Catalogs.BusinessViews.ViewPerformanceAndClicks import ViewCampaignPerformanceAndClicks, ViewAdSetPerformanceAndClicks, ViewAdPerformanceAndClicks
from Turing.Api.Catalogs.BusinessViews.ViewTargetingAndCreative import ViewCampaignTargetingAndCreative, ViewAdSetTargetingAndCreative, ViewAdTargetingAndCreative
from Turing.Api.Catalogs.BusinessViews.ViewVideoEngagement import ViewCampaignVideoEngagement, ViewAdSetVideoEngagement, ViewAdVideoEngagement
from Turing.Api.Catalogs.Views.ViewMaster import ViewMaster


class AdsManagerCatalogsViewsDto:

    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    __shared_state = {
        "views": [
            # master view
            ViewMaster(),

            # campaign views
            ViewCampaignAppEngagement(),
            ViewCampaignBiddingAndOptimization(),
            ViewCampaignCarouselEngagement(),
            ViewCampaignCrossDevice(),
            ViewCampaignDelivery(),
            ViewCampaignEngagement(),
            ViewCampaignPerformance(),
            ViewCampaignPerformanceAndClicks(),
            ViewCampaignTargetingAndCreative(),
            ViewCampaignVideoEngagement(),

            # adset views
            ViewAdSetAppEngagement(),
            ViewAdSetBiddingAndOptimization(),
            ViewAdSetCarouselEngagement(),
            ViewAdSetCrossDevice(),
            ViewAdSetDelivery(),
            ViewAdSetEngagement(),
            ViewAdSetPerformance(),
            ViewAdSetPerformanceAndClicks(),
            ViewAdSetTargetingAndCreative(),
            ViewAdSetVideoEngagement(),

            # ad views
            ViewAdAppEngagement(),
            ViewAdBiddingAndOptimization(),
            ViewAdCarouselEngagement(),
            ViewAdCrossDevice(),
            ViewAdDelivery(),
            ViewAdEngagement(),
            ViewAdPerformance(),
            ViewAdPerformanceAndClicks(),
            ViewAdTargetingAndCreative(),
            ViewAdVideoEngagement(),

            # fallback view
            ViewCampaignFallback()
        ]
    }

    def __init__(self):
        super().__init__()
        self.__dict__ = self.__shared_state

    @classmethod
    def get(cls):
        return cls.json_encoder(cls.__shared_state)
