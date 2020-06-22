from Core.Tools.Misc.ObjectSerializers import object_to_json, object_to_attribute_values_list
from FacebookTuring.Api.Catalogs.BusinessViews.ViewAppEngagement import ViewCampaignAppEngagement, \
    ViewAdSetAppEngagement, ViewAdAppEngagement
from FacebookTuring.Api.Catalogs.BusinessViews.ViewBiddingAndOptimization import ViewCampaignBiddingAndOptimization, \
    ViewAdSetBiddingAndOptimization, ViewAdBiddingAndOptimization
from FacebookTuring.Api.Catalogs.BusinessViews.ViewCarouselEngagement import ViewCampaignCarouselEngagement, \
    ViewAdSetCarouselEngagement, ViewAdCarouselEngagement
from FacebookTuring.Api.Catalogs.BusinessViews.ViewCrossDevice import ViewCampaignCrossDevice, ViewAdSetCrossDevice, \
    ViewAdCrossDevice
from FacebookTuring.Api.Catalogs.BusinessViews.ViewDelivery import ViewCampaignDelivery, ViewAdSetDelivery, \
    ViewAdDelivery
from FacebookTuring.Api.Catalogs.BusinessViews.ViewEngagement import ViewCampaignEngagement, ViewAdSetEngagement, \
    ViewAdEngagement
from FacebookTuring.Api.Catalogs.BusinessViews.ViewPerformance import ViewCampaignFallback, ViewCampaignPerformance, \
    ViewAdSetFallback, ViewAdSetPerformance, ViewAdFallback, ViewAdPerformance
from FacebookTuring.Api.Catalogs.BusinessViews.ViewPerformanceAndClicks import ViewCampaignPerformanceAndClicks, \
    ViewAdSetPerformanceAndClicks, ViewAdPerformanceAndClicks
from FacebookTuring.Api.Catalogs.BusinessViews.ViewTargetingAndCreative import ViewCampaignTargetingAndCreative, \
    ViewAdSetTargetingAndCreative, ViewAdTargetingAndCreative
from FacebookTuring.Api.Catalogs.BusinessViews.ViewVideoEngagement import ViewCampaignVideoEngagement, \
    ViewAdSetVideoEngagement, ViewAdVideoEngagement
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewMaster import ViewMaster


class AdsManagerCatalogsViewsByLevelDto:
    json_encoder = object_to_json
    json_list_encoder = object_to_attribute_values_list

    vCampaignInsights = {
        "views": [
            # master view
            ViewMaster(),
            # fallback view
            ViewCampaignFallback(),

            ViewCampaignAppEngagement(),
            ViewCampaignBiddingAndOptimization(),
            ViewCampaignCarouselEngagement(),
            ViewCampaignCrossDevice(),
            ViewCampaignDelivery(),
            ViewCampaignEngagement(),
            ViewCampaignPerformance(),
            ViewCampaignPerformanceAndClicks(),
            ViewCampaignTargetingAndCreative(),
            ViewCampaignVideoEngagement()]
    }
    vAdSetInsights = {
        "views": [
            # master view
            ViewMaster(),
            # fallback view
            ViewAdSetFallback(),

            ViewAdSetAppEngagement(),
            ViewAdSetBiddingAndOptimization(),
            ViewAdSetCarouselEngagement(),
            ViewAdSetCrossDevice(),
            ViewAdSetDelivery(),
            ViewAdSetEngagement(),
            ViewAdSetPerformance(),
            ViewAdSetPerformanceAndClicks(),
            ViewAdSetTargetingAndCreative(),
            ViewAdSetVideoEngagement()
        ]
    }

    vAdInsights = {
        "views": [
            # master view
            ViewMaster(),
            # fallback view
            ViewAdFallback(),

            ViewAdAppEngagement(),
            ViewAdBiddingAndOptimization(),
            ViewAdCarouselEngagement(),
            ViewAdCrossDevice(),
            ViewAdDelivery(),
            ViewAdEngagement(),
            ViewAdPerformance(),
            ViewAdPerformanceAndClicks(),
            ViewAdTargetingAndCreative(),
            ViewAdVideoEngagement()
        ]
    }

    def __init__(self):
        super().__init__()

    @classmethod
    def get(cls, level):
        return cls.json_encoder(getattr(cls, level))
