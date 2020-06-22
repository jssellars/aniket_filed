from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.Levels.Breakdowns.Gender.CampaignGenderDimensionColumnsMaster import \
    CampaignGenderDimensionColumnsMaster
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.MetricColumnsBase import MetricColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.MetricColumnsMaster import MetricColumnsMaster


class CampaignGenderMetricColumnsMaster(MetricColumnsBase):
    AVAILABLE_DIMENSIONS = CampaignGenderDimensionColumnsMaster.DIMENSIONS
    METRICS = [
        MetricColumnsMaster.active_view_cpm,
        MetricColumnsMaster.active_view_ctr,
        MetricColumnsMaster.active_view_impressions,
        MetricColumnsMaster.active_view_measurability,
        MetricColumnsMaster.active_view_measurable_cost,
        MetricColumnsMaster.active_view_measurable_impressions,
        MetricColumnsMaster.active_view_viewability,
        MetricColumnsMaster.all_conversion_rate,
        MetricColumnsMaster.all_conversions,
        MetricColumnsMaster.all_conversion_value,
        MetricColumnsMaster.average_cost,
        MetricColumnsMaster.average_cpc,
        MetricColumnsMaster.average_cpe,
        MetricColumnsMaster.average_cpm,
        MetricColumnsMaster.average_cpv,
        MetricColumnsMaster.clicks,
        MetricColumnsMaster.conversion_rate,
        MetricColumnsMaster.conversions,
        MetricColumnsMaster.conversion_value,
        MetricColumnsMaster.cost,
        MetricColumnsMaster.cost_per_all_conversion,
        MetricColumnsMaster.cost_per_conversion,
        MetricColumnsMaster.cross_device_conversions,
        MetricColumnsMaster.ctr,
        MetricColumnsMaster.engagement_rate,
        MetricColumnsMaster.engagements,
        MetricColumnsMaster.gmail_forwards,
        MetricColumnsMaster.gmail_saves,
        MetricColumnsMaster.gmail_secondary_clicks,
        MetricColumnsMaster.impressions,
        MetricColumnsMaster.interaction_rate,
        MetricColumnsMaster.interactions,
        MetricColumnsMaster.interaction_types,
        MetricColumnsMaster.value_per_all_conversion,
        MetricColumnsMaster.value_per_conversion,
        MetricColumnsMaster.video_quartile_100_rate,
        MetricColumnsMaster.video_quartile_25_rate,
        MetricColumnsMaster.video_quartile_50_rate,
        MetricColumnsMaster.video_quartile_75_rate,
        MetricColumnsMaster.video_view_rate,
        MetricColumnsMaster.video_views,
        MetricColumnsMaster.view_through_conversions,
    ]
