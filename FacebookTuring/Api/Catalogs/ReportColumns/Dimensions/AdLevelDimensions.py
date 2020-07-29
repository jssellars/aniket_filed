from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewColumnsMaster import ViewColumnsMaster
from FacebookTuring.Api.Catalogs.Views.ViewsAdsManager.ViewFieldsBreakdownsMetadata import ViewFieldsBreakdownsMetadata

AD_PERFORMANCE_REPORT_DIMENSIONS = [
    ViewColumnsMaster.account_id,
    ViewColumnsMaster.campaign_id,
    ViewColumnsMaster.campaign_name,
    ViewColumnsMaster.adset_id,
    ViewColumnsMaster.adset_name,
    ViewColumnsMaster.ad_id,
    ViewColumnsMaster.ad_name,
    ViewColumnsMaster.date_time,
    ViewColumnsMaster.objective,
    ViewFieldsBreakdownsMetadata.age_breakdown,
    ViewFieldsBreakdownsMetadata.gender_breakdown,
    ViewFieldsBreakdownsMetadata.placements,
    ViewFieldsBreakdownsMetadata.country,
    ViewFieldsBreakdownsMetadata.region,
    ViewFieldsBreakdownsMetadata.publisher_platform,
    ViewFieldsBreakdownsMetadata.dma,
    ViewFieldsBreakdownsMetadata.frequency_value,
    ViewFieldsBreakdownsMetadata.device_platform,
    ViewFieldsBreakdownsMetadata.action_destination
]
