from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.CampaignGenderDimensionColumnsMaster import \
    CampaignGenderDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.CampaignGenderMetricColumnsMaster import \
    CampaignGenderMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.SegmentColumnsBase import SegmentColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.SegmentColumnsMaster import SegmentColumnsMaster


class CampaignGenderSegmentColumnsMaster(SegmentColumnsBase):
    AVAILABLE_DIMENSIONS = CampaignGenderDimensionColumnsMaster.DIMENSIONS
    AVAILABLE_METRICS = CampaignGenderMetricColumnsMaster.METRICS
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
