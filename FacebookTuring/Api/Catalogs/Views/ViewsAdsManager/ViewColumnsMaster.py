from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewFieldsCustomMetadata import ViewFieldsCustomMetadata
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewFieldsMetricEngagementMetadata import \
    ViewFieldsMetricEngagementMetadata
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewFieldsMetricPerformanceMetadata import \
    ViewFieldsMetricPerformanceMetadata
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewFieldsMetricStandardEventsMetadata import \
    ViewFieldsMetricStandardEventsMetadata
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewFieldsMetricStructureMetadata import \
    ViewFieldsMetricStructureMetadata
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewFieldsStructureMetadata import ViewFieldsStructureMetadata


class ViewColumnsMaster(ViewFieldsCustomMetadata,
                        ViewFieldsMetricEngagementMetadata,
                        ViewFieldsMetricPerformanceMetadata,
                        ViewFieldsMetricStandardEventsMetadata,
                        ViewFieldsMetricStructureMetadata,
                        ViewFieldsStructureMetadata):
    pass
