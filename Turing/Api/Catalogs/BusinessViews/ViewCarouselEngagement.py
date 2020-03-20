from Turing.Api.Catalogs.Views.ViewBase import View
from Turing.Api.Catalogs.Views.ViewColumnsMaster import ViewColumnsMaster


class ViewCarouselEngagementBase(View):
    name = "App engagement"
    type = "Business"


class ViewCampaignCarouselEngagement(ViewCarouselEngagementBase):
    tableName = "vCampaignInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.campaign_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.link_click,
        ViewColumnsMaster.unique_link_click,
        # TODO: get COST per unique click (all)
        # ViewColumnsMaster.costPerUniqueInlineLinkClick,
        ViewColumnsMaster.unique_ctr,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.cpm,
        # TODO: get actions column ??
        # TODO: get people taking actions column ??
        # ViewColumnsMaster.mobileAppInstall,
        # ViewColumnsMaster.offsiteConversionFbPixelLead,
        # ViewColumnsMaster.offsiteConversionFbPixelViewContent,
        # ViewColumnsMaster.offsiteConversionFbPixelCompleteRegistration,
        # ViewColumnsMaster.offsiteConversionFbPixelAddToCart,
        # ViewColumnsMaster.offsiteConversionFbPixelInitiateCheckout,
        #  TODO: get COST per lead ( and others non-unique below )column
        # ViewColumnsMaster.costPerUniqueLead,
        # ViewColumnsMaster.costPerUniqueViewContent,
        # ViewColumnsMaster.costPerUniqueCompleteRegistration,
        # ViewColumnsMaster.costPerUniqueAddToCart,
        # ViewColumnsMaster.costPerUniqueInitiateCheckout
    ]


class ViewAdSetCarouselEngagement(ViewCarouselEngagementBase):
    tableName = "vAdSetInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.adset_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.link_click,
        ViewColumnsMaster.unique_link_click,
        # TODO: get COST per unique click (all)
        # ViewColumnsMaster.costPerUniqueInlineLinkClick,
        ViewColumnsMaster.unique_ctr,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.cpm,
        # TODO: get actions column ??
        # TODO: get people taking actions column ??
        # ViewColumnsMaster.mobileAppInstall,
        # ViewColumnsMaster.offsiteConversionFbPixelLead,
        # ViewColumnsMaster.offsiteConversionFbPixelViewContent,
        # ViewColumnsMaster.offsiteConversionFbPixelCompleteRegistration,
        # ViewColumnsMaster.offsiteConversionFbPixelAddToCart,
        # ViewColumnsMaster.offsiteConversionFbPixelInitiateCheckout,
        # #  TODO: get COST per lead ( and others non-unique below )column
        # ViewColumnsMaster.costPerUniqueLead,
        # ViewColumnsMaster.costPerUniqueViewContent,
        # ViewColumnsMaster.costPerUniqueCompleteRegistration,
        # ViewColumnsMaster.costPerUniqueAddToCart,
        # ViewColumnsMaster.costPerUniqueInitiateCheckout
    ]


class ViewAdCarouselEngagement(ViewCarouselEngagementBase):
    tableName = "vAdInsights"
    columns = [
        ViewColumnsMaster.effective_status,
        ViewColumnsMaster.ad_name,
        ViewColumnsMaster.delivery,
        ViewColumnsMaster.reach,
        ViewColumnsMaster.frequency,
        ViewColumnsMaster.impressions,
        ViewColumnsMaster.link_click,
        ViewColumnsMaster.unique_link_click,
        # TODO: get COST per unique click (all)
        # ViewColumnsMaster.costPerUniqueInlineLinkClick,
        ViewColumnsMaster.unique_ctr,
        ViewColumnsMaster.spend,
        ViewColumnsMaster.cpm,
        # TODO: get actions column ??
        # TODO: get people taking actions column ??
        # ViewColumnsMaster.mobileAppInstall,
        # ViewColumnsMaster.offsiteConversionFbPixelLead,
        # ViewColumnsMaster.offsiteConversionFbPixelViewContent,
        # ViewColumnsMaster.offsiteConversionFbPixelCompleteRegistration,
        # ViewColumnsMaster.offsiteConversionFbPixelAddToCart,
        # ViewColumnsMaster.offsiteConversionFbPixelInitiateCheckout,
        # #  TODO: get COST per lead ( and others non-unique below )column
        # ViewColumnsMaster.costPerUniqueLead,
        # ViewColumnsMaster.costPerUniqueViewContent,
        # ViewColumnsMaster.costPerUniqueCompleteRegistration,
        # ViewColumnsMaster.costPerUniqueAddToCart,
        # ViewColumnsMaster.costPerUniqueInitiateCheckout
    ]
