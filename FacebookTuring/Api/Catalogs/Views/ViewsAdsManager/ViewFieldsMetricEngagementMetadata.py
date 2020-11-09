from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnCategoryEnum import ViewColumnCategoryEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewFieldsMetricEngagementMetadata:
    page_engagement = ViewColumn(
        Autoincrement.hex_string("page_engagement"),
        display_name="Page engagement",
        primary_value=FieldsMetadata.page_engagement,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    page_likes = ViewColumn(
        Autoincrement.hex_string("page_likes"),
        display_name="Page likes",
        primary_value=FieldsMetadata.page_likes,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    post_comments = ViewColumn(
        Autoincrement.hex_string("post_comments"),
        display_name="Post comments",
        primary_value=FieldsMetadata.post_comments,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    post_engagement = ViewColumn(
        Autoincrement.hex_string("post_engagement"),
        display_name="Post engagement",
        primary_value=FieldsMetadata.post_engagement,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    post_reactions = ViewColumn(
        Autoincrement.hex_string("post_reactions"),
        display_name="Post reactions",
        primary_value=FieldsMetadata.post_reactions,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    post_saves = ViewColumn(
        Autoincrement.hex_string("post_saves"),
        display_name="Post saves",
        primary_value=FieldsMetadata.post_saves,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    post_shares = ViewColumn(
        Autoincrement.hex_string("post_shares"),
        display_name="Post shares",
        primary_value=FieldsMetadata.post_shares,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    photo_views = ViewColumn(
        Autoincrement.hex_string("photo_views"),
        display_name="Photo views",
        primary_value=FieldsMetadata.photo_views,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    event_responses = ViewColumn(
        Autoincrement.hex_string("event_responses"),
        display_name="Event responses",
        primary_value=FieldsMetadata.event_responses,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    checkins = ViewColumn(
        Autoincrement.hex_string("checkins"),
        display_name="Check-ins",
        primary_value=FieldsMetadata.checkins,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    inview_impressions_100p = ViewColumn(
        Autoincrement.hex_string("inview_impressions_100p"),
        display_name="In-view impressions 100%",
        primary_value=FieldsMetadata.inview_impressions_100p,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    inview_reach_100p = ViewColumn(
        Autoincrement.hex_string("inview_reach_100p"),
        display_name="In-view reach 100%",
        primary_value=FieldsMetadata.inview_reach_100p,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_page_engagement = ViewColumn(
        Autoincrement.hex_string("cost_per_page_engagement"),
        display_name="Cost per page engagement",
        primary_value=FieldsMetadata.cost_per_page_engagement,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_page_like = ViewColumn(
        Autoincrement.hex_string("cost_per_page_like"),
        display_name="Cost per page like",
        primary_value=FieldsMetadata.cost_per_page_like,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_post_engagement = ViewColumn(
        Autoincrement.hex_string("cost_per_post_engagement"),
        display_name="Cost per post engagement",
        primary_value=FieldsMetadata.cost_per_post_engagement,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_event_response = ViewColumn(
        Autoincrement.hex_string("cost_per_event_response"),
        display_name="Cost per event response",
        primary_value=FieldsMetadata.cost_per_event_response,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    new_messaging_connections = ViewColumn(
        Autoincrement.hex_string("new_messaging_connections"),
        display_name="New messaging connections",
        primary_value=FieldsMetadata.new_messaging_connections,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    blocked_messaging_connections = ViewColumn(
        Autoincrement.hex_string("blocked_messaging_connections"),
        display_name="Blocked messaging connections",
        primary_value=FieldsMetadata.blocked_messaging_connections,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_new_messaging_connection = ViewColumn(
        Autoincrement.hex_string("cost_per_new_messaging_connection"),
        display_name="Cost per new messaging connections",
        primary_value=FieldsMetadata.cost_per_new_messaging_connection,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    continuous_video_plays_2s_unique = ViewColumn(
        Autoincrement.hex_string("continuous_video_plays_2s_unique"),
        display_name="Unique continuous 2s video plays",
        primary_value=FieldsMetadata.continuous_video_plays_2s_unique,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    continuous_video_plays_2s = ViewColumn(
        Autoincrement.hex_string("continuous_video_plays_2s"),
        display_name="Continuous 2s video plays",
        primary_value=FieldsMetadata.continuous_video_plays_2s,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    video_plays_3s = ViewColumn(
        Autoincrement.hex_string("video_plays_3s"),
        display_name="3s video plays",
        primary_value=FieldsMetadata.video_plays_3s,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    thru_plays = ViewColumn(
        Autoincrement.hex_string("thru_plays"),
        display_name="Thru plays",
        primary_value=FieldsMetadata.thru_plays,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    video_plays_25p = ViewColumn(
        Autoincrement.hex_string("video_plays_25p"),
        display_name="Video plays 25% watched actions",
        primary_value=FieldsMetadata.video_plays_25p,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    video_plays_50p = ViewColumn(
        Autoincrement.hex_string("video_plays_50p"),
        display_name="Video plays 50% watched actions",
        primary_value=FieldsMetadata.video_plays_50p,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    video_plays_75p = ViewColumn(
        Autoincrement.hex_string("video_plays_75p"),
        display_name="Video plays 75% watched actions",
        primary_value=FieldsMetadata.video_plays_75p,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    video_plays_95p = ViewColumn(
        Autoincrement.hex_string("video_plays_95p"),
        display_name="Video plays 95% watched actions",
        primary_value=FieldsMetadata.video_plays_95p,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    video_plays_100p = ViewColumn(
        Autoincrement.hex_string("video_plays_100p"),
        display_name="Video plays 100% watched actions",
        primary_value=FieldsMetadata.video_plays_100p,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    video_average_play_time = ViewColumn(
        Autoincrement.hex_string("video_average_play_time"),
        display_name="Video play average time",
        primary_value=FieldsMetadata.video_average_play_time,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    video_plays = ViewColumn(
        Autoincrement.hex_string("video_plays"),
        display_name="Video plays",
        primary_value=FieldsMetadata.video_plays,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    instant_experience_view_time = ViewColumn(
        Autoincrement.hex_string("instant_experience_view_time"),
        display_name="Instant experience view time",
        primary_value=FieldsMetadata.instant_experience_view_time,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    instant_experience_view_percentage = ViewColumn(
        Autoincrement.hex_string("instant_experience_view_percentage"),
        display_name="Instant experience view percentage",
        primary_value=FieldsMetadata.instant_experience_view_percentage,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_continuous_video_play_2s = ViewColumn(
        Autoincrement.hex_string("cost_per_continuous_video_play_2s"),
        display_name="Cost per continuous 2s video play",
        primary_value=FieldsMetadata.cost_per_continuous_video_play_2s,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_thru_play = ViewColumn(
        Autoincrement.hex_string("cost_per_thru_play"),
        display_name="Cost per thru play",
        primary_value=FieldsMetadata.cost_per_thru_play,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    link_clicks = ViewColumn(
        Autoincrement.hex_string("link_clicks"),
        display_name="Link clicks",
        primary_value=FieldsMetadata.link_clicks,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    unique_link_clicks = ViewColumn(
        Autoincrement.hex_string("unique_link_clicks"),
        display_name="Unique link clicks",
        primary_value=FieldsMetadata.unique_link_clicks,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    outbound_clicks = ViewColumn(
        Autoincrement.hex_string("outbound_clicks"),
        display_name="Outbound clicks",
        primary_value=FieldsMetadata.outbound_clicks,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    unique_outbound_clicks = ViewColumn(
        Autoincrement.hex_string("unique_outbound_clicks"),
        display_name="Outbound unique clicks",
        primary_value=FieldsMetadata.unique_outbound_clicks,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    link_click_through_rate = ViewColumn(
        Autoincrement.hex_string("link_click_through_rate"),
        display_name="Link click-through rate",
        primary_value=FieldsMetadata.link_click_through_rate,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
        no_of_decimals=2,
    )
    unique_link_click_through_rate = ViewColumn(
        Autoincrement.hex_string("unique_link_click_through_rate"),
        display_name="Unique link click-through rate",
        primary_value=FieldsMetadata.unique_link_click_through_rate,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
        no_of_decimals=2,
    )
    outbound_link_click_through_rate = ViewColumn(
        Autoincrement.hex_string("outbound_link_click_through_rate"),
        display_name="Outbound link click-through rate",
        primary_value=FieldsMetadata.outbound_link_click_through_rate,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    unique_outbound_linK_click_through_rate = ViewColumn(
        Autoincrement.hex_string("unique_outbound_linK_click_through_rate"),
        display_name="Unique Outbound link click-through rate",
        primary_value=FieldsMetadata.unique_outbound_linK_click_through_rate,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    unique_clicks_all = ViewColumn(
        Autoincrement.hex_string("unique_clicks_all"),
        display_name="Unique clicks (All)",
        primary_value=FieldsMetadata.unique_clicks_all,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    unique_ctr_all = ViewColumn(
        Autoincrement.hex_string("unique_ctr_all"),
        display_name="Unique CTR (All)",
        primary_value=FieldsMetadata.unique_ctr_all,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
        no_of_decimals=2,
    )
    instant_experience_clicks_to_open = ViewColumn(
        Autoincrement.hex_string("instant_experience_clicks_to_open"),
        display_name="Instant experience clicks to open",
        primary_value=FieldsMetadata.instant_experience_clicks_to_open,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    instant_experience_clicks_to_start = ViewColumn(
        Autoincrement.hex_string("instant_experience_clicks_to_start"),
        display_name="Instant experience clicks to start",
        primary_value=FieldsMetadata.instant_experience_clicks_to_start,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    instant_experience_outbound_clicks = ViewColumn(
        Autoincrement.hex_string("instant_experience_outbound_clicks"),
        display_name="Instant experience outbound clicks",
        primary_value=FieldsMetadata.instant_experience_outbound_clicks,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_link_click = ViewColumn(
        Autoincrement.hex_string("cost_per_link_click"),
        display_name="Cost per link click",
        primary_value=FieldsMetadata.cost_per_link_click,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    cost_per_unique_link_click = ViewColumn(
        Autoincrement.hex_string("cost_per_unique_link_click"),
        display_name="Cost per unique link click",
        primary_value=FieldsMetadata.cost_per_unique_link_click,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    cost_per_outbound_click = ViewColumn(
        Autoincrement.hex_string("cost_per_outbound_click"),
        display_name="Cost per outbound click",
        primary_value=FieldsMetadata.cost_per_outbound_click,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_unique_outbound_click = ViewColumn(
        Autoincrement.hex_string("cost_per_unique_outbound_click"),
        display_name="Cost per unique outbound click",
        primary_value=FieldsMetadata.cost_per_unique_outbound_click,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_unique_click_all = ViewColumn(
        Autoincrement.hex_string("cost_per_unique_click_all"),
        display_name="Cost per unique click (All)",
        primary_value=FieldsMetadata.cost_per_unique_click_all,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
        is_filterable=True,
        is_sortable=True,
    )
    estimated_ad_recall_lift = ViewColumn(
        Autoincrement.hex_string("estimated_ad_recall_lift"),
        display_name="Estimated ad recallers",
        primary_value=FieldsMetadata.estimated_ad_recall_lift,
        type_id=ViewColumnTypeEnum.NUMBER.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    estimated_ad_recall_lift_rate = ViewColumn(
        Autoincrement.hex_string("estimated_ad_recall_lift_rate"),
        display_name="Estimated ad recall rate",
        primary_value=FieldsMetadata.estimated_ad_recall_lift_rate,
        type_id=ViewColumnTypeEnum.PERCENTAGE.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    cost_per_estimated_ad_recall_lift = ViewColumn(
        Autoincrement.hex_string("cost_per_estimated_ad_recall_lift"),
        display_name="Cost per estimated ad recall",
        primary_value=FieldsMetadata.cost_per_estimated_ad_recall_lift,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
    social_spend = ViewColumn(
        Autoincrement.hex_string("social_spend"),
        display_name="Social spend",
        primary_value=FieldsMetadata.social_spend,
        type_id=ViewColumnTypeEnum.CURRENCY.value,
        category_id=ViewColumnCategoryEnum.ENGAGEMENT.value,
        is_fixed=False,
    )
