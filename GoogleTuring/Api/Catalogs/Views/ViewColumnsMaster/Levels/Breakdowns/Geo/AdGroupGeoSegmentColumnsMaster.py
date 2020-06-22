from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Geo.AdGroupGeoDimensionColumnsMaster import \
    AdGroupGeoDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Geo.AdGroupGeoMetricColumnsMaster import \
    AdGroupGeoMetricColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.SegmentColumnsBase import SegmentColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.SegmentColumnsMaster import SegmentColumnsMaster


class AdGroupGeoSegmentColumnsMaster(SegmentColumnsBase):
    AVAILABLE_DIMENSIONS = AdGroupGeoDimensionColumnsMaster.DIMENSIONS
    AVAILABLE_METRICS = AdGroupGeoMetricColumnsMaster.METRICS
    SEGMENTS = [
        SegmentColumnsMaster.ad_format,
        SegmentColumnsMaster.ad_group_id_segment,
        SegmentColumnsMaster.ad_group_name_segment,
        SegmentColumnsMaster.ad_group_status_segment,
        SegmentColumnsMaster.ad_network_type_1,
        SegmentColumnsMaster.ad_network_type_2,
        SegmentColumnsMaster.conversion_category_name,
        SegmentColumnsMaster.conversion_tracker_id,
        SegmentColumnsMaster.conversion_type_name,
        SegmentColumnsMaster.date,
        SegmentColumnsMaster.day_of_week,
        SegmentColumnsMaster.device,
        SegmentColumnsMaster.external_conversion_source,
        SegmentColumnsMaster.location_type,
        SegmentColumnsMaster.month,
        SegmentColumnsMaster.month_of_year,
        SegmentColumnsMaster.quarter,
        SegmentColumnsMaster.week,
        SegmentColumnsMaster.year,
    ]
