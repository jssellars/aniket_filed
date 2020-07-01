from Core.Metadata.Columns.ColumnMetadata import ColumnMetadata
from Core.Metadata.Columns.ColumnType import ColumnType

from GoogleTuring.Infrastructure.Domain.GoogleMetricFieldsMetadata import GoogleMetricFieldsMetadata


class GoogleMetricMetadataColumnsPool:
    #  Structure fields and parameters
    #  Object names, IDs, statuses, and dates
    absolute_top_impression_percentage = ColumnMetadata(
        GoogleMetricFieldsMetadata.absolute_top_impression_percentage.name, ColumnType.text)

    active_view_cpm = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_cpm.name, ColumnType.text)

    active_view_ctr = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_ctr.name, ColumnType.text)

    active_view_impressions = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_impressions.name,
                                             ColumnType.text)

    active_view_measurability = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_measurability.name,
                                               ColumnType.text)

    active_view_measurable_cost = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_measurable_cost.name,
                                                 ColumnType.text)

    active_view_measurable_impressions = ColumnMetadata(
        GoogleMetricFieldsMetadata.active_view_measurable_impressions.name, ColumnType.text)

    active_view_viewability = ColumnMetadata(GoogleMetricFieldsMetadata.active_view_viewability.name,
                                             ColumnType.text)

    all_conversion_rate = ColumnMetadata(GoogleMetricFieldsMetadata.all_conversion_rate.name, ColumnType.text)

    all_conversions = ColumnMetadata(GoogleMetricFieldsMetadata.all_conversions.name, ColumnType.text)

    all_conversion_value = ColumnMetadata(GoogleMetricFieldsMetadata.all_conversion_value.name, ColumnType.text)

    average_cost = ColumnMetadata(GoogleMetricFieldsMetadata.average_cost.name, ColumnType.text)

    average_cpc = ColumnMetadata(GoogleMetricFieldsMetadata.average_cpc.name, ColumnType.text)

    average_cpe = ColumnMetadata(GoogleMetricFieldsMetadata.average_cpe.name, ColumnType.text)

    average_cpm = ColumnMetadata(GoogleMetricFieldsMetadata.average_cpm.name, ColumnType.text)

    average_cpv = ColumnMetadata(GoogleMetricFieldsMetadata.average_cpv.name, ColumnType.text)

    average_pageviews = ColumnMetadata(GoogleMetricFieldsMetadata.average_pageviews.name, ColumnType.text)

    average_position = ColumnMetadata(GoogleMetricFieldsMetadata.average_position.name, ColumnType.text)

    average_time_on_site = ColumnMetadata(GoogleMetricFieldsMetadata.average_time_on_site.name, ColumnType.text)

    bounce_rate = ColumnMetadata(GoogleMetricFieldsMetadata.bounce_rate.name, ColumnType.text)

    click_assisted_conversions = ColumnMetadata(GoogleMetricFieldsMetadata.click_assisted_conversions.name,
                                                ColumnType.text)

    click_assisted_conversions_over_last_click_conversions = ColumnMetadata(
        GoogleMetricFieldsMetadata.click_assisted_conversions_over_last_click_conversions.name, ColumnType.text)

    click_assisted_conversion_value = ColumnMetadata(
        GoogleMetricFieldsMetadata.click_assisted_conversion_value.name,
        ColumnType.text)

    clicks = ColumnMetadata(GoogleMetricFieldsMetadata.clicks.name, ColumnType.text)

    link_clicks = ColumnMetadata(GoogleMetricFieldsMetadata.link_clicks.name, ColumnType.text)

    conversion_rate = ColumnMetadata(GoogleMetricFieldsMetadata.conversion_rate.name, ColumnType.text)

    conversions = ColumnMetadata(GoogleMetricFieldsMetadata.conversions.name, ColumnType.text)

    leads = ColumnMetadata(GoogleMetricFieldsMetadata.leads.name, ColumnType.text)

    conversion_value = ColumnMetadata(GoogleMetricFieldsMetadata.conversion_value.name, ColumnType.text)

    purchases = ColumnMetadata(GoogleMetricFieldsMetadata.purchases.name, ColumnType.text)

    purchase_value = ColumnMetadata(GoogleMetricFieldsMetadata.purchase_value.name, ColumnType.text)

    cost = ColumnMetadata(GoogleMetricFieldsMetadata.cost.name, ColumnType.text)

    cost_per_all_conversion = ColumnMetadata(GoogleMetricFieldsMetadata.cost_per_all_conversion.name,
                                             ColumnType.text)

    cost_per_conversion = ColumnMetadata(GoogleMetricFieldsMetadata.cost_per_conversion.name, ColumnType.text)

    cost_per_current_model_attributed_conversion = ColumnMetadata(
        GoogleMetricFieldsMetadata.cost_per_current_model_attributed_conversion.name, ColumnType.text)

    cross_device_conversions = ColumnMetadata(GoogleMetricFieldsMetadata.cross_device_conversions.name,
                                              ColumnType.text)

    ctr = ColumnMetadata(GoogleMetricFieldsMetadata.ctr.name, ColumnType.text)

    current_model_attributed_conversions = ColumnMetadata(
        GoogleMetricFieldsMetadata.current_model_attributed_conversions.name, ColumnType.text)

    current_model_attributed_conversion_value = ColumnMetadata(
        GoogleMetricFieldsMetadata.current_model_attributed_conversion_value.name, ColumnType.text)

    engagement_rate = ColumnMetadata(GoogleMetricFieldsMetadata.engagement_rate.name, ColumnType.text)

    engagements = ColumnMetadata(GoogleMetricFieldsMetadata.engagements.name, ColumnType.text)

    gmail_forwards = ColumnMetadata(GoogleMetricFieldsMetadata.gmail_forwards.name, ColumnType.text)

    gmail_saves = ColumnMetadata(GoogleMetricFieldsMetadata.gmail_saves.name, ColumnType.text)

    gmail_secondary_clicks = ColumnMetadata(GoogleMetricFieldsMetadata.gmail_secondary_clicks.name,
                                            ColumnType.text)

    impression_assisted_conversions = ColumnMetadata(
        GoogleMetricFieldsMetadata.impression_assisted_conversions.name,
        ColumnType.text)

    impression_assisted_conversions_over_last_click_conversions = ColumnMetadata(
        GoogleMetricFieldsMetadata.impression_assisted_conversions_over_last_click_conversions.name,
        ColumnType.text)

    impression_assisted_conversion_value = ColumnMetadata(
        GoogleMetricFieldsMetadata.impression_assisted_conversion_value.name, ColumnType.text)

    impressions = ColumnMetadata(GoogleMetricFieldsMetadata.impressions.name, ColumnType.text)

    interaction_rate = ColumnMetadata(GoogleMetricFieldsMetadata.interaction_rate.name, ColumnType.text)

    interactions = ColumnMetadata(GoogleMetricFieldsMetadata.interactions.name, ColumnType.text)

    interaction_types = ColumnMetadata(GoogleMetricFieldsMetadata.interaction_types.name, ColumnType.text)

    percent_new_visitors = ColumnMetadata(GoogleMetricFieldsMetadata.percent_new_visitors.name, ColumnType.text)

    top_impression_percentage = ColumnMetadata(GoogleMetricFieldsMetadata.top_impression_percentage.name,
                                               ColumnType.text)

    value_per_all_conversion = ColumnMetadata(GoogleMetricFieldsMetadata.value_per_all_conversion.name,
                                              ColumnType.text)

    value_per_conversion = ColumnMetadata(GoogleMetricFieldsMetadata.value_per_conversion.name, ColumnType.text)

    value_per_current_model_attributed_conversion = ColumnMetadata(
        GoogleMetricFieldsMetadata.value_per_current_model_attributed_conversion.name,
        ColumnType.text)

    video_quartile_100_rate = ColumnMetadata(GoogleMetricFieldsMetadata.video_quartile_100_rate.name,
                                             ColumnType.text)

    video_quartile_25_rate = ColumnMetadata(GoogleMetricFieldsMetadata.video_quartile_25_rate.name,
                                            ColumnType.text)

    video_quartile_50_rate = ColumnMetadata(GoogleMetricFieldsMetadata.video_quartile_50_rate.name,
                                            ColumnType.text)

    video_quartile_75_rate = ColumnMetadata(GoogleMetricFieldsMetadata.video_quartile_75_rate.name,
                                            ColumnType.text)

    video_view_rate = ColumnMetadata(GoogleMetricFieldsMetadata.video_view_rate.name, ColumnType.text)

    video_views = ColumnMetadata(GoogleMetricFieldsMetadata.video_views.name, ColumnType.text)

    view_through_conversions = ColumnMetadata(GoogleMetricFieldsMetadata.view_through_conversions.name,
                                              ColumnType.text)

    content_impression_share = ColumnMetadata(GoogleMetricFieldsMetadata.content_impression_share.name,
                                              ColumnType.text)

    content_rank_lost_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.content_rank_lost_impression_share.name, ColumnType.text)

    num_offline_impressions = ColumnMetadata(GoogleMetricFieldsMetadata.num_offline_impressions.name,
                                             ColumnType.text)

    num_offline_interactions = ColumnMetadata(GoogleMetricFieldsMetadata.num_offline_interactions.name,
                                              ColumnType.text)

    offline_interaction_rate = ColumnMetadata(GoogleMetricFieldsMetadata.offline_interaction_rate.name,
                                              ColumnType.text)

    relative_ctr = ColumnMetadata(GoogleMetricFieldsMetadata.relative_ctr.name, ColumnType.text)

    search_absolute_top_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_absolute_top_impression_share.name, ColumnType.text)

    search_budget_lost_absolute_top_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_budget_lost_absolute_top_impression_share.name,
        ColumnType.text)

    search_budget_lost_top_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_budget_lost_top_impression_share.name, ColumnType.text)

    search_exact_match_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_exact_match_impression_share.name, ColumnType.text)

    search_impression_share = ColumnMetadata(GoogleMetricFieldsMetadata.search_impression_share.name,
                                             ColumnType.text)

    search_rank_lost_absolute_top_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_rank_lost_absolute_top_impression_share.name,
        ColumnType.text)

    search_rank_lost_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_rank_lost_impression_share.name, ColumnType.text)

    search_rank_lost_top_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_rank_lost_top_impression_share.name, ColumnType.text)

    search_top_impression_share = ColumnMetadata(GoogleMetricFieldsMetadata.search_top_impression_share.name,
                                                 ColumnType.text)

    average_frequency = ColumnMetadata(GoogleMetricFieldsMetadata.average_frequency.name, ColumnType.text)

    content_budget_lost_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.content_budget_lost_impression_share.name, ColumnType.text)

    impression_reach = ColumnMetadata(GoogleMetricFieldsMetadata.impression_reach.name, ColumnType.text)

    invalid_click_rate = ColumnMetadata(GoogleMetricFieldsMetadata.invalid_click_rate.name, ColumnType.text)

    invalid_clicks = ColumnMetadata(GoogleMetricFieldsMetadata.invalid_clicks.name, ColumnType.text)

    search_budget_lost_impression_share = ColumnMetadata(
        GoogleMetricFieldsMetadata.search_budget_lost_impression_share.name, ColumnType.text)

    search_click_share = ColumnMetadata(GoogleMetricFieldsMetadata.search_click_share.name, ColumnType.text)

    historical_creative_quality_score = ColumnMetadata(
        GoogleMetricFieldsMetadata.historical_creative_quality_score.name, ColumnType.text)

    historical_landing_page_quality_score = ColumnMetadata(
        GoogleMetricFieldsMetadata.historical_landing_page_quality_score.name, ColumnType.text)

    historical_quality_score = ColumnMetadata(GoogleMetricFieldsMetadata.historical_quality_score.name,
                                              ColumnType.text)

    historical_search_predicted_ctr = ColumnMetadata(
        GoogleMetricFieldsMetadata.historical_search_predicted_ctr.name,
        ColumnType.text)
