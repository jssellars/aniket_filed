from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Keywords.CampaignKeywordsDimensionColumnsMaster import \
    CampaignKeywordsDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Keywords.CampaignKeywordsMetricColumnsMaster import \
    CampaignKeywordsMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.SegmentColumnsBase import SegmentColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.SegmentColumnsMaster import SegmentColumnsMaster


class CampaignKeywordsSegmentColumnsMaster(SegmentColumnsBase):
    AVAILABLE_DIMENSIONS = CampaignKeywordsDimensionColumnsMaster.DIMENSIONS
    AVAILABLE_METRICS = CampaignKeywordsMetricColumnsMaster.METRICS
    SEGMENTS = [
        SegmentColumnsMaster.ad_network_type_1,
        SegmentColumnsMaster.ad_network_type_2,
        SegmentColumnsMaster.click_type,
        SegmentColumnsMaster.conversion_adjustment_lag_bucket,
        SegmentColumnsMaster.conversion_category_name,
        SegmentColumnsMaster.conversion_lag_bucket,
        SegmentColumnsMaster.conversion_tracker_id,
        SegmentColumnsMaster.conversion_type_name,
        SegmentColumnsMaster.date,
        SegmentColumnsMaster.day_of_week,
        SegmentColumnsMaster.device,
        SegmentColumnsMaster.external_conversion_source,
        SegmentColumnsMaster.month,
        SegmentColumnsMaster.month_of_year,
        SegmentColumnsMaster.quarter,
        SegmentColumnsMaster.slot,
        SegmentColumnsMaster.week,
        SegmentColumnsMaster.year,
    ]
