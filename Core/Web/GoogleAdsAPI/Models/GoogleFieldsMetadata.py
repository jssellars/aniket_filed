from Core.Web.GoogleAdsAPI.Models.GoogleField import GoogleField
from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleFieldType, GoogleResourceType


class GoogleFieldsMetadata:
    id = GoogleField(
        name="id",
        field_name="id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER,
    )

    customer_client_id = GoogleField(
        name="id",
        field_name="id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER_CLIENT,
    )

    descriptive_name = GoogleField(
        name="name",
        field_name="descriptive_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER,
    )

    client_descriptive_name = GoogleField(
        name="name",
        field_name="descriptive_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER_CLIENT,
    )

    name = GoogleField(
        name="name",
        field_name="name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    bidding_strategy_id = GoogleField(
        name="Bidding strategy ID",
        field_name="id",
        field_type=GoogleFieldType.METRIC,
        resource_type=GoogleResourceType.BIDDING_STRATEGY,
    )

    bidding_strategy_name = GoogleField(
        name="Bidding strategy name",
        field_name="bidding_strategy_id",
        field_type=GoogleFieldType.METRIC,
        resource_type=GoogleResourceType.BIDDING_STRATEGY,
    )

    ad_id = GoogleField(
        name="Ad ID",
        field_name="ad_id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.Ad,
    )

    ad_name = GoogleField(
        name="Ad Name",
        field_name="ad_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.Ad,
    )

    adgroup_id = GoogleField(
        name="Ad Group ID",
        field_name="adgroup_id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.ADGROUP,
    )

    adgroup_name = GoogleField(
        name="Ad Group Name",
        field_name="adgroup_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.ADGROUP,
    )

    campaign_id = GoogleField(
        name="Campaign ID",
        field_name="campaign_id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    campaign_name = GoogleField(
        name="Campaign Name",
        field_name="campaign_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    criterion_id = GoogleField(
        name="criterion_id",
        field_name="criterion_id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
    )

    keyword_match_type = GoogleField(
        name="keyword_match_type",
        field_name="keyword.match_type",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
    )

    keyword_text = GoogleField(
        name="keyword_text",
        field_name="keyword.text",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
    )

    resource_name = GoogleField(
        name="resource_name",
        field_name="resource_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.KEYWORD_VIEW,
    )

    currency_code = GoogleField(
        name="currency",
        field_name="currency_code",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER,
    )

    cpc_bid_ceiling_micros = GoogleField(
        name="Max CPC Bid limit for target IS ",
        field_name="target_impression_share.cpc_bid_ceiling_micros",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    target_impression_share_location = GoogleField(
        name="Location Goal for Target IS",
        field_name="target_impression_share.location",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    maximize_conversion_value_target_roas = GoogleField(
        name="Target ROAS",
        field_name="maximize_conversion_value.target_roas",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    optimization_score = GoogleField(
        name="Optimization score",
        field_name="optimization_score",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    target_cpa = GoogleField(
        name="Target CPA",
        field_name="maximize_conversions.target_cpa",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    clicks = GoogleField(
        name="clicks",
        field_name="clicks",
        field_type=GoogleFieldType.METRIC,
    )

    cost = GoogleField(
        name="cost",
        field_name="cost",
        field_type=GoogleFieldType.METRIC,
    )

    impressions = GoogleField(
        name="impressions",
        field_name="impressions",
        field_type=GoogleFieldType.METRIC,
    )

    interactions = GoogleField(
        name="interactions",
        field_name="interactions",
        field_type=GoogleFieldType.METRIC,
    )

    interaction_rate = GoogleField(
        name="interaction_rate",
        field_name="interaction_rate",
        field_type=GoogleFieldType.METRIC,
    )

    engagements = GoogleField(
        name="engagements",
        field_name="engagements",
        field_type=GoogleFieldType.METRIC,
    )

    engagement_rate = GoogleField(
        name="engagement_rate",
        field_name="engagement_rate",
        field_type=GoogleFieldType.METRIC,
    )

    invalid_clicks = GoogleField(
        name="invalid_clicks",
        field_name="invalid_clicks",
        field_type=GoogleFieldType.METRIC,
    )

    invalid_click_rate = GoogleField(
        name="invalid_click_rate",
        field_name="invalid_click_rate",
        field_type=GoogleFieldType.METRIC,
    )

    average_cpc = GoogleField(
        name="average_cpc",
        field_name="average_cpc",
        field_type=GoogleFieldType.METRIC,
    )

    ctr = GoogleField(
        name="ctr",
        field_name="ctr",
        field_type=GoogleFieldType.METRIC,
    )

    average_cost = GoogleField(
        name="average_cost",
        field_name="average_cost",
        field_type=GoogleFieldType.METRIC,
    )

    average_cpe = GoogleField(
        name="average_cpe",
        field_name="average_cpe",
        field_type=GoogleFieldType.METRIC,
    )

    average_cpm = GoogleField(
        name="average_cpm",
        field_name="average_cpm",
        field_type=GoogleFieldType.METRIC,
    )

    average_cpv = GoogleField(
        name="average_cpv",
        field_name="average_cpv",
        field_type=GoogleFieldType.METRIC,
    )

    average_target_cpa = GoogleField(
        name="average_target_cpa",
        field_name="maximize_conversions.target_cpa",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    average_target_roas = GoogleField(
        name="average_target_roas",
        field_name="target_roas.target_roas",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    views = GoogleField(
        name="views",
        field_name="views",
        field_type=GoogleFieldType.METRIC,
    )

    view_rate = GoogleField(
        name="view_rate",
        field_name="view_rate",
        field_type=GoogleFieldType.METRIC,
    )

    watch_time = GoogleField(
        name="watch_time",
        field_name="watch_time",
        field_type=GoogleFieldType.METRIC,
    )

    average_watch_time = GoogleField(
        name="average_watch_time",
        field_name="average_watch_time",
        field_type=GoogleFieldType.METRIC,
    )

    video_p_25 = GoogleField(
        name="video_p_25",
        field_name="video_p_25",
        field_type=GoogleFieldType.METRIC,
    )

    video_p_50 = GoogleField(
        name="video_p_50",
        field_name="video_p_50",
        field_type=GoogleFieldType.METRIC,
    )

    video_p_75 = GoogleField(
        name="video_p_75",
        field_name="video_p_75",
        field_type=GoogleFieldType.METRIC,
    )

    video_p_100 = GoogleField(
        name="video_p_100",
        field_name="video_p_100",
        field_type=GoogleFieldType.METRIC,
    )

    absolute_top_impression_percentage = GoogleField(
        name="absolute_top_impression_percentage",
        field_name="absolute_top_impression_percentage",
        field_type=GoogleFieldType.METRIC,
    )

    top_impression_percentage = GoogleField(
        name="top_impression_percentage",
        field_name="top_impression_percentage",
        field_type=GoogleFieldType.METRIC,
    )

    date = GoogleField(
        name="date",
        field_name="date",
        field_type=GoogleFieldType.SEGMENT,
    )

    level = GoogleField(
        name="level",
        field_name="level",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER_CLIENT,
    )

    manager = GoogleField(
        name="manager",
        field_name="manager",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER_CLIENT,
    )

    client_customer = GoogleField(
        name="client_customer",
        field_name="client_customer",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER_CLIENT,
    )

    time_zone = GoogleField(
        name="time_zone",
        field_name="time_zone",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER_CLIENT,
    )

    viewable_impressions = GoogleField(
        name="viewable impressions",
        field_name="active_view_impressions",
        field_type=GoogleFieldType.METRIC,
    )

    measurable_impressions = GoogleField(
        name="Measurable impressions",
        field_name="active_view_measurable_impressions",
        field_type=GoogleFieldType.METRIC,
    )

    measurable_cost = GoogleField(
        name="Measurable cost ",
        field_name="active_view_measurable_cost_micros",
        field_type=GoogleFieldType.METRIC,
    )

    Mmesurable_rate = GoogleField(
        name="Measurable rate ",
        field_name="active_view_measurability",
        field_type=GoogleFieldType.METRIC,
    )

    average_viewable_cpm = GoogleField(
        name="Average viewable CPM",
        field_name="active_view_cpm",
        field_type=GoogleFieldType.METRIC,
    )

    viewable_ctr = GoogleField(
        name="Viewable CTR",
        field_name="active_view_ctr",
        field_type=GoogleFieldType.METRIC,
    )

    viewable_rate = GoogleField(
        name="Viewable Rate ",
        field_name="active_view_viewability",
        field_type=GoogleFieldType.METRIC,
    )

    conversions = GoogleField(
        name="conversions",
        field_name="conversions",
        field_type=GoogleFieldType.METRIC,
    )

    cost_per_conversion = GoogleField(
        name="Cost Per Conversion",
        field_name="cost_per_conversion",
        field_type=GoogleFieldType.METRIC,
    )

    conversion_rate = GoogleField(
        name="Conversion Rate",
        field_name="conversion_rate",
        field_type=GoogleFieldType.METRIC,
    )

    conversions_value = GoogleField(
        name="Conversion value",
        field_name="conversions_value",
        field_type=GoogleFieldType.METRIC,
    )

    conversions_value_per_cost = GoogleField(
        name="Conversion value per cost",
        field_name="conversions_value_per_cost",
        field_type=GoogleFieldType.METRIC,
    )

    value_per_conversion = GoogleField(
        name="Value per conversion",
        field_name="value_per_conversion ",
        field_type=GoogleFieldType.METRIC,
    )

    conversions_by_conversion_date = GoogleField(
        name="Conversions (by conv. time)",
        field_name="conversions_by_conversion_date",
        field_type=GoogleFieldType.METRIC,
    )

    conversions_value_by_conversion_date = GoogleField(
        name="Conv. value (by conv. time)",
        field_name="conversions_value_by_conversion_date",
        field_type=GoogleFieldType.METRIC,
    )

    value_per_conversions_by_conversion_date = GoogleField(
        name="Value / conv. (by conv. time)",
        field_name="value_per_conversions_by_conversion_date",
        field_type=GoogleFieldType.METRIC,
    )

    all_conversions = GoogleField(
        name="All conversions",
        field_name="all_conversions",
        field_type=GoogleFieldType.METRIC,
    )

    cost_per_all_conversions = GoogleField(
        name="Cost per all conversions",
        field_name="cost_per_all_conversions",
        field_type=GoogleFieldType.METRIC,
    )

    all_conversions_from_interactions_rate = GoogleField(
        name="All conversion rate ",
        field_name="all_conversions_from_interactions_rate",
        field_type=GoogleFieldType.METRIC,
    )

    all_conversions_value = GoogleField(
        name="All conversion value",
        field_name="all_conversions_value",
        field_type=GoogleFieldType.METRIC,
    )

    all_conversions_value_per_cost = GoogleField(
        name="All conversion value per cost",
        field_name="all_conversions_value_per_cost",
        field_type=GoogleFieldType.METRIC,
    )

    value_per_all_conversions = GoogleField(
        name="Value per all conversions",
        field_name="value_per_all_conversions",
        field_type=GoogleFieldType.METRIC,
    )

    all_conversions_by_conversion_date = GoogleField(
        name="All conv. (by conv. time)",
        field_name="all_conversions_by_conversion_date",
        field_type=GoogleFieldType.METRIC,
    )

    value_per_all_conversions_by_conversion_date = GoogleField(
        name="Value / all conv. (by conv. time) ",
        field_name="value_per_all_conversions_by_conversion_date",
        field_type=GoogleFieldType.METRIC,
    )

    cross_device_conversions = GoogleField(
        name="Cross-device conversions",
        field_name="cross_device_conversions",
        field_type=GoogleFieldType.METRIC,
    )

    view_through_conversions = GoogleField(
        name="View-through conversions",
        field_name="view_through_conversions",
        field_type=GoogleFieldType.METRIC,
    )

    search_impression_share = GoogleField(
        name="Search Impression Share",
        field_name="search_impression_share",
        field_type=GoogleFieldType.METRIC,
    )

    search_top_impression_share = GoogleField(
        name="Search top impression share (IS)",
        field_name="search_top_impression_share",
        field_type=GoogleFieldType.METRIC,
    )

    search_absolute_top_impression_share = GoogleField(
        name="Search absolute top impression share",
        field_name="search_absolute_top_impression_share",
        field_type=GoogleFieldType.METRIC,
    )

    search_rank_lost_impression_share = GoogleField(
        name="Search lost impression share (rank)",
        field_name="search_rank_lost_impression_share",
        field_type=GoogleFieldType.METRIC,
    )

    search_rank_lost_top_impression_share = GoogleField(
        name="Search lost top impression share (rank)",
        field_name="search_rank_lost_top_impression_share",
        field_type=GoogleFieldType.METRIC,
    )

    search_budget_lost_impression_share = GoogleField(
        name="Search lost impression share (budget)",
        field_name="search_budget_lost_impression_share",
        field_type=GoogleFieldType.METRIC,
    )

    search_exact_match_impression_share = GoogleField(
        name="Search exact match impression share (IS)",
        field_name="search_exact_match_impression_share",
        field_type=GoogleFieldType.METRIC,
    )

    content_impression_share = GoogleField(
        name="Display impression share",
        field_name="content_impression_share",
        field_type=GoogleFieldType.METRIC,
    )

    content_rank_lost_impression_share = GoogleField(
        name="Display lost impression share (rank)",
        field_name="content_rank_lost_impression_share",
        field_type=GoogleFieldType.METRIC,
    )

    content_budget_lost_impression_share = GoogleField(
        name="Display Lost impression share (budget)",
        field_name="content_budget_lost_impression_share",
        field_type=GoogleFieldType.METRIC,
    )

    search_click_share = GoogleField(
        name="Click share",
        field_name="search_click_share",
        field_type=GoogleFieldType.METRIC,
    )

    relative_ctr = GoogleField(
        name="Relative CTR ",
        field_name="relative_ctr",
        field_type=GoogleFieldType.METRIC,
    )

    views = GoogleField(
        name="Phone calls",
        field_name="phone_calls",
        field_type=GoogleFieldType.METRIC,
    )

    phone_impressions = GoogleField(
        name="Phone impressions ",
        field_name="phone_impressions",
        field_type=GoogleFieldType.METRIC,
    )

    phone_through_rate = GoogleField(
        name="Phone through rate (PTR)",
        field_name="phone_through_rate",
        field_type=GoogleFieldType.METRIC,
    )

    message_chats = GoogleField(
        name="Message chats",
        field_name="message_chats",
        field_type=GoogleFieldType.METRIC,
    )

    message_impressions = GoogleField(
        name="Message impressions",
        field_name="message_impressions",
        field_type=GoogleFieldType.METRIC,
    )

    message_chat_rate = GoogleField(
        name="Message chat rate",
        field_name="message_chat_rate",
        field_type=GoogleFieldType.METRIC,
    )

    gmail_forwards = GoogleField(
        name="Gmail forwards",
        field_name="gmail_forwards",
        field_type=GoogleFieldType.METRIC,
    )

    gmail_saves = GoogleField(
        name="Gmail saves",
        field_name="gmail_saves",
        field_type=GoogleFieldType.METRIC,
    )

    gmail_secondary_clicks = GoogleField(
        name="Gmail clicks to website ",
        field_name="gmail_secondary_clicks",
        field_type=GoogleFieldType.METRIC,
    )
