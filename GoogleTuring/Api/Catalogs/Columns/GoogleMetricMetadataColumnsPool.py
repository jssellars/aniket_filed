from Core.Metadata.Columns.ColumnMetadata import ColumnMetadata
from Core.Metadata.Columns.ColumnType import ColumnType

from GoogleTuring.Infrastructure.Domain.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata


class GoogleMetricMetadataColumnsPool:
    #  Structure fields and parameters
    #  Object names, IDs, statuses, and dates
    absolute_top_impression_percentage = ColumnMetadata(
        GoogleMetricFieldsMetadata.absolute_top_impression_percentage.field_name, ColumnType.text)

    active_view_cpm = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_cpm.field_name, ColumnType.text)

    active_view_ctr = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_ctr.field_name, ColumnType.text)

    active_view_impressions = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_impressions.field_name,
                                             ColumnType.text)

    active_view_measurability = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_measurability.field_name,
                                               ColumnType.text)

    active_view_measurable_cost = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_measurable_cost.field_name,
                                                 ColumnType.text)

    active_view_measurable_impressions = ColumnMetadata(
        GoogleMetricFieldsMetadata.active_view_measurable_impressions.field_name, ColumnType.text)

    active_view_viewability = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_viewability.field_name,
                                             ColumnType.text)

    all_conversion_rate = ColumnMetadata(GoogleMetricFieldsMetadata.all_conversion_rate.field_name, ColumnType.text)

    all_conversions = ColumnMetadata(GoogleMetricFieldsMetadata.all_conversions.field_name, ColumnType.text)

    all_conversion_value = ColumnMetadata(GoogleMetricFieldsMetadata.all_conversion_value.field_name, ColumnType.text)

    average_cost = ColumnMetadata(GoogleMetricFieldsMetadata.average_cost.field_name, ColumnType.text)

    average_cpc = ColumnMetadata(GoogleMetricFieldsMetadata.average_cpc.field_name, ColumnType.text)

    average_cpe = ColumnMetadata(GoogleMetricFieldsMetadata.average_cpe.field_name, ColumnType.text)

    average_cpm = ColumnMetadata(GoogleMetricFieldsMetadata.average_cpm.field_name, ColumnType.text)

    average_cpv = ColumnMetadata(GoogleMetricFieldsMetadata.average_cpv.field_name, ColumnType.text)

    average_pageviews = ColumnMetadata(GoogleMetricFieldsMetadata.average_pageviews.field_name, ColumnType.text)

    average_position = ColumnMetadata(GoogleMetricFieldsMetadata.average_position.field_name, ColumnType.text)

    average_time_on_site = ColumnMetadata(GoogleMetricFieldsMetadata.average_time_on_site.field_name, ColumnType.text)

    bounce_rate = ColumnMetadata(GoogleMetricFieldsMetadata.bounce_rate.field_name, ColumnType.text)

    click_assisted_conversions = ColumnMetadata(GoogleMetricFieldsMetadata.click_assisted_conversions.field_name,
                                                ColumnType.text)

    click_assisted_conversions_over_last_click_conversions = ColumnMetadata(
        GoogleMetricFieldsMetadata.click_assisted_conversions_over_last_click_conversions.field_name, ColumnType.text)

    click_assisted_conversion_value = ColumnMetadata(
        GoogleMetricFieldsMetadata.click_assisted_conversion_value.field_name,
        ColumnType.text)

    clicks = ColumnMetadata(GoogleMetricFieldsMetadata.clicks.field_name, ColumnType.text)

    conversion_rate = ColumnMetadata(GoogleMetricFieldsMetadata.conversion_rate.field_name, ColumnType.text)

    conversions = ColumnMetadata(GoogleMetricFieldsMetadata.conversions.field_name, ColumnType.text)

    conversion_value = ColumnMetadata(GoogleMetricFieldsMetadata.conversion_value.field_name, ColumnType.text)

    cost = ColumnMetadata(GoogleMetricFieldsMetadata.cost.field_name, ColumnType.text)

    cost_per_all_conversion = ColumnMetadata(GoogleMetricFieldsMetadata.cost_per_all_conversion.field_name,
                                             ColumnType.text)

    cost_per_conversion = ColumnMetadata(GoogleMetricFieldsMetadata.cost_per_conversion.field_name, ColumnType.text)

    cost_per_current_model_attributed_conversion = ColumnMetadata(
        GoogleMetricFieldsMetadata.cost_per_current_model_attributed_conversion.field_name, ColumnType.text)

    cross_device_conversions = ColumnMetadata(GoogleMetricFieldsMetadata.cross_device_conversions.field_name,
                                              ColumnType.text)

    ctr = ColumnMetadata(GoogleMetricFieldsMetadata.ctr.field_name, ColumnType.text)

    current_model_attributed_conversions = ColumnMetadata(
        GoogleMetricFieldsMetadata.current_model_attributed_conversions.field_name, ColumnType.text)

    current_model_attributed_conversion_value = ColumnMetadata(
        GoogleMetricFieldsMetadata.current_model_attributed_conversion_value.field_name, ColumnType.text)

    engagement_rate = ColumnMetadata(GoogleMetricFieldsMetadata.engagement_rate.field_name, ColumnType.text)

    engagements = ColumnMetadata(GoogleMetricFieldsMetadata.engagements.field_name, ColumnType.text)

    gmail_forwards = ColumnMetadata(GoogleMetricFieldsMetadata.gmail_forwards.field_name, ColumnType.text)

    gmail_saves = ColumnMetadata(GoogleMetricFieldsMetadata.gmail_saves.field_name, ColumnType.text)

    gmail_secondary_clicks = ColumnMetadata(GoogleMetricFieldsMetadata.gmail_secondary_clicks.field_name,
                                            ColumnType.text)

    impression_assisted_conversions = ColumnMetadata(
        GoogleMetricFieldsMetadata.impression_assisted_conversions.field_name,
        ColumnType.text)

    impression_assisted_conversions_over_last_click_conversions = ColumnMetadata(
        GoogleMetricFieldsMetadata.impression_assisted_conversions_over_last_click_conversions.field_name,
        ColumnType.text)

    impression_assisted_conversion_value = ColumnMetadata(
        GoogleMetricFieldsMetadata.impression_assisted_conversion_value.field_name, ColumnType.text)

    impressions = ColumnMetadata(GoogleMetricFieldsMetadata.impressions.field_name, ColumnType.text)

    interaction_rate = ColumnMetadata(GoogleMetricFieldsMetadata.interaction_rate.field_name, ColumnType.text)

    interactions = ColumnMetadata(GoogleMetricFieldsMetadata.interactions.field_name, ColumnType.text)

    interaction_types = ColumnMetadata(GoogleMetricFieldsMetadata.interaction_types.field_name, ColumnType.text)

    percent_new_visitors = ColumnMetadata(GoogleMetricFieldsMetadata.percent_new_visitors.field_name, ColumnType.text)

    top_impression_percentage = ColumnMetadata(GoogleMetricFieldsMetadata.top_impression_percentage.field_name,
                                               ColumnType.text)

    value_per_all_conversion = ColumnMetadata(GoogleMetricFieldsMetadata.value_per_all_conversion.field_name,
                                              ColumnType.text)

    value_per_conversion = ColumnMetadata(GoogleMetricFieldsMetadata.value_per_conversion.field_name, ColumnType.text)

    value_per_current_model_attributed_conversion = ColumnMetadata(
        GoogleMetricFieldsMetadata.value_per_current_model_attributed_conversion.field_name,
        ColumnType.text)

    video_quartile_100_rate = ColumnMetadata(GoogleMetricFieldsMetadata.video_quartile_100_rate.field_name,
                                             ColumnType.text)

    video_quartile_25_rate = ColumnMetadata(GoogleMetricFieldsMetadata.video_quartile_25_rate.field_name,
                                            ColumnType.text)

    video_quartile_50_rate = ColumnMetadata(GoogleMetricFieldsMetadata.video_quartile_50_rate.field_name,
                                            ColumnType.text)

    video_quartile_75_rate = ColumnMetadata(GoogleMetricFieldsMetadata.video_quartile_75_rate.field_name,
                                            ColumnType.text)

    video_view_rate = ColumnMetadata(GoogleMetricFieldsMetadata.video_view_rate.field_name, ColumnType.text)

    video_views = ColumnMetadata(GoogleMetricFieldsMetadata.video_views.field_name, ColumnType.text)

    view_through_conversions = ColumnMetadata(GoogleMetricFieldsMetadata.view_through_conversions.field_name,
                                              ColumnType.text)

    content_impression_share = ColumnMetadata(GoogleMetricFieldsMetadata.content_impression_share.field_name,
                                              ColumnType.text)

    content_rank_lost_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.content_rank_lost_impression_share.field_name, ColumnType.text)

    num_offline_impressions = ColumnMetadata(GoogleMetricFieldsMetadata.num_offline_impressions.field_name,
                                             ColumnType.text)

    num_offline_interactions = ColumnMetadata(GoogleMetricFieldsMetadata.num_offline_interactions.field_name,
                                              ColumnType.text)

    offline_interaction_rate = ColumnMetadata(GoogleMetricFieldsMetadata.offline_interaction_rate.field_name,
                                              ColumnType.text)

    relative_ctr = ColumnMetadata(GoogleMetricFieldsMetadata.relative_ctr.field_name, ColumnType.text)

    search_absolute_top_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_absolute_top_impression_share.field_name, ColumnType.text)

    search_budget_lost_absolute_top_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_budget_lost_absolute_top_impression_share.field_name,
        ColumnType.text)

    search_budget_lost_top_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_budget_lost_top_impression_share.field_name, ColumnType.text)

    search_exact_match_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_exact_match_impression_share.field_name, ColumnType.text)

    search_impression_share = ColumnMetadata(GoogleMetricFieldsMetadata.search_impression_share.field_name,
                                             ColumnType.text)

    search_rank_lost_absolute_top_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_rank_lost_absolute_top_impression_share.field_name,
        ColumnType.text)

    search_rank_lost_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_rank_lost_impression_share.field_name, ColumnType.text)

    search_rank_lost_top_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_rank_lost_top_impression_share.field_name, ColumnType.text)

    search_top_impression_share = ColumnMetadata(GoogleMetricFieldsMetadata.search_top_impression_share.field_name,
                                                 ColumnType.text)

    average_frequency = ColumnMetadata(GoogleMetricFieldsMetadata.average_frequency.field_name, ColumnType.text)

    content_budget_lost_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.content_budget_lost_impression_share.field_name, ColumnType.text)

    impression_reach = ColumnMetadata(GoogleMetricFieldsMetadata.impression_reach.field_name, ColumnType.text)

    invalid_click_rate = ColumnMetadata(GoogleMetricFieldsMetadata.invalid_click_rate.field_name, ColumnType.text)

    invalid_clicks = ColumnMetadata(GoogleMetricFieldsMetadata.invalid_clicks.field_name, ColumnType.text)

    search_budget_lost_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_budget_lost_impression_share.field_name, ColumnType.text)

    search_click_share = ColumnMetadata(GoogleMetricFieldsMetadata.search_click_share.field_name, ColumnType.text)

    historical_creative_quality_score = ColumnMetadata(
        GoogleMetricFieldsMetadata.historical_creative_quality_score.field_name, ColumnType.text)

    historical_landing_page_quality_score = ColumnMetadata(
        GoogleMetricFieldsMetadata.historical_landing_page_quality_score.field_name, ColumnType.text)

    historical_quality_score = ColumnMetadata(GoogleMetricFieldsMetadata.historical_quality_score.field_name,
                                              ColumnType.text)

    historical_search_predicted_ctr = ColumnMetadata(
        GoogleMetricFieldsMetadata.historical_search_predicted_ctr.field_name,
        ColumnType.text)
