from Core.Metadata.Columns.ViewColumns.ViewColumnCategory import ViewColumnCategory
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType
from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.GoogleAdsAPI.Models.GoogleFieldsMetadata import GoogleFieldsMetadata
from GoogleTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn


class ViewFieldsMetricPerformanceMetadata:
    clicks = ViewColumn(
        Autoincrement.hex_string("clicks"),
        display_name="Clicks",
        primary_value=GoogleFieldsMetadata.clicks,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    cost = ViewColumn(
        Autoincrement.hex_string("cost"),
        display_name="Cost",
        primary_value=GoogleFieldsMetadata.cost,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    impressions = ViewColumn(
        Autoincrement.hex_string("Impressions"),
        display_name="impressions",
        primary_value=GoogleFieldsMetadata.impressions,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    ctr = ViewColumn(
        Autoincrement.hex_string("ctr"),
        display_name="CTR",
        primary_value=GoogleFieldsMetadata.ctr,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    interactions = ViewColumn(
        Autoincrement.hex_string("interactions"),
        display_name="Interactions",
        primary_value=GoogleFieldsMetadata.interactions,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    interaction_rate = ViewColumn(
        Autoincrement.hex_string("interaction_rate"),
        display_name="Interaction Rate",
        primary_value=GoogleFieldsMetadata.interaction_rate,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    engagements = ViewColumn(
        Autoincrement.hex_string("engagements"),
        display_name="Engagements",
        primary_value=GoogleFieldsMetadata.engagements,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    engagement_rate = ViewColumn(
        Autoincrement.hex_string("Engagement_rate"),
        display_name="Engagement Rate",
        primary_value=GoogleFieldsMetadata.engagement_rate,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    invalid_clicks = ViewColumn(
        Autoincrement.hex_string("invalid_clicks"),
        display_name="Invalid Clicks",
        primary_value=GoogleFieldsMetadata.invalid_clicks,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    invalid_click_rate = ViewColumn(
        Autoincrement.hex_string("invalid_click_rate"),
        display_name="Invalid Click Rate",
        primary_value=GoogleFieldsMetadata.invalid_click_rate,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    average_cpc = ViewColumn(
        Autoincrement.hex_string("average_cpc"),
        display_name="Average CPC",
        primary_value=GoogleFieldsMetadata.average_cpc,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    average_cost = ViewColumn(
        Autoincrement.hex_string("average_cost"),
        display_name="Average Cost",
        primary_value=GoogleFieldsMetadata.average_cost,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    average_cpe = ViewColumn(
        Autoincrement.hex_string("average_cpe"),
        display_name="Average CPE",
        primary_value=GoogleFieldsMetadata.average_cpe,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    average_cpm = ViewColumn(
        Autoincrement.hex_string("average_cpm"),
        display_name="Average CPM",
        primary_value=GoogleFieldsMetadata.average_cpm,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    average_target_cpa = ViewColumn(
        Autoincrement.hex_string("average_target_cpa"),
        display_name="Average Target CPA",
        primary_value=GoogleFieldsMetadata.average_target_cpa,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
    )

    average_cpv = ViewColumn(
        Autoincrement.hex_string("average_cpv"),
        display_name="Average CPV",
        primary_value=GoogleFieldsMetadata.average_cpv,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
    )

    average_target_roas = ViewColumn(
        Autoincrement.hex_string("average_target_roas"),
        display_name="Average Target ROAS",
        primary_value=GoogleFieldsMetadata.average_target_roas,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
    )

    views = ViewColumn(
        Autoincrement.hex_string("views"),
        display_name="Views",
        primary_value=GoogleFieldsMetadata.views,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    view_rate = ViewColumn(
        Autoincrement.hex_string("view_rate"),
        display_name="View Rate",
        primary_value=GoogleFieldsMetadata.view_rate,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    watch_time = ViewColumn(
        Autoincrement.hex_string("watch_time"),
        display_name="Watch Time",
        primary_value=GoogleFieldsMetadata.watch_time,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    average_watch_time = ViewColumn(
        Autoincrement.hex_string("average_watch_time"),
        display_name="Average Watch Time",
        primary_value=GoogleFieldsMetadata.average_watch_time,
        type_id=ViewColumnType.NUMBER.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    video_p_25 = ViewColumn(
        Autoincrement.hex_string("video_p_25"),
        display_name="video_p_25",
        primary_value=GoogleFieldsMetadata.video_p_25,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        group_display_name="Video played to",
        is_filterable=True,
        is_sortable=True,
    )

    video_p_50 = ViewColumn(
        Autoincrement.hex_string("video_p_50"),
        display_name="video_p_50",
        primary_value=GoogleFieldsMetadata.video_p_50,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        group_display_name="Video played to",
        is_filterable=True,
        is_sortable=True,
    )

    video_p_75 = ViewColumn(
        Autoincrement.hex_string("video_p_75"),
        display_name="video_p_75",
        primary_value=GoogleFieldsMetadata.video_p_75,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        group_display_name="Video played to",
        is_filterable=True,
        is_sortable=True,
    )

    video_p_100 = ViewColumn(
        Autoincrement.hex_string("video_p_100"),
        display_name="video_p_100",
        primary_value=GoogleFieldsMetadata.video_p_100,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        group_display_name="Video played to",
        is_filterable=True,
        is_sortable=True,
    )

    absolute_top_impression_percentage = ViewColumn(
        Autoincrement.hex_string("absolute_top_impression_percentage"),
        display_name="Absolute Top Impression Percentage",
        primary_value=GoogleFieldsMetadata.absolute_top_impression_percentage,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )

    top_impression_percentage = ViewColumn(
        Autoincrement.hex_string("top_impression_percentage"),
        display_name="Top Impression Percentage",
        primary_value=GoogleFieldsMetadata.top_impression_percentage,
        type_id=ViewColumnType.PERCENTAGE.value,
        category_id=ViewColumnCategory.PERFORMANCE.value,
        is_filterable=True,
        is_sortable=True,
    )
