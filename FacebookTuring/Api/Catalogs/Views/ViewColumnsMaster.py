from FacebookTuring.Api.Catalogs.Views.ViewFieldsCustomMetadata import ViewFieldsCustomMetadata
from FacebookTuring.Api.Catalogs.Views.ViewFieldsMetricEngagementMetadata import ViewFieldsMetricEngagementMetadata
from FacebookTuring.Api.Catalogs.Views.ViewFieldsMetricPerformanceMetadata import ViewFieldsMetricPerformanceMetadata
from FacebookTuring.Api.Catalogs.Views.ViewFieldsMetricStandardEventsMetadata import \
    ViewFieldsMetricStandardEventsMetadata
from FacebookTuring.Api.Catalogs.Views.ViewFieldsMetricStructureMetadata import ViewFieldsMetricStructureMetadata
from FacebookTuring.Api.Catalogs.Views.ViewFieldsStructureMetadata import ViewFieldsStructureMetadata


class ViewColumnsMaster(ViewFieldsCustomMetadata,
                        ViewFieldsMetricEngagementMetadata,
                        ViewFieldsMetricPerformanceMetadata,
                        ViewFieldsMetricStandardEventsMetadata,
                        ViewFieldsMetricStructureMetadata,
                        ViewFieldsStructureMetadata):
    pass
