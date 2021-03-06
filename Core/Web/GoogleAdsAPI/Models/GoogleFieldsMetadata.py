from Core.Web.GoogleAdsAPI.Models.GoogleField import GoogleField
from Core.Web.GoogleAdsAPI.Models.GoogleFieldType import GoogleFieldType, GoogleResourceType
from Core.Web.GoogleAdsAPI.Models.GoogleMetricsConversionFunctions import (
    enum_to_string,
    float_to_percentage,
    id_to_string,
    money_conversion,
    round_float,
)


class GoogleFieldsMetadata:
    google_account_id = GoogleField(
        name="google_account_id",
        field_name="google_account_id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER,
        conversion_function=id_to_string,
    )

    google_manager_id = GoogleField(
        name="google_manager_id",
        field_name="google_manager_id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER,
        conversion_function=id_to_string,
    )

    customer_id = GoogleField(
        name="id",
        field_name="id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER,
        conversion_function=id_to_string,
    )

    customer_client_id = GoogleField(
        name="id",
        field_name="id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER_CLIENT,
        conversion_function=id_to_string,
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
        name="bidding_strategy_id",
        field_name="id",
        field_type=GoogleFieldType.METRIC,
        resource_type=GoogleResourceType.BIDDING_STRATEGY,
        conversion_function=id_to_string,
    )

    bidding_strategy_name = GoogleField(
        name="bidding_strategy_name",
        field_name="bidding_strategy_name",
        field_type=GoogleFieldType.METRIC,
        resource_type=GoogleResourceType.BIDDING_STRATEGY,
    )

    ad_id = GoogleField(
        name="ad_id",
        field_name="ad_id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.Ad,
        conversion_function=id_to_string,
    )

    ad_name = GoogleField(
        name="ad_name",
        field_name="ad_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.Ad,
    )

    adgroup_id = GoogleField(
        name="adgroup_id",
        field_name="id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.ADGROUP,
        conversion_function=id_to_string,
    )

    adgroup_name = GoogleField(
        name="adgroup_name",
        field_name="name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.ADGROUP,
    )

    campaign_id = GoogleField(
        name="campaign_id",
        field_name="id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
        conversion_function=id_to_string,
    )

    campaign_name = GoogleField(
        name="campaign_name",
        field_name="name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    criterion_id = GoogleField(
        name="keyword_id",
        field_name="criterion_id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
        conversion_function=id_to_string,
    )

    audience_id = GoogleField(
        name="criterion_id",
        field_name="criterion_id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
        conversion_function=id_to_string,
    )

    keyword_match_type = GoogleField(
        name="keyword_match_type",
        field_name="keyword.match_type",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
        conversion_function=enum_to_string,
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

    ad_group_criterion_resource_name = GoogleField(
        name="resource_name",
        field_name="resource_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
    )

    campaign_budget = GoogleField(
        name="campaign_budget",
        field_name="campaign_budget",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
        conversion_function=money_conversion,
    )

    campaign_budget_amount_micros = GoogleField(
        name="campaign_budget_amount_micros",
        field_name="amount_micros",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN_BUDGET,
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
        conversion_function=money_conversion,
    )

    target_impression_share_location = GoogleField(
        name="Location Goal for Target IS",
        field_name="target_impression_share.location",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
        conversion_function=enum_to_string,
    )

    maximize_conversion_value_target_roas = GoogleField(
        name="target_roas",
        field_name="maximize_conversion_value.target_roas",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
        conversion_function=float_to_percentage,
    )

    optimization_score = GoogleField(
        name="optimization_score",
        field_name="optimization_score",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    target_cpa = GoogleField(
        name="target_cpa",
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
        field_name="cost_micros",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
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
        conversion_function=float_to_percentage,
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
        conversion_function=float_to_percentage,
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
        conversion_function=float_to_percentage,
    )

    average_cpc = GoogleField(
        name="average_cpc",
        field_name="average_cpc",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    ctr = GoogleField(
        name="ctr",
        field_name="ctr",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    average_cost = GoogleField(
        name="average_cost",
        field_name="average_cost",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
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
        conversion_function=money_conversion,
    )

    average_cpv = GoogleField(
        name="average_cpv",
        field_name="average_cpv",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    average_target_cpa = GoogleField(
        name="average_target_cpa",
        field_name="maximize_conversions.target_cpa",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
        conversion_function=money_conversion,
    )

    average_target_roas = GoogleField(
        name="average_target_roas",
        field_name="target_roas.target_roas",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
        conversion_function=money_conversion,
    )

    views = GoogleField(
        name="views",
        field_name="video_views",
        field_type=GoogleFieldType.METRIC,
    )

    view_rate = GoogleField(
        name="view_rate",
        field_name="video_view_rate",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
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
        field_name="video_quartile_p25_rate",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    video_p_50 = GoogleField(
        name="video_p_50",
        field_name="video_quartile_p50_rate",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    video_p_75 = GoogleField(
        name="video_p_75",
        field_name="video_quartile_p75_rate",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    video_p_100 = GoogleField(
        name="video_p_100",
        field_name="video_quartile_p100_rate",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    absolute_top_impression_percentage = GoogleField(
        name="absolute_top_impression_percentage",
        field_name="absolute_top_impression_percentage",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    top_impression_percentage = GoogleField(
        name="top_impression_percentage",
        field_name="top_impression_percentage",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    date = GoogleField(
        name="date",
        field_name="date",
        field_type=GoogleFieldType.SEGMENT,
    )

    device = GoogleField(
        name="device",
        field_name="device",
        field_type=GoogleFieldType.SEGMENT,
    )

    level = GoogleField(
        name="Level",
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
        name="viewable_impressions",
        field_name="active_view_impressions",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    measurable_impressions = GoogleField(
        name="measurable_impressions",
        field_name="active_view_measurable_impressions",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    measurable_cost = GoogleField(
        name="measurable_cost ",
        field_name="active_view_measurable_cost_micros",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    measurable_rate = GoogleField(
        name="measurable_rate ",
        field_name="active_view_measurability",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    average_viewable_cpm = GoogleField(
        name="average_viewable_cpm",
        field_name="active_view_cpm",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    viewable_ctr = GoogleField(
        name="viewable_ctr",
        field_name="active_view_ctr",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    viewable_rate = GoogleField(
        name="viewable_rate ",
        field_name="active_view_viewability",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    conversions = GoogleField(
        name="conversions",
        field_name="conversions",
        field_type=GoogleFieldType.METRIC,
    )

    cost_per_conversion = GoogleField(
        name="cost_per_conversion",
        field_name="cost_per_conversion",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    conversion_rate = GoogleField(
        name="conversion_rate",
        field_name="conversion_rate",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
    )

    conversions_value = GoogleField(
        name="conversion_value",
        field_name="conversions_value",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    conversions_value_per_cost = GoogleField(
        name="conversion_value_per_cost",
        field_name="conversions_value_per_cost",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    value_per_conversion = GoogleField(
        name="value_per_conversion",
        field_name="value_per_conversion ",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    conversions_by_conversion_date = GoogleField(
        name="conversions_by_conv_time",
        field_name="conversions_by_conversion_date",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    conversions_value_by_conversion_date = GoogleField(
        name="Conv. value (by conv. time)",
        field_name="conversions_value_by_conversion_date",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    value_per_conversions_by_conversion_date = GoogleField(
        name="Value / conv. (by conv. time)",
        field_name="value_per_conversions_by_conversion_date",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    all_conversions = GoogleField(
        name="All conversions",
        field_name="all_conversions",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    cost_per_all_conversions = GoogleField(
        name="Cost per all conversions",
        field_name="cost_per_all_conversions",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    all_conversions_from_interactions_rate = GoogleField(
        name="All conversion rate ",
        field_name="all_conversions_from_interactions_rate",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    all_conversions_value = GoogleField(
        name="All conversion value",
        field_name="all_conversions_value",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    all_conversions_value_per_cost = GoogleField(
        name="All conversion value per cost",
        field_name="all_conversions_value_per_cost",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    value_per_all_conversions = GoogleField(
        name="Value per all conversions",
        field_name="value_per_all_conversions",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    all_conversions_by_conversion_date = GoogleField(
        name="All conv. (by conv. time)",
        field_name="all_conversions_by_conversion_date",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    value_per_all_conversions_by_conversion_date = GoogleField(
        name="Value / all conv. (by conv. time) ",
        field_name="value_per_all_conversions_by_conversion_date",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    cross_device_conversions = GoogleField(
        name="Cross-device conversions",
        field_name="cross_device_conversions",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    view_through_conversions = GoogleField(
        name="View-through conversions",
        field_name="view_through_conversions",
        field_type=GoogleFieldType.METRIC,
        conversion_function=money_conversion,
    )

    search_impression_share = GoogleField(
        name="Search Impression Share",
        field_name="search_impression_share",
        field_type=GoogleFieldType.METRIC,
        conversion_function=round_float,
    )

    search_top_impression_share = GoogleField(
        name="Search top impression share (IS)",
        field_name="search_top_impression_share",
        field_type=GoogleFieldType.METRIC,
        conversion_function=round_float,
    )

    search_absolute_top_impression_share = GoogleField(
        name="Search absolute top impression share",
        field_name="search_absolute_top_impression_share",
        field_type=GoogleFieldType.METRIC,
        conversion_function=round_float,
    )

    search_rank_lost_impression_share = GoogleField(
        name="Search lost impression share (rank)",
        field_name="search_rank_lost_impression_share",
        field_type=GoogleFieldType.METRIC,
        conversion_function=round_float,
    )

    search_rank_lost_top_impression_share = GoogleField(
        name="Search lost top impression share (rank)",
        field_name="search_rank_lost_top_impression_share",
        field_type=GoogleFieldType.METRIC,
        conversion_function=round_float,
    )

    search_budget_lost_impression_share = GoogleField(
        name="Search lost impression share (budget)",
        field_name="search_budget_lost_impression_share",
        field_type=GoogleFieldType.METRIC,
        conversion_function=round_float,
    )

    search_exact_match_impression_share = GoogleField(
        name="Search exact match impression share (IS)",
        field_name="search_exact_match_impression_share",
        field_type=GoogleFieldType.METRIC,
        conversion_function=round_float,
    )

    content_impression_share = GoogleField(
        name="Display impression share",
        field_name="content_impression_share",
        field_type=GoogleFieldType.METRIC,
        conversion_function=round_float,
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
        conversion_function=round_float,
    )

    search_click_share = GoogleField(
        name="Click share",
        field_name="search_click_share",
        field_type=GoogleFieldType.METRIC,
        conversion_function=round_float,
    )

    relative_ctr = GoogleField(
        name="Relative CTR ",
        field_name="relative_ctr",
        field_type=GoogleFieldType.METRIC,
        conversion_function=float_to_percentage,
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
        conversion_function=float_to_percentage,
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
        conversion_function=float_to_percentage,
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

    audience_type = GoogleField(
        name="type",
        field_name="type",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
    )

    user_interest = GoogleField(
        name="user_interest",
        field_name="user_interest.user_interest_category",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
    )

    custom_intent = GoogleField(
        name="custom_intent",
        field_name="custom_intent.custom_intent",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
    )

    ad_group_criterion_status = GoogleField(
        name="status",
        field_name="status",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
    )

    user_interest_id = GoogleField(
        name="user_interest_id",
        field_name="user_interest_id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.USER_INTEREST,
    )

    user_interest_name = GoogleField(
        name="name",
        field_name="name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.USER_INTEREST,
    )

    user_interest_resource_name = GoogleField(
        name="resource_name",
        field_name="resource_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.USER_INTEREST,
    )

    user_interest_taxonomy_type = GoogleField(
        name="taxonomy_type",
        field_name="taxonomy_type",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.USER_INTEREST,
    )

    user_interest_parent = GoogleField(
        name="user_interest_parent",
        field_name="user_interest_parent",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.USER_INTEREST,
    )

    custom_interest_id = GoogleField(
        name="id",
        field_name="id",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOM_INTEREST,
    )

    custom_interest_name = GoogleField(
        name="name",
        field_name="name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOM_INTEREST,
    )

    custom_interest_resource_name = GoogleField(
        name="resource_name",
        field_name="resource_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOM_INTEREST,
    )

    custom_interest_status = GoogleField(
        name="status",
        field_name="status",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOM_INTEREST,
    )

    custom_interest_type = GoogleField(
        name="type",
        field_name="type",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOM_INTEREST,
    )

    custom_interest_members = GoogleField(
        name="members",
        field_name="members",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOM_INTEREST,
    )

    custom_interest_description = GoogleField(
        name="description",
        field_name="description",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOM_INTEREST,
    )

    audience = GoogleField(
        name="audience",
        field_name="audience",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
    )

    audience_category = GoogleField(
        name="audience_category",
        field_name="audience_category",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.AD_GROUP_CRITERION,
    )

    campaign_status = GoogleField(
        name="campaign_status",
        field_name="status",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CAMPAIGN,
    )

    adgroup_status = GoogleField(
        name="adgroup_status",
        field_name="status",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.ADGROUP,
    )
