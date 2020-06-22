from Core.Metadata.Columns.ViewColumns.SegmentColumn import SegmentColumn
from Core.Tools.Misc.Autoincrement import Autoincrement
from GoogleTuring.Api.Catalogs.Columns.GoogleSegmentMetadataColumnsPool import GoogleSegmentMetadataColumnsPool
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.MetricColumnsMaster import MetricColumnsMaster


class SegmentColumnsMaster:
    __id = Autoincrement(0)
    ad_network_type_1 = SegmentColumn(id=__id.increment(),
                                      column_name=GoogleSegmentMetadataColumnsPool.ad_network_type_1.name,
                                      display_name="Ad network type 1", not_supported_dimensions=[],
                                      not_supported_metrics=[])
    ad_network_type_2 = SegmentColumn(id=__id.increment(),
                                      column_name=GoogleSegmentMetadataColumnsPool.ad_network_type_2.name,
                                      display_name="Ad network type 2", not_supported_dimensions=[],
                                      not_supported_metrics=[])
    click_type = SegmentColumn(id=__id.increment(),
                               column_name=GoogleSegmentMetadataColumnsPool.click_type.name,
                               display_name="Click type",
                               not_supported_dimensions=[],
                               not_supported_metrics=[MetricColumnsMaster.absolute_top_impression_percentage,
                                                      MetricColumnsMaster.average_cpe,
                                                      MetricColumnsMaster.average_cpv,
                                                      MetricColumnsMaster.average_frequency,
                                                      MetricColumnsMaster.average_pageviews,
                                                      MetricColumnsMaster.average_time_on_site,
                                                      MetricColumnsMaster.bounce_rate,
                                                      MetricColumnsMaster.click_assisted_conversion_value,
                                                      MetricColumnsMaster.click_assisted_conversions,
                                                      MetricColumnsMaster.click_assisted_conversions_over_last_click_conversions,
                                                      MetricColumnsMaster.content_budget_lost_impression_share,
                                                      MetricColumnsMaster.content_impression_share,
                                                      MetricColumnsMaster.content_rank_lost_impression_share,
                                                      # MetricColumnsMaster.conversion_lag_bucket,
                                                      MetricColumnsMaster.engagement_rate,
                                                      MetricColumnsMaster.engagements,
                                                      MetricColumnsMaster.impression_assisted_conversion_value,
                                                      MetricColumnsMaster.impression_assisted_conversions,
                                                      MetricColumnsMaster.impression_assisted_conversions_over_last_click_conversions,
                                                      MetricColumnsMaster.impression_reach,
                                                      MetricColumnsMaster.percent_new_visitors,
                                                      MetricColumnsMaster.relative_ctr,
                                                      MetricColumnsMaster.search_absolute_top_impression_share,
                                                      MetricColumnsMaster.search_budget_lost_absolute_top_impression_share,
                                                      MetricColumnsMaster.search_budget_lost_impression_share,
                                                      MetricColumnsMaster.search_budget_lost_top_impression_share,
                                                      MetricColumnsMaster.search_click_share,
                                                      MetricColumnsMaster.search_exact_match_impression_share,
                                                      MetricColumnsMaster.search_impression_share,
                                                      MetricColumnsMaster.search_rank_lost_absolute_top_impression_share,
                                                      MetricColumnsMaster.search_rank_lost_impression_share,
                                                      MetricColumnsMaster.search_rank_lost_top_impression_share,
                                                      MetricColumnsMaster.search_top_impression_share,
                                                      MetricColumnsMaster.top_impression_percentage,
                                                      MetricColumnsMaster.video_quartile_100_rate,
                                                      MetricColumnsMaster.video_quartile_25_rate,
                                                      MetricColumnsMaster.video_quartile_50_rate,
                                                      MetricColumnsMaster.video_quartile_75_rate,
                                                      MetricColumnsMaster.video_view_rate,
                                                      MetricColumnsMaster.video_views,
                                                      MetricColumnsMaster.view_through_conversions,
                                                      ])
    conversion_adjustment_lag_bucket = SegmentColumn(id=__id.increment(),
                                                     column_name=GoogleSegmentMetadataColumnsPool.conversion_adjustment_lag_bucket.name,
                                                     display_name="Conversion adjustment lag bucket",
                                                     not_supported_dimensions=[], not_supported_metrics=[])
    conversion_lag_bucket = SegmentColumn(id=__id.increment(),
                                          column_name=GoogleSegmentMetadataColumnsPool.conversion_lag_bucket.name,
                                          display_name="Conversion lag bucket", not_supported_dimensions=[],
                                          not_supported_metrics=[])
    conversion_tracker_id = SegmentColumn(id=__id.increment(),
                                          column_name=GoogleSegmentMetadataColumnsPool.conversion_tracker_id.name,
                                          display_name="Conversion tracker id", not_supported_dimensions=[],
                                          not_supported_metrics=[])
    conversion_type_name = SegmentColumn(id=__id.increment(),
                                         column_name=GoogleSegmentMetadataColumnsPool.conversion_type_name.name,
                                         display_name="Conversion type name", not_supported_dimensions=[],
                                         not_supported_metrics=[])
    criterion_id = SegmentColumn(id=__id.increment(),
                                 column_name=GoogleSegmentMetadataColumnsPool.criterion_id.name,
                                 display_name="Criterion id", not_supported_dimensions=[], not_supported_metrics=[])
    criterion_type = SegmentColumn(id=__id.increment(),
                                   column_name=GoogleSegmentMetadataColumnsPool.criterion_type.name,
                                   display_name="Criterion type", not_supported_dimensions=[],
                                   not_supported_metrics=[])
    date = SegmentColumn(id=__id.increment(), column_name=GoogleSegmentMetadataColumnsPool.date.name,
                         display_name="Date", not_supported_dimensions=[], not_supported_metrics=[])
    day_of_week = SegmentColumn(id=__id.increment(),
                                column_name=GoogleSegmentMetadataColumnsPool.day_of_week.name,
                                display_name="Day of week", not_supported_dimensions=[], not_supported_metrics=[])
    device = SegmentColumn(id=__id.increment(), column_name=GoogleSegmentMetadataColumnsPool.device.name,
                           display_name="Device", not_supported_dimensions=[], not_supported_metrics=[])
    external_conversion_source = SegmentColumn(id=__id.increment(),
                                               column_name=GoogleSegmentMetadataColumnsPool.external_conversion_source.name,
                                               display_name="External conversion source", not_supported_dimensions=[],
                                               not_supported_metrics=[])
    month = SegmentColumn(id=__id.increment(), column_name=GoogleSegmentMetadataColumnsPool.month.name,
                          display_name="Month", not_supported_dimensions=[], not_supported_metrics=[])
    month_of_year = SegmentColumn(id=__id.increment(),
                                  column_name=GoogleSegmentMetadataColumnsPool.month_of_year.name,
                                  display_name="Month of year", not_supported_dimensions=[], not_supported_metrics=[])
    quarter = SegmentColumn(id=__id.increment(),
                            column_name=GoogleSegmentMetadataColumnsPool.quarter.name,
                            display_name="Quarter", not_supported_dimensions=[], not_supported_metrics=[])
    slot = SegmentColumn(id=__id.increment(), column_name=GoogleSegmentMetadataColumnsPool.slot.name,
                         display_name="Slot", not_supported_dimensions=[], not_supported_metrics=[])
    week = SegmentColumn(id=__id.increment(), column_name=GoogleSegmentMetadataColumnsPool.week.name,
                         display_name="Week", not_supported_dimensions=[], not_supported_metrics=[])
    year = SegmentColumn(id=__id.increment(), column_name=GoogleSegmentMetadataColumnsPool.year.name,
                         display_name="Year", not_supported_dimensions=[], not_supported_metrics=[])
    hour_of_day = SegmentColumn(id=__id.increment(),
                                column_name=GoogleSegmentMetadataColumnsPool.hour_of_day.name,
                                display_name="Hour of day", not_supported_dimensions=[], not_supported_metrics=[])
    conversion_attribution_event_type = SegmentColumn(id=__id.increment(),
                                                      column_name=GoogleSegmentMetadataColumnsPool.conversion_attribution_event_type.name,
                                                      display_name="Conversion attribution event type",
                                                      not_supported_dimensions=[], not_supported_metrics=[])
    ad_format = SegmentColumn(id=__id.increment(),
                              column_name=GoogleSegmentMetadataColumnsPool.ad_format.name,
                              display_name="Ad format", not_supported_dimensions=[], not_supported_metrics=[])
    location_type = SegmentColumn(id=__id.increment(),
                                  column_name=GoogleSegmentMetadataColumnsPool.location_type.name,
                                  display_name="Location type", not_supported_dimensions=[], not_supported_metrics=[])
    conversion_category_name = SegmentColumn(id=__id.increment(),
                                             column_name=GoogleSegmentMetadataColumnsPool.conversion_category_name.name,
                                             display_name="Conversion category name", not_supported_dimensions=[],
                                             not_supported_metrics=[])
    ad_group_id_segment = SegmentColumn(id=__id.increment(),
                                        column_name=GoogleSegmentMetadataColumnsPool.ad_group_id_segment.name,
                                        display_name="Ad group id segment", not_supported_dimensions=[],
                                        not_supported_metrics=[])
    ad_group_name_segment = SegmentColumn(id=__id.increment(),
                                          column_name=GoogleSegmentMetadataColumnsPool.ad_group_name_segment.name,
                                          display_name="Ad group name segment", not_supported_dimensions=[],
                                          not_supported_metrics=[])
    ad_group_status_segment = SegmentColumn(id=__id.increment(),
                                            column_name=GoogleSegmentMetadataColumnsPool.ad_group_status_segment.name,
                                            display_name="Ad group status segment", not_supported_dimensions=[],
                                            not_supported_metrics=[])
