from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.CampaignAgeRangeDimensionColumnsMaster import \
    CampaignAgeRangeDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.AgeRange.CampaignAgeRangeMetricColumnsMaster import \
    CampaignAgeRangeMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.SegmentColumnsBase import SegmentColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.SegmentColumnsMaster import SegmentColumnsMaster


class CampaignAgeRangeSegmentColumnsMaster(SegmentColumnsBase):
    AVAILABLE_DIMENSIONS = CampaignAgeRangeDimensionColumnsMaster.DIMENSIONS
    AVAILABLE_METRICS = CampaignAgeRangeMetricColumnsMaster.METRICS

    SEGMENTS = [
        SegmentColumnsMaster.ad_network_type_1,
        SegmentColumnsMaster.ad_network_type_2,
        SegmentColumnsMaster.click_type,
        SegmentColumnsMaster.conversion_category_name,
        SegmentColumnsMaster.conversion_tracker_id,
        SegmentColumnsMaster.conversion_type_name,
        SegmentColumnsMaster.date,
        SegmentColumnsMaster.day_of_week,
        SegmentColumnsMaster.device,
        SegmentColumnsMaster.external_conversion_source,
        SegmentColumnsMaster.month,
        SegmentColumnsMaster.month_of_year,
        SegmentColumnsMaster.quarter,
        SegmentColumnsMaster.week,
        SegmentColumnsMaster.year,
    ]
