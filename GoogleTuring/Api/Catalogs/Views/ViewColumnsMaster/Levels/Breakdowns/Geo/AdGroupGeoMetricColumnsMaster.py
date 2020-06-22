from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Geo.AdGroupGeoDimensionColumnsMaster import \
    AdGroupGeoDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.MetricColumnsBase import MetricColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.MetricColumnsMaster import MetricColumnsMaster


class AdGroupGeoMetricColumnsMaster(MetricColumnsBase):
    AVAILABLE_DIMENSIONS = AdGroupGeoDimensionColumnsMaster.DIMENSIONS
    METRICS = [
        MetricColumnsMaster.absolute_top_impression_percentage,
        MetricColumnsMaster.all_conversion_rate,
        MetricColumnsMaster.all_conversions,
        MetricColumnsMaster.all_conversion_value,
        MetricColumnsMaster.average_cost,
        MetricColumnsMaster.average_cpc,
        MetricColumnsMaster.average_cpm,
        MetricColumnsMaster.average_cpv,
        MetricColumnsMaster.average_position,
        MetricColumnsMaster.clicks,
        MetricColumnsMaster.conversion_rate,
        MetricColumnsMaster.conversions,
        MetricColumnsMaster.conversion_value,
        MetricColumnsMaster.cost,
        MetricColumnsMaster.cost_per_all_conversion,
        MetricColumnsMaster.cost_per_conversion,
        MetricColumnsMaster.cross_device_conversions,
        MetricColumnsMaster.ctr,
        MetricColumnsMaster.impressions,
        MetricColumnsMaster.interaction_rate,
        MetricColumnsMaster.interactions,
        MetricColumnsMaster.interaction_types,
        MetricColumnsMaster.top_impression_percentage,
        MetricColumnsMaster.value_per_all_conversion,
        MetricColumnsMaster.value_per_conversion,
        MetricColumnsMaster.video_view_rate,
        MetricColumnsMaster.video_views,
        MetricColumnsMaster.view_through_conversions,
    ]
