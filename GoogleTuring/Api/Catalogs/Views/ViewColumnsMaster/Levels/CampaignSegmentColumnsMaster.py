from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.CampaignDimensionColumnsMaster import \
    CampaignDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.CampaignMetricColumnsMaster import \
    CampaignMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.SegmentColumnsBase import SegmentColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.SegmentColumnsMaster import SegmentColumnsMaster


class CampaignSegmentColumnsMaster(SegmentColumnsBase):
    AVAILABLE_DIMENSIONS = CampaignDimensionColumnsMaster.DIMENSIONS
    AVAILABLE_METRICS = CampaignMetricColumnsMaster.METRICS

    SEGMENTS = [
        SegmentColumnsMaster.ad_network_type_1,
        SegmentColumnsMaster.ad_network_type_2,
        SegmentColumnsMaster.click_type,
        SegmentColumnsMaster.conversion_adjustment_lag_bucket,
        SegmentColumnsMaster.conversion_attribution_event_type,
        SegmentColumnsMaster.conversion_category_name,
        SegmentColumnsMaster.conversion_lag_bucket,
        SegmentColumnsMaster.conversion_tracker_id,
        SegmentColumnsMaster.conversion_type_name,
        SegmentColumnsMaster.date,
        SegmentColumnsMaster.day_of_week,
        SegmentColumnsMaster.device,
        SegmentColumnsMaster.external_conversion_source,
        SegmentColumnsMaster.hour_of_day,
        SegmentColumnsMaster.month,
        SegmentColumnsMaster.month_of_year,
        SegmentColumnsMaster.quarter,
        SegmentColumnsMaster.slot,
        SegmentColumnsMaster.week,
        SegmentColumnsMaster.year,
    ]
