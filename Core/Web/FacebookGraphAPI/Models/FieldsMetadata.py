from Core.Web.FacebookGraphAPI.Models.Field import Field
from Core.Web.FacebookGraphAPI.Models.Field import FieldType


ad_creative_field_definition = 'adcreatives{account_id, actor_id, applink_treatment, asset_feed_spec, authorization_category,' \
                               'auto_update, body, branded_content_sponsor_page_id, call_to_action_type, categorization_criteria, bundle_folder_id, category_media_source, destination_set_id,' \
                               'effective_authorization_category, effective_instagram_story_id, dynamic_ad_voice, effective_object_story_id, enable_direct_install, id, image_crops,' \
                               'enable_launch_instant_app, image_hash, image_url, instagram_permalink_url, instagram_story_id, instagram_actor_id, interactive_components_spec, link_deep_link_url,' \
                               'link_url, messenger_sponsored_message, link_og_id, name, object_id, object_story_id, object_story_spec, object_store_url, object_type, object_url,' \
                               'platform_customizations, playable_asset_id, place_page_set_id, portrait_customizations, product_set_id, status, template_url, recommender_settings, thumbnail_url,' \
                               'title, url_tags, use_page_actor_override, video_id, template_url_spec}'


class FieldsMetadata:

    # ====== STRUCTURE ====== #
    name = Field(name="name", field_name="name", fields=["name"], field_type=FieldType.STRUCTURE)

    id = Field(name="id", field_name="id", fields=["id"], field_type=FieldType.STRUCTURE)

    ad_account_id = Field(name="account_id", field_name="account_id", fields=["account_id"], field_type=FieldType.SIMPLE)

    account_name = Field(name="account_name", field_name="account_name", fields=["account_name"], field_type=FieldType.SIMPLE)

    ad_id = Field(name="ad_id", field_name="ad_id", fields=["ad_id"], field_type=FieldType.SIMPLE)

    ad_name = Field(name="ad_name", field_name="ad_name", fields=["ad_name"], field_type=FieldType.SIMPLE)

    adset_id = Field(name="adset_id", field_name="adset_id", fields=["adset_id"], field_type=FieldType.SIMPLE)

    adset_name = Field(name="adset_name", field_name="adset_name", fields=["adset_name"], field_type=FieldType.SIMPLE)

    buying_type = Field(name="buying_type", field_name="buying_type", fields=["buying_type"], field_type=FieldType.STRUCTURE)

    campaign_id = Field(name="campaign_id", field_name="campaign_id", fields=["campaign_id"], field_type=FieldType.SIMPLE)

    campaign_name = Field(name="campaign_name", field_name="campaign_name", fields=["campaign_name"], field_type=FieldType.SIMPLE)

    effective_status = Field(name="effective_status", field_name="effective_status", fields=["effective_status"], field_type=FieldType.STRUCTURE)

    tags = Field(name="tags", field_name="tags", fields=["tags"], field_type=FieldType.STRUCTURE)

    objective = Field(name="objective", field_name="objective", fields=["objective"], field_type=FieldType.SIMPLE)

    created_at = Field(name="created_time", field_name="created_time", fields=["created_time"], field_type=FieldType.STRUCTURE)

    last_significant_edit = Field(name="last_significant_edit", field_name="last_significant_edit", fields=["last_significant_edit"], field_type=FieldType.STRUCTURE)

    start_date = Field(name="start_time", field_name="start_time", fields=["start_time"], field_type=FieldType.STRUCTURE)

    end_date = Field(name="stop_time", field_name="stop_time", fields=["stop_time"], field_type=FieldType.STRUCTURE)

    bid_strategy = Field(name="bid_strategy", field_name="bid_strategy", fields=["bid_strategy"], field_type=FieldType.STRUCTURE)

    amount_spent_percentage = Field(name="amount_spent_percentage", field_name="amount_spent_percentage", fields=["amount_spent_percentage"], field_type=FieldType.STRUCTURE)

    bid_cap = Field(name="bid_cap", field_name="bid_cap", fields=["bid_cap"], field_type=FieldType.STRUCTURE)

    budget = Field(name="budget", field_name="budget", fields=["budget"], field_type=FieldType.STRUCTURE)

    budget_remaining = Field(name="budget_remaining", field_name="budget_remaining", fields=["budget_remaining"], field_type=FieldType.STRUCTURE)

    date_start = Field(name="date_start", field_name="date_start", fields=["date_start"], field_type=FieldType.SIMPLE)

    date_stop = Field(name="date_stop", field_name="date_stop", fields=["date_stop"], field_type=FieldType.SIMPLE)

    ad_labels = Field(name="ad_labels", field_name="adlabels", fields=["adlabels"], field_type=FieldType.STRUCTURE)

    boosted_object_id = Field(name="boosted_object_id", field_name="boosted_object_id", fields=["boosted_object_id"], field_type=FieldType.STRUCTURE)

    brand_lift_studies = Field(name="brand_lift_studies", field_name="brand_lift_studies", fields=["brand_lift_studies"], field_type=FieldType.STRUCTURE)

    budget_rebalance_flag = Field(name="budget_rebalance_flag", field_name="budget_rebalance_flag", fields=["budget_rebalance_flag"], field_type=FieldType.STRUCTURE)

    can_create_brand_lift_study = Field(name="can_create_brand_lift_study", field_name="can_create_brand_lift_study", fields=["can_create_brand_lift_study"], field_type=FieldType.STRUCTURE)

    configured_status = Field(name="configured_status", field_name="configured_status", fields=["configured_status"], field_type=FieldType.STRUCTURE)

    can_use_spend_cap = Field(name="can_use_spend_cap", field_name="can_use_spend_cap", fields=["can_use_spend_cap"], field_type=FieldType.STRUCTURE)

    daily_budget = Field(name="daily_budget", field_name="daily_budget", fields=["daily_budget"], field_type=FieldType.STRUCTURE)

    last_budget_toggling_time = Field(name="last_budget_toggling_time", field_name="last_budget_toggling_time", fields=["last_budget_toggling_time"], field_type=FieldType.STRUCTURE)

    lifetime_budget = Field(name="lifetime_budget", field_name="lifetime_budget", fields=["lifetime_budget"], field_type=FieldType.STRUCTURE)

    pacing_type = Field(name="pacing_type", field_name="pacing_type", fields=["pacing_type"], field_type=FieldType.STRUCTURE)

    recommendations = Field(name="recommendations", field_name="recommendations", fields=["recommendations"], field_type=FieldType.STRUCTURE)

    promoted_object = Field(name="promoted_object", field_name="promoted_object", fields=["promoted_object"], field_type=FieldType.STRUCTURE)

    source_campaign = Field(name="source_campaign", field_name="source_campaign", fields=["source_campaign"], field_type=FieldType.STRUCTURE)

    special_ad_category = Field(name="special_ad_category", field_name="special_ad_category", fields=["special_ad_category"], field_type=FieldType.STRUCTURE)

    source_campaign_id = Field(name="source_campaign_id", field_name="source_campaign_id", fields=["source_campaign_id"], field_type=FieldType.STRUCTURE)

    spend_cap = Field(name="spend_cap", field_name="spend_cap", fields=["spend_cap"], field_type=FieldType.STRUCTURE)

    top_line_id = Field(name="topline_id", field_name="topline_id", fields=["topline_id"], field_type=FieldType.STRUCTURE)

    ad_rules_governed = Field(name="adrules_governed", field_name="adrules_governed", fields=["adrules_governed"], field_type=FieldType.STRUCTURE)

    updated_time = Field(name="updated_time", field_name="updated_time", fields=["updated_time"], field_type=FieldType.STRUCTURE)

    copies = Field(name="copies", field_name="copies", fields=["copies"], field_type=FieldType.STRUCTURE)

    adset_schedule = Field(name="adset_schedule", field_name="adset_schedule", fields=["adset_schedule"], field_type=FieldType.STRUCTURE)

    asset_feed_id = Field(name="asset_feed_id", field_name="asset_feed_id", fields=["asset_feed_id"], field_type=FieldType.STRUCTURE)

    attribution_spec = Field(name="attribution_spec", field_name="attribution_spec", fields=["attribution_spec"], field_type=FieldType.STRUCTURE)

    bid_adjustments = Field(name="bid_adjustments", field_name="bid_adjustments", fields=["bid_adjustments"], field_type=FieldType.STRUCTURE)

    bid_constraints = Field(name="bid_constraints", field_name="bid_constraints", fields=["bid_constraints"], field_type=FieldType.STRUCTURE)

    bid_amount = Field(name="bid_amount", field_name="bid_amount", fields=["bid_amount"], field_type=FieldType.STRUCTURE)

    bid_info = Field(name="bid_info", field_name="bid_info", fields=["bid_info"], field_type=FieldType.STRUCTURE)

    billing_event = Field(name="billing_event", field_name="billing_event", fields=["billing_event"], field_type=FieldType.STRUCTURE)

    campaign = Field(name="campaign", field_name="campaign", fields=["campaign"], field_type=FieldType.STRUCTURE)

    daily_min_spend_target = Field(name="daily_min_spend_target", field_name="daily_min_spend_target", fields=["daily_min_spend_target"], field_type=FieldType.STRUCTURE)

    destination_type = Field(name="destination_type", field_name="destination_type", fields=["destination_type"], field_type=FieldType.STRUCTURE)

    end_time = Field(name="end_time", field_name="end_time", fields=["end_time"], field_type=FieldType.STRUCTURE)

    frequency_control_specs = Field(name="frequency_control_specs", field_name="frequency_control_specs", fields=["frequency_control_specs"], field_type=FieldType.STRUCTURE)

    instagram_actor_id = Field(name="instagram_actor_id", field_name="instagram_actor_id", fields=["instagram_actor_id"], field_type=FieldType.STRUCTURE)

    is_dynamic_creative = Field(name="is_dynamic_creative", field_name="is_dynamic_creative", fields=["is_dynamic_creative"], field_type=FieldType.STRUCTURE)

    issues_info = Field(name="issues_info", field_name="issues_info", fields=["issues_info"], field_type=FieldType.STRUCTURE)

    lifetime_imps = Field(name="lifetime_imps", field_name="lifetime_imps", fields=["lifetime_imps"], field_type=FieldType.STRUCTURE)

    lifetime_spend_cap = Field(name="lifetime_spend_cap", field_name="lifetime_spend_cap", fields=["lifetime_spend_cap"], field_type=FieldType.STRUCTURE)

    optimization_goal = Field(name="optimization_goal", field_name="optimization_goal", fields=["optimization_goal"], field_type=FieldType.STRUCTURE)

    optimization_sub_event = Field(name="optimization_sub_event", field_name="optimization_sub_event", fields=["optimization_sub_event"], field_type=FieldType.STRUCTURE)

    source_adset = Field(name="source_adset", field_name="source_adset", fields=["source_adset"], field_type=FieldType.STRUCTURE)

    source_adset_id = Field(name="source_adset_id", field_name="source_adset_id", fields=["source_adset_id"], field_type=FieldType.STRUCTURE)

    targeting = Field(name="targeting", field_name="targeting", fields=["targeting"], field_type=FieldType.STRUCTURE)

    time_based_ad_rotation_id_blocks = Field(name="time_based_ad_rotation_id_blocks", field_name="time_based_ad_rotation_id_blocks", fields=["time_based_ad_rotation_id_blocks"], field_type=FieldType.STRUCTURE)

    time_based_ad_rotation_intervals = Field(name="time_based_ad_rotation_intervals", field_name="time_based_ad_rotation_intervals", fields=["time_based_ad_rotation_intervals"], field_type=FieldType.STRUCTURE)

    use_new_app_click = Field(name="use_new_app_click", field_name="use_new_app_click", fields=["use_new_app_click"], field_type=FieldType.STRUCTURE)

    lifetime_min_spend_target = Field(name="lifetime_min_spend_target", field_name="lifetime_min_spend_target", fields=["lifetime_min_spend_target"], field_type=FieldType.STRUCTURE)

    targetingsentencelines = Field(name="targetingsentencelines", field_name="targetingsentencelines", fields=["targetingsentencelines"], field_type=FieldType.STRUCTURE)

    daily_spend_cap = Field(name="daily_spend_cap", field_name="daily_spend_cap", fields=["daily_spend_cap"], field_type=FieldType.STRUCTURE)

    adset = Field(name="adset", field_name="adset", fields=["adset"], field_type=FieldType.STRUCTURE)

    creative = Field(name="creative", field_name="creative", fields=["creative"], field_type=FieldType.STRUCTURE)

    last_updated_by_app_id = Field(name="last_updated_by_app_id", field_name="last_updated_by_app_id", fields=["last_updated_by_app_id"], field_type=FieldType.STRUCTURE)

    source_ad = Field(name="source_ad", field_name="source_ad", fields=["source_ad"], field_type=FieldType.STRUCTURE)

    source_ad_id = Field(name="source_ad_id", field_name="source_ad_id", fields=["source_ad_id"], field_type=FieldType.STRUCTURE)

    tracking_specs = Field(name="tracking_specs", field_name="tracking_specs", fields=["tracking_specs"], field_type=FieldType.STRUCTURE)

    ad_creatives = Field(name="ad_creative", field_name="adcreatives", fields=[ad_creative_field_definition], field_type=FieldType.STRUCTURE)

    campaign_structure_name = Field(name="campaign_name", field_name="campaign_name", fields=["campaign_name"], field_type=FieldType.STRUCTURE)

    campaign_structure_id = Field(name="campaign_id", field_name="campaign_id", fields=["campaign_id"], field_type=FieldType.STRUCTURE)

    adset_structure_name = Field(name="adset_name", field_name="adset_name", fields=["adset_name"], field_type=FieldType.STRUCTURE)

    adset_structure_id = Field(name="adset_id", field_name="adset_id", fields=["adset_id"], field_type=FieldType.STRUCTURE)

    ad_structure_name = Field(name="ad_name", field_name="ad_name", fields=["ad_name"], field_type=FieldType.STRUCTURE)

    ad_structure_id = Field(name="ad_id", field_name="ad_id", fields=["ad_id"], field_type=FieldType.STRUCTURE)

    ad_account_structure_id = Field(name="account_id", field_name="account_id", fields=["account_id"], field_type=FieldType.STRUCTURE)

    objective_structure = Field(name="objective", field_name="objective", fields=["objective"], field_type=FieldType.STRUCTURE)

    ad_account_structure_name = Field(name="account_name", field_name="account_name", fields=["account_name"], field_type=FieldType.STRUCTURE)

    # Targeting

    location = Field(name="location", field_name="location", fields=["location"], field_type=FieldType.STRUCTURE)

    age = Field(name="age", field_name="age", fields=["age"], field_type=FieldType.STRUCTURE)

    gender = Field(name="gender", field_name="gender", fields=["gender"], field_type=FieldType.STRUCTURE)

    included_custom_audiences = Field(name="included_custom_audiences", field_name="included_custom_audiences", fields=["included_custom_audiences"], field_type=FieldType.STRUCTURE)

    excluded_custom_audiences = Field(name="excluded_custom_audiences", field_name="excluded_custom_audiences", fields=["excluded_custom_audiences"], field_type=FieldType.STRUCTURE)

    # Ad creative

    page_name = Field(name="page_name", field_name="page_name", fields=["page_name"], field_type=FieldType.STRUCTURE)

    headline = Field(name="headline", field_name="headline", fields=["headline"], field_type=FieldType.STRUCTURE)

    body = Field(name="body", field_name="body", fields=["body"], field_type=FieldType.STRUCTURE)

    link = Field(name="link", field_name="link", fields=["link"], field_type=FieldType.STRUCTURE)

    destination = Field(name="destination", field_name="destination", fields=["destination"], field_type=FieldType.STRUCTURE)

    # Tracking
    url_parameters = Field(name="url_parameters", field_name="url_parameters", fields=["url_parameters"], field_type=FieldType.STRUCTURE)

    pixel = Field(name="pixel", field_name="pixel", fields=["pixel"], field_type=FieldType.STRUCTURE)

    app_event = Field(name="app_event", field_name="app_event", fields=["app_event"], field_type=FieldType.STRUCTURE)

    offline_event = Field(name="offline_event", field_name="offline_event", fields=["offline_event"], field_type=FieldType.STRUCTURE)

    # ====== PERFORMANCE ====== #

    reach = Field(name="reach", field_name="reach", fields=["reach"], field_type=FieldType.SIMPLE)

    frequency = Field(name="frequency", field_name="frequency", fields=["frequency"], field_type=FieldType.SIMPLE)

    impressions = Field(name="impressions", field_name="impressions", fields=["impressions"], field_type=FieldType.SIMPLE)

    # STRUCTURE columns
    status = Field(name="status", field_name="status", fields=["status"], field_type=FieldType.STRUCTURE)

    delivery = Field(name="delivery", field_name="effective_status", fields=["effective_status"], field_type=FieldType.STRUCTURE)

    adset_delivery = Field(name="adset_delivery", field_name="effective_status", fields=["adset", "effective_status"], field_type=FieldType.STRUCTURE)

    amount_spent = Field(name="amount_spent", field_name="spend", fields=["spend"], field_type=FieldType.SIMPLE)

    social_spend = Field(name="social_spend", field_name="social_spend", fields=["social_spend"], field_type=FieldType.SIMPLE)

    all_clicks = Field(name="clicks_all", field_name="clicks", fields=["clicks"], field_type=FieldType.SIMPLE)

    all_cpc = Field(name="cpc_all", field_name="cpc", fields=["cpc"], field_type=FieldType.SIMPLE)

    all_ctr = Field(name="ctr_all", field_name="ctr", fields=["ctr"], field_type=FieldType.SIMPLE)

    all_cpp = Field(name="cpp_all", field_name="cpp", fields=["cpp"], field_type=FieldType.SIMPLE)

    # impressions_gross TODO: FIND OUT WHERE FB GETS THIS INFO FROM

    # impressions_auto_refresh TODO: FIND OUT WHERE FB GETS THIS INFO FROM

    # ad relevance columns
    quality_ranking = Field(name="quality_ranking", field_name="quality_rankingt", fields=["quality_ranking"], field_type=FieldType.SIMPLE)

    engagement_rate_ranking = Field(name="engagement_rate_ranking", field_name="engagement_rate_ranking", fields=["engagement_rate_ranking"], field_type=FieldType.SIMPLE)

    conversion_rate_ranking = Field(name="conversion_rate_ranking", field_name="conversion_rate_ranking", fields=["conversion_rate_ranking"], field_type=FieldType.SIMPLE)

    # COST
    # COST per result
    # TODO: ADD FROM ABOVE

    # COST per 1000 people reached
    # TODO: ADD FROM ABOVE

    cpm = Field(name="cpm", field_name="cpm", fields=["cpm"], field_type=FieldType.SIMPLE)

    # ====== ENGAGEMENT ====== #
    # Page post

    page_engagement = Field(name="page_engagement", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="page_engagement", action_field_name_key="action_type", field_type=FieldType.NESTED)

    page_like = Field(name="page_like", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="like", action_field_name_key="action_type", field_type=FieldType.NESTED)

    post_comment = Field(name="post_comment", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="comment", action_field_name_key="action_type", field_type=FieldType.NESTED)

    post_engagement = Field(name="post_engagement", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="post_engagement", action_field_name_key="action_type", field_type=FieldType.NESTED)

    # TODO: Check this on FB
    post_reaction = Field(name="post_reaction", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="post_reaction", action_field_name_key="action_type", field_type=FieldType.NESTED)

    post_save = Field(name="post_save", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="onsite_conversion.post_save", action_field_name_key="action_type", field_type=FieldType.NESTED)

    post_share = Field(name="post_share", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="post", action_field_name_key="action_type", field_type=FieldType.NESTED)

    photo_view = Field(name="post_view", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="photo_view", action_field_name_key="action_type", field_type=FieldType.NESTED)

    event_responses = Field(name="event_responses", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="rsvp", action_field_name_key="action_type", field_type=FieldType.NESTED)

    # checkins
    # TODO: FIND OUT WHERE FB GETS THIS INFO

    full_view_impressions = Field(name="full_view_impressions", field_name="full_view_impressions", fields=["full_view_impressions"], field_type=FieldType.SIMPLE)

    full_view_reach = Field(name="full_view_reach", field_name="full_view_reach", fields=["full_view_reach"], field_type=FieldType.SIMPLE)

    # effect share
    # TODO: FIND OUT WHERE FB GETS THIS INFO

    # COST page and post

    cost_per_page_engagement = Field(name="cost_per_page_engagement", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="page_engagement", field_type=FieldType.NESTED)

    cost_per_page_like = Field(name="cost_per_page_like", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="like", field_type=FieldType.NESTED)

    cost_per_post_engagement = Field(name="cost_per_post_engagement", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="post_engagement", field_type=FieldType.NESTED)

    cost_per_event_response = Field(name="cost_per_event_response", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="rsvp", field_type=FieldType.NESTED)

    # messaging
    new_messaging_connections = Field(name="new_messaging_connections", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_first_reply", field_type=FieldType.NESTED)

    messaging_conversation_started_7d = Field(name="messaging_conversation_started_7d", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_conversation_started.7d", field_type=FieldType.NESTED)

    blocked_messaging_connections = Field(name="blocked_messaging_connections", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_block", field_type=FieldType.NESTED)

    #  COST per messaging
    cost_per_new_messaging_connection = Field(name="cost_per_new_messaging_connection", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_first_reply", field_type=FieldType.NESTED)

    # media
    video_play = Field(name="video_play", field_name="video_play_actions", fields=["video_play_actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FieldType.NESTED)

    thruplay = Field(name="thruplay", field_name="video_thruplay_watched_actions", fields=["video_thruplay_watched_actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FieldType.NESTED)

    unique_2s_continuous_video_play = Field(name="unique_two_second_continuous_video_play", field_name="unique_actions", fields=["unique_actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FieldType.NESTED)

    two_seconds_continuous_video_play = Field(name="two_second_continuous_video_play", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FieldType.NESTED)

    total_video_25p_watched_actions = Field(name="total_video_25p_watched_actions", field_name="video_p25_watched_actions", fields=["video_p25_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="TOTAL", field_type=FieldType.NESTED)

    click_to_play_video_25p_watched_actions = Field(name="click_to_play_video_25p_watched_actions", field_name="video_p25_watched_actions", fields=["video_p25_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", field_type=FieldType.NESTED)

    autoplay_video_25p_watched_actions = Field(name="auto_play_video_25p_watched_actions", field_name="video_p25_watched_actions", fields=["video_p25_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="auto_play", field_type=FieldType.NESTED)

    total_video_50p_watched_actions = Field(name="total_video_50p_watched_actions", field_name="video_p50_watched_actions", fields=["video_p50_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="TOTAL", field_type=FieldType.NESTED)

    click_to_play_video_50p_watched_actions = Field(name="click_to_play_video_50p_watched_actions", field_name="video_p50_watched_actions", fields=["video_p50_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", field_type=FieldType.NESTED)

    autoplay_video_50p_watched_actions = Field(name="auto_play_video_50p_watched_actions", field_name="video_p50_watched_actions", fields=["video_p50_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="auto_play", field_type=FieldType.NESTED)

    total_video_75p_watched_actions = Field(name="total_video_75p_watched_actions", field_name="video_p75_watched_actions", fields=["video_p75_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="TOTAL", field_type=FieldType.NESTED)

    click_to_play_video_75p_watched_actions = Field(name="click_to_play_video_75p_watched_actions", field_name="video_p75_watched_actions", fields=["video_p75_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", field_type=FieldType.NESTED)

    autoplay_video_75p_watched_actions = Field(name="auto_play_video_75p_watched_actions", field_name="video_p75_watched_actions", fields=["video_p75_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="auto_play", field_type=FieldType.NESTED)

    total_video_95p_watched_actions = Field(name="total_video_95p_watched_actions", field_name="video_p95_watched_actions", fields=["video_p95_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="TOTAL", field_type=FieldType.NESTED)

    click_to_play_video_95p_watched_actions = Field(name="click_to_play_video_95p_watched_actions", field_name="video_p95_watched_actions", fields=["video_p95_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", field_type=FieldType.NESTED)

    autoplay_video_95p_watched_actions = Field(name="auto_play_video_95p_watched_actions", field_name="video_p95_watched_actions", fields=["video_p95_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="auto_play", field_type=FieldType.NESTED)

    total_video_100p_watched_actions = Field(name="total_video_100p_watched_actions", field_name="video_p100_watched_actions", fields=["video_p100_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="TOTAL", field_type=FieldType.NESTED)

    click_to_play_video_100p_watched_actions = Field(name="click_to_play_video_100p_watched_actions", field_name="video_p100_watched_actions", fields=["video_p100_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", field_type=FieldType.NESTED)

    autoplay_video_100p_watched_actions = Field(name="auto_play_video_100p_watched_actions", field_name="video_p100_watched_actions", fields=["video_p100_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="auto_play", field_type=FieldType.NESTED)

    instant_experience_view_time = Field(name="canvas_avg_view_time", field_name="canvas_avg_view_time", fields=["canvas_avg_view_time"], field_type=FieldType.SIMPLE)

    instant_experience_view_percentage = Field(name="canvas_avg_view_percent", field_name="canvas_avg_view_percent", fields=["canvas_avg_view_percent"], field_type=FieldType.SIMPLE)

    # COST media
    cost_per_2s_continuous_video_play = Field(name="cost_per_two_second_continuous_video_play", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FieldType.NESTED)

    cost_per_thruplay = Field(name="cost_per_thruplay_video_play", field_name="cost_per_thruplay", fields=["cost_per_thruplay"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FieldType.NESTED)

    # clicks

    link_click = Field(name="link_click", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", field_type=FieldType.NESTED)

    unique_link_click = Field(name="unique_link_click", field_name="unique_actions", fields=["unique_actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", field_type=FieldType.NESTED)

    outbound_click = Field(name="outbound_clicks", field_name="outbound_clicks", fields=["outbound_clicks"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FieldType.NESTED)

    unique_outbound_click = Field(name="unique_outbound_clicks", field_name="unique_outbound_clicks", fields=["unique_outbound_clicks"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FieldType.NESTED)

    link_click_ctr = Field(name="link_click_ctr", field_name="website_ctr", fields=["website_ctr"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", field_type=FieldType.NESTED)

    unique_link_click_ctr = Field(name="unique_link_clicks_ctr", field_name="unique_link_clicks_ctr", fields=["unique_link_clicks_ctr"], field_type=FieldType.SIMPLE)

    outbound_link_click_ctr = Field(name="outbound_clicks_ctr", field_name="outbound_clicks_ctr", fields=["outbound_clicks_ctr"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FieldType.NESTED)

    unique_outbound_link_click_ctr = Field(name="unique_outbound_clicks_ctr", field_name="unique_outbound_clicks_ctr", fields=["unique_outbound_clicks_ctr"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FieldType.NESTED)

    unique_click = Field(name="unique_clicks", field_name="unique_clicks", fields=["unique_clicks"], field_type=FieldType.SIMPLE)

    unique_ctr = Field(name="unique_ctr", field_name="unique_ctr", fields=["unique_ctr"], field_type=FieldType.SIMPLE)

    instant_experience_click_to_open = Field(name="instant_experience_clicks_to_open", field_name="instant_experience_clicks_to_open", fields=["instant_experience_clicks_to_open"], field_type=FieldType.SIMPLE)

    instant_experience_click_to_start = Field(name="instant_experience_clicks_to_start", field_name="instant_experience_clicks_to_start", fields=["instant_experience_clicks_to_start"], field_type=FieldType.SIMPLE)

    instant_experience_outbound_click = Field(name="instant_experience_outbound_clicks", field_name="instant_experience_outbound_clicks", fields=["instant_experience_outbound_clicks"], field_type=FieldType.SIMPLE)

    # COST clicks
    cost_per_link_click = Field(name="cost_per_link_click", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", field_type=FieldType.NESTED)

    cost_per_unique_link_click = Field(name="cost_per_unique_link_click", field_name="cost_per_unique_action_type", fields=["cost_per_unique_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", field_type=FieldType.NESTED)

    cost_per_outbound_link_click = Field(name="cost_per_outbound_click", field_name="cost_per_outbound_click", fields=["cost_per_outbound_click"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FieldType.NESTED)

    click_per_unique_outbound_link_click = Field(name="cost_per_unique_outbound_click", field_name="cost_per_unique_outbound_click", fields=["cost_per_unique_outbound_click"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FieldType.NESTED)

    cost_per_unique_click_all = Field(name="cost_per_unique_click", field_name="cost_per_unique_click", fields=["cost_per_unique_click"], field_type=FieldType.SIMPLE)

    # awareness
    estimated_ad_recall_lift = Field(name="estimated_ad_recallers", field_name="estimated_ad_recallers", fields=["estimated_ad_recallers"], field_type=FieldType.SIMPLE)

    estimated_ad_recall_rate = Field(name="estimated_ad_recall_rate", field_name="estimated_ad_recall_rate", fields=["estimated_ad_recall_rate"], field_type=FieldType.SIMPLE)

    cost_per_estimated_ad_recall_lift = Field(name="cost_per_estimated_ad_recallers", field_name="cost_per_estimated_ad_recallers", fields=["cost_per_estimated_ad_recallers"], field_type=FieldType.SIMPLE)

    website_purchase_roas = Field(name="website_purchase_roas", field_name="website_purchase_roas", fields=["website_purchase_roas"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="offsite_conversion.", field_type=FieldType.NESTED)

    purchase_roas = Field(name="purchase_roas", field_name="purchase_roas", fields=["purchase_roas"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="omni_purchase", field_type=FieldType.NESTED)

    # ======= Breakdowns ====== #

    # delivery
    age_breakdown = Field(name="age_breakdown", field_name="age", breakdowns=["age"], field_type=FieldType.BREAKDOWN)

    gender_breakdown = Field(name="gender_breakdown", field_name="gender", breakdowns=["gender"], field_type=FieldType.BREAKDOWN)

    country = Field(name="country", field_name="country", breakdowns=["country"], field_type=FieldType.BREAKDOWN)

    dma = Field(name="dma", field_name="dma", breakdowns=["dma"], field_type=FieldType.BREAKDOWN)

    impression_device = Field(name="impression_device", field_name="impression_device", breakdowns=["impression_device"], field_type=FieldType.BREAKDOWN)

    publisher_platform = Field(name="publisher_platform", field_name="publisher_platform", breakdowns=["publisher_platform"], field_type=FieldType.BREAKDOWN)

    placement = Field(name="placement", field_name=["publisher_platform", "platform_position", "device_platform"], breakdowns=["publisher_platform", "platform_position", "device_platform"], field_type=FieldType.BREAKDOWN)

    product_id = Field(name="product_id", field_name="product_id", breakdowns=["product_id"], field_type=FieldType.BREAKDOWN)

    frequency_value = Field(name="frequency_value", field_name="frequency_value", breakdowns=["frequency_value"], field_type=FieldType.BREAKDOWN)

    hourly_stats_aggregated_by_advertiser_time_zone = Field(name="hourly_stats_aggregated_by_advertiser_time_zone", field_name="hourly_stats_aggregated_by_advertiser_time_zone", breakdowns=["hourly_stats_aggregated_by_advertiser_time_zone"], field_type=FieldType.BREAKDOWN)

    hourly_stats_aggregated_by_audience_time_zone = Field(name="hourly_stats_aggregated_by_audience_time_zone", field_name="hourly_stats_aggregated_by_audience_time_zone", breakdowns=["hourly_stats_aggregated_by_audience_time_zone"], field_type=FieldType.BREAKDOWN)

    business_locations = Field(name="place_page_id", field_name="place_page_id", breakdowns=["place_page_id"], field_type=FieldType.BREAKDOWN)

    platform_position = Field(name="platform_position", field_name="platform_position", breakdowns=["platform_position"], field_type=FieldType.BREAKDOWN)

    device_platform = Field(name="device_platform", field_name="device_platform", breakdowns=["device_platform"], field_type=FieldType.BREAKDOWN)

    age_gender = Field(name="age_gender", field_name=["age", "gender"], breakdowns=["age", "gender"], field_type=FieldType.BREAKDOWN)

    platform_and_device = Field(name="platform_and_device", field_name=["publisher_platform", "impression_device"], breakdowns=["publisher_platform", "impression_device"], field_type=FieldType.BREAKDOWN)

    placement_and_device = Field(name="placement_and_device", field_name=["publisher_platform", "platform_position", "device_platform", "impression_device"], breakdowns=["publisher_platform", "platform_position", "device_platform", "impression_device"], field_type=FieldType.BREAKDOWN)

    region = Field(name="region", field_name="region", breakdowns=["region"], field_type=FieldType.BREAKDOWN)

    # action breakdowns # TODO: DEFINE THEM PROPERLY
    action_type = Field(name="action_type", field_name="action_type", action_breakdowns=["action_type"], action_field_name_key="action_type", field_type=FieldType.ACTION_BREAKDOWN)

    device = Field(name="action_device", field_name="action_device", action_breakdowns=["action_device"], action_field_name_key="action_device", field_type=FieldType.ACTION_BREAKDOWN)

    canvas_component = Field(name="action_canvas_component_name", field_name="action_canvas_component_name", action_breakdowns=["action_canvas_component_name"], action_field_name_key="action_canvas_component_name", field_type=FieldType.ACTION_BREAKDOWN)

    carousel_card_id = Field(name="action_carousel_card_id", field_name="action_carousel_card_id", action_breakdowns=["action_carousel_card_id"], action_field_name_key="action_carousel_card_id", field_type=FieldType.ACTION_BREAKDOWN)

    carousel_card_name = Field(name="action_carousel_card_name", field_name="action_carousel_card_name", action_breakdowns=["action_carousel_card_name"], action_field_name_key="action_carousel_card_name", field_type=FieldType.ACTION_BREAKDOWN)

    destination_breakdown = Field(name="action_destination", field_name="action_destination", action_breakdowns=["action_destination"], action_field_name_key="action_destination", field_type=FieldType.ACTION_BREAKDOWN)

    reaction = Field(name="action_reaction", field_name="action_reaction", action_breakdowns=["action_reaction"], action_field_name_key="action_reaction", field_type=FieldType.ACTION_BREAKDOWN)

    target = Field(name="action_target_id", field_name="action_target_id", action_breakdowns=["action_target_id"], action_field_name_key="action_target_id", field_type=FieldType.ACTION_BREAKDOWN)

    video_sound = Field(name="action_video_sound", field_name="action_video_sound", action_breakdowns=["action_video_sound"], action_field_name_key="action_video_sound", field_type=FieldType.ACTION_BREAKDOWN)

    video_type = Field(name="action_video_type", field_name="action_video_type", action_breakdowns=["action_video_type"], action_field_name_key="action_video_type", field_type=FieldType.ACTION_BREAKDOWN)

    # time
    day = Field(name="day", field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value=1, field_type=FieldType.TIME_BREAKDOWN)

    week = Field(name="week", field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value=7, field_type=FieldType.TIME_BREAKDOWN)

    two_weeks = Field(name="two_weeks", field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value=14, field_type=FieldType.TIME_BREAKDOWN)

    monthly = Field(name="monthly", field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value="monthly", field_type=FieldType.TIME_BREAKDOWN)

    # ====== Custom columns ====== #
    results = Field(name="results", field_name="actions", fields=["actions", "objective"], action_breakdowns=["action_type"], action_field_name_key="action_type", field_type=FieldType.TOTAL)

    cost_per_result = Field(name="cost_per_result", field_name="actions", fields=["actions", "objective", "spend"], action_breakdowns=["action_type"], action_field_name_key="action_type", field_type=FieldType.COST)

    conversions = Field(name="conversions", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="conversion", field_type=FieldType.TOTAL)

    cost_per_conversion = Field(name="cost_per_conversion", field_name="actions", fields=["actions", "spend"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="conversion", field_type=FieldType.COST)

    cost_per_1000_people_reached = Field("cost_per_1000_people_reached", field_name="reach", fields=["reach", "spend"], field_type=FieldType.COST)

    actions = Field("actions", field_name="actions", fields=["actions"], field_type=FieldType.NESTED)