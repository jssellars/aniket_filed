from Turing.Infrastructure.Models.FacebookField import FacebookField
from Turing.Infrastructure.Models.FacebookField import FacebookFieldType


ad_creatives_field_definition = 'adcreatives{account_id, actor_id, applink_treatment, asset_feed_spec, authorization_category,' \
                                'auto_update, body, branded_content_sponsor_page_id, call_to_action_type, categorization_criteria, bundle_folder_id, category_media_source, destination_set_id,' \
                                'effective_authorization_category, effective_instagram_story_id, dynamic_ad_voice, effective_object_story_id, enable_direct_install, id, image_crops,' \
                                'enable_launch_instant_app, image_hash, image_url, instagram_permalink_url, instagram_story_id, instagram_actor_id, interactive_components_spec, link_deep_link_url,' \
                                'link_url, messenger_sponsored_message, link_og_id, name, object_id, object_story_id, object_story_spec, object_store_url, object_type, object_url,' \
                                'platform_customizations, playable_asset_id, place_page_set_id, portrait_customizations, product_set_id, status, template_url, recommender_settings, thumbnail_url,' \
                                'title, url_tags, use_page_actor_override, video_id, template_url_spec}'

class FacebookFieldsMetadata:

    # ====== STRUCTURE ====== #
    name = FacebookField(name="name", field_name="name", fields=["name"], field_type=FacebookFieldType.STRUCTURE)

    id = FacebookField(name="id", field_name="id", fields=["id"], field_type=FacebookFieldType.STRUCTURE)

    ad_account_id = FacebookField(name="account_id", field_name="account_id", fields=["account_id"], field_type=FacebookFieldType.SIMPLE)

    account_name = FacebookField(name="account_name", field_name="account_name", fields=["account_name"], field_type=FacebookFieldType.SIMPLE)

    ad_id = FacebookField(name="ad_id", field_name="ad_id", fields=["ad_id"], field_type=FacebookFieldType.SIMPLE)

    ad_name = FacebookField(name="ad_name", field_name="ad_name", fields=["ad_name"], field_type=FacebookFieldType.SIMPLE)

    adset_id = FacebookField(name="adset_id", field_name="adset_id", fields=["adset_id"], field_type=FacebookFieldType.SIMPLE)

    adset_name = FacebookField(name="adset_name", field_name="adset_name", fields=["adset_name"], field_type=FacebookFieldType.SIMPLE)

    buying_type = FacebookField(name="buying_type", field_name="buying_type", fields=["buying_type"], field_type=FacebookFieldType.STRUCTURE)

    campaign_id = FacebookField(name="campaign_id", field_name="campaign_id", fields=["campaign_id"], field_type=FacebookFieldType.SIMPLE)

    campaign_name = FacebookField(name="campaign_name", field_name="campaign_name", fields=["campaign_name"], field_type=FacebookFieldType.SIMPLE)

    effective_status = FacebookField(name="effective_status", field_name="effective_status", fields=["effective_status"], field_type=FacebookFieldType.STRUCTURE)

    tags = FacebookField(name="tags", field_name="tags", fields=["tags"], field_type=FacebookFieldType.STRUCTURE)

    objective = FacebookField(name="objective", field_name="objective", fields=["objective"], field_type=FacebookFieldType.SIMPLE)

    created_at = FacebookField(name="created_time", field_name="created_time", fields=["created_time"], field_type=FacebookFieldType.STRUCTURE)

    last_significant_edit = FacebookField(name="last_significant_edit", field_name="last_significant_edit", fields=["last_significant_edit"], field_type=FacebookFieldType.STRUCTURE)

    start_date = FacebookField(name="start_time", field_name="start_time", fields=["start_time"], field_type=FacebookFieldType.STRUCTURE)

    end_date = FacebookField(name="stop_time", field_name="stop_time", fields=["stop_time"], field_type=FacebookFieldType.STRUCTURE)

    bid_strategy = FacebookField(name="bid_strategy", field_name="bid_strategy", fields=["bid_strategy"], field_type=FacebookFieldType.STRUCTURE)

    amount_spent_percentage = FacebookField(name="amount_spent_percentage", field_name="amount_spent_percentage", fields=["amount_spent_percentage"], field_type=FacebookFieldType.STRUCTURE)

    bid_cap = FacebookField(name="bid_cap", field_name="bid_cap", fields=["bid_cap"], field_type=FacebookFieldType.STRUCTURE)

    budget = FacebookField(name="budget", field_name="budget", fields=["budget"], field_type=FacebookFieldType.STRUCTURE)

    budget_remaining = FacebookField(name="budget_remaining", field_name="budget_remaining", fields=["budget_remaining"], field_type=FacebookFieldType.STRUCTURE)

    date_start = FacebookField(name="date_start", field_name="date_start", fields=["date_start"], field_type=FacebookFieldType.SIMPLE)

    date_stop = FacebookField(name="date_stop", field_name="date_stop", fields=["date_stop"], field_type=FacebookFieldType.SIMPLE)

    ad_labels = FacebookField(name="ad_labels", field_name="adlabels", fields=["adlabels"], field_type=FacebookFieldType.STRUCTURE)

    boosted_object_id = FacebookField(name="boosted_object_id", field_name="boosted_object_id", fields=["boosted_object_id"], field_type=FacebookFieldType.STRUCTURE)

    brand_lift_studies = FacebookField(name="brand_lift_studies", field_name="brand_lift_studies", fields=["brand_lift_studies"], field_type=FacebookFieldType.STRUCTURE)

    budget_rebalance_flag = FacebookField(name="budget_rebalance_flag", field_name="budget_rebalance_flag", fields=["budget_rebalance_flag"], field_type=FacebookFieldType.STRUCTURE)

    can_create_brand_lift_study = FacebookField(name="can_create_brand_lift_study", field_name="can_create_brand_lift_study", fields=["can_create_brand_lift_study"], field_type=FacebookFieldType.STRUCTURE)

    configured_status = FacebookField(name="configured_status", field_name="configured_status", fields=["configured_status"], field_type=FacebookFieldType.STRUCTURE)

    can_use_spend_cap = FacebookField(name="can_use_spend_cap", field_name="can_use_spend_cap", fields=["can_use_spend_cap"], field_type=FacebookFieldType.STRUCTURE)

    daily_budget = FacebookField(name="daily_budget", field_name="daily_budget", fields=["daily_budget"], field_type=FacebookFieldType.STRUCTURE)

    last_budget_toggling_time = FacebookField(name="last_budget_toggling_time", field_name="last_budget_toggling_time", fields=["last_budget_toggling_time"], field_type=FacebookFieldType.STRUCTURE)

    lifetime_budget = FacebookField(name="lifetime_budget", field_name="lifetime_budget", fields=["lifetime_budget"], field_type=FacebookFieldType.STRUCTURE)

    pacing_type = FacebookField(name="pacing_type", field_name="pacing_type", fields=["pacing_type"], field_type=FacebookFieldType.STRUCTURE)

    recommendations = FacebookField(name="recommendations", field_name="recommendations", fields=["recommendations"], field_type=FacebookFieldType.STRUCTURE)

    promoted_object = FacebookField(name="promoted_object", field_name="promoted_object", fields=["promoted_object"], field_type=FacebookFieldType.STRUCTURE)

    source_campaign = FacebookField(name="source_campaign", field_name="source_campaign", fields=["source_campaign"], field_type=FacebookFieldType.STRUCTURE)

    special_ad_category = FacebookField(name="special_ad_category", field_name="special_ad_category", fields=["special_ad_category"], field_type=FacebookFieldType.STRUCTURE)

    source_campaign_id = FacebookField(name="source_campaign_id", field_name="source_campaign_id", fields=["source_campaign_id"], field_type=FacebookFieldType.STRUCTURE)

    spend_cap = FacebookField(name="spend_cap", field_name="spend_cap", fields=["spend_cap"], field_type=FacebookFieldType.STRUCTURE)

    top_line_id = FacebookField(name="topline_id", field_name="topline_id", fields=["topline_id"], field_type=FacebookFieldType.STRUCTURE)

    ad_rules_governed = FacebookField(name="adrules_governed", field_name="adrules_governed", fields=["adrules_governed"], field_type=FacebookFieldType.STRUCTURE)

    updated_time = FacebookField(name="updated_time", field_name="updated_time", fields=["updated_time"], field_type=FacebookFieldType.STRUCTURE)

    copies = FacebookField(name="copies", field_name="copies", fields=["copies"], field_type=FacebookFieldType.STRUCTURE)

    adset_schedule = FacebookField(name="adset_schedule", field_name="adset_schedule", fields=["adset_schedule"], field_type=FacebookFieldType.STRUCTURE)

    asset_feed_id = FacebookField(name="asset_feed_id", field_name="asset_feed_id", fields=["asset_feed_id"], field_type=FacebookFieldType.STRUCTURE)

    attribution_spec = FacebookField(name="attribution_spec", field_name="attribution_spec", fields=["attribution_spec"], field_type=FacebookFieldType.STRUCTURE)

    bid_adjustments = FacebookField(name="bid_adjustments", field_name="bid_adjustments", fields=["bid_adjustments"], field_type=FacebookFieldType.STRUCTURE)

    bid_constraints = FacebookField(name="bid_constraints", field_name="bid_constraints", fields=["bid_constraints"], field_type=FacebookFieldType.STRUCTURE)

    bid_amount = FacebookField(name="bid_amount", field_name="bid_amount", fields=["bid_amount"], field_type=FacebookFieldType.STRUCTURE)

    bid_info = FacebookField(name="bid_info", field_name="bid_info", fields=["bid_info"], field_type=FacebookFieldType.STRUCTURE)

    billing_event = FacebookField(name="billing_event", field_name="billing_event", fields=["billing_event"], field_type=FacebookFieldType.STRUCTURE)

    campaign = FacebookField(name="campaign", field_name="campaign", fields=["campaign"], field_type=FacebookFieldType.STRUCTURE)

    daily_min_spend_target = FacebookField(name="daily_min_spend_target", field_name="daily_min_spend_target", fields=["daily_min_spend_target"], field_type=FacebookFieldType.STRUCTURE)

    destination_type = FacebookField(name="destination_type", field_name="destination_type", fields=["destination_type"], field_type=FacebookFieldType.STRUCTURE)

    end_time = FacebookField(name="end_time", field_name="end_time", fields=["end_time"], field_type=FacebookFieldType.STRUCTURE)

    frequency_control_specs = FacebookField(name="frequency_control_specs", field_name="frequency_control_specs", fields=["frequency_control_specs"], field_type=FacebookFieldType.STRUCTURE)

    instagram_actor_id = FacebookField(name="instagram_actor_id", field_name="instagram_actor_id", fields=["instagram_actor_id"], field_type=FacebookFieldType.STRUCTURE)

    is_dynamic_creative = FacebookField(name="is_dynamic_creative", field_name="is_dynamic_creative", fields=["is_dynamic_creative"], field_type=FacebookFieldType.STRUCTURE)

    issues_info = FacebookField(name="issues_info", field_name="issues_info", fields=["issues_info"], field_type=FacebookFieldType.STRUCTURE)

    lifetime_imps = FacebookField(name="lifetime_imps", field_name="lifetime_imps", fields=["lifetime_imps"], field_type=FacebookFieldType.STRUCTURE)

    lifetime_spend_cap = FacebookField(name="lifetime_spend_cap", field_name="lifetime_spend_cap", fields=["lifetime_spend_cap"], field_type=FacebookFieldType.STRUCTURE)

    optimization_goal = FacebookField(name="optimization_goal", field_name="optimization_goal", fields=["optimization_goal"], field_type=FacebookFieldType.STRUCTURE)

    optimization_sub_event = FacebookField(name="optimization_sub_event", field_name="optimization_sub_event", fields=["optimization_sub_event"], field_type=FacebookFieldType.STRUCTURE)

    source_adset = FacebookField(name="source_adset", field_name="source_adset", fields=["source_adset"], field_type=FacebookFieldType.STRUCTURE)

    source_adset_id = FacebookField(name="source_adset_id", field_name="source_adset_id", fields=["source_adset_id"], field_type=FacebookFieldType.STRUCTURE)

    targeting = FacebookField(name="targeting", field_name="targeting", fields=["targeting"], field_type=FacebookFieldType.STRUCTURE)

    time_based_ad_rotation_id_blocks = FacebookField(name="time_based_ad_rotation_id_blocks", field_name="time_based_ad_rotation_id_blocks", fields=["time_based_ad_rotation_id_blocks"], field_type=FacebookFieldType.STRUCTURE)

    time_based_ad_rotation_intervals = FacebookField(name="time_based_ad_rotation_intervals", field_name="time_based_ad_rotation_intervals", fields=["time_based_ad_rotation_intervals"], field_type=FacebookFieldType.STRUCTURE)

    use_new_app_click = FacebookField(name="use_new_app_click", field_name="use_new_app_click", fields=["use_new_app_click"], field_type=FacebookFieldType.STRUCTURE)

    lifetime_min_spend_target = FacebookField(name="lifetime_min_spend_target", field_name="lifetime_min_spend_target", fields=["lifetime_min_spend_target"], field_type=FacebookFieldType.STRUCTURE)

    targetingsentencelines = FacebookField(name="targetingsentencelines", field_name="targetingsentencelines", fields=["targetingsentencelines"], field_type=FacebookFieldType.STRUCTURE)

    daily_spend_cap = FacebookField(name="daily_spend_cap", field_name="daily_spend_cap", fields=["daily_spend_cap"], field_type=FacebookFieldType.STRUCTURE)

    adset = FacebookField(name="adset", field_name="adset", fields=["adset"], field_type=FacebookFieldType.STRUCTURE)

    creative = FacebookField(name="creative", field_name="creative", fields=["creative"], field_type=FacebookFieldType.STRUCTURE)

    last_updated_by_app_id = FacebookField(name="last_updated_by_app_id", field_name="last_updated_by_app_id", fields=["last_updated_by_app_id"], field_type=FacebookFieldType.STRUCTURE)

    source_ad = FacebookField(name="source_ad", field_name="source_ad", fields=["source_ad"], field_type=FacebookFieldType.STRUCTURE)

    source_ad_id = FacebookField(name="source_ad_id", field_name="source_ad_id", fields=["source_ad_id"], field_type=FacebookFieldType.STRUCTURE)

    tracking_specs = FacebookField(name="tracking_specs", field_name="tracking_specs", fields=["tracking_specs"], field_type=FacebookFieldType.STRUCTURE)

    ad_creatives = FacebookField(name="ad_creative", field_name="adcreatives", fields=[ad_creatives_field_definition], field_type=FacebookFieldType.STRUCTURE)

    campaign_structure_name = FacebookField(name="campaign_name", field_name="campaign_name", fields=["campaign_name"], field_type=FacebookFieldType.STRUCTURE)

    campaign_structure_id = FacebookField(name="campaign_id", field_name="campaign_id", fields=["campaign_id"], field_type=FacebookFieldType.STRUCTURE)

    adset_structure_name = FacebookField(name="adset_name", field_name="adset_name", fields=["adset_name"], field_type=FacebookFieldType.STRUCTURE)

    adset_structure_id = FacebookField(name="adset_id", field_name="adset_id", fields=["adset_id"], field_type=FacebookFieldType.STRUCTURE)

    ad_structure_name = FacebookField(name="ad_name", field_name="ad_name", fields=["ad_name"], field_type=FacebookFieldType.STRUCTURE)

    ad_structure_id = FacebookField(name="ad_id", field_name="ad_id", fields=["ad_id"], field_type=FacebookFieldType.STRUCTURE)

    ad_account_structure_id = FacebookField(name="account_id", field_name="account_id", fields=["account_id"], field_type=FacebookFieldType.STRUCTURE)

    objective_structure = FacebookField(name="objective", field_name="objective", fields=["objective"], field_type=FacebookFieldType.STRUCTURE)

    ad_account_structure_name = FacebookField(name="account_name", field_name="account_name", fields=["account_name"], field_type=FacebookFieldType.STRUCTURE)

    # Targeting

    location = FacebookField(name="location", field_name="location", fields=["location"], field_type=FacebookFieldType.STRUCTURE)

    age = FacebookField(name="age", field_name="age", fields=["age"], field_type=FacebookFieldType.STRUCTURE)

    gender = FacebookField(name="gender", field_name="gender", fields=["gender"], field_type=FacebookFieldType.STRUCTURE)

    included_custom_audiences = FacebookField(name="included_custom_audiences", field_name="included_custom_audiences", fields=["included_custom_audiences"], field_type=FacebookFieldType.STRUCTURE)

    excluded_custom_audiences = FacebookField(name="excluded_custom_audiences", field_name="excluded_custom_audiences", fields=["excluded_custom_audiences"], field_type=FacebookFieldType.STRUCTURE)

    # Ad creative

    page_name = FacebookField(name="page_name", field_name="page_name", fields=["page_name"], field_type=FacebookFieldType.STRUCTURE)

    headline = FacebookField(name="headline", field_name="headline", fields=["headline"], field_type=FacebookFieldType.STRUCTURE)

    body = FacebookField(name="body", field_name="body", fields=["body"], field_type=FacebookFieldType.STRUCTURE)

    link = FacebookField(name="link", field_name="link", fields=["link"], field_type=FacebookFieldType.STRUCTURE)

    destination = FacebookField(name="destination", field_name="destination", fields=["destination"], field_type=FacebookFieldType.STRUCTURE)

    # Tracking
    url_parameters = FacebookField(name="url_parameters", field_name="url_parameters", fields=["url_parameters"], field_type=FacebookFieldType.STRUCTURE)

    pixel = FacebookField(name="pixel", field_name="pixel", fields=["pixel"], field_type=FacebookFieldType.STRUCTURE)

    app_event = FacebookField(name="app_event", field_name="app_event", fields=["app_event"], field_type=FacebookFieldType.STRUCTURE)

    offline_event = FacebookField(name="offline_event", field_name="offline_event", fields=["offline_event"], field_type=FacebookFieldType.STRUCTURE)

    # ====== PERFORMANCE ====== #

    reach = FacebookField(name="reach", field_name="reach", fields=["reach"], field_type=FacebookFieldType.SIMPLE)

    frequency = FacebookField(name="frequency", field_name="frequency", fields=["frequency"], field_type=FacebookFieldType.SIMPLE)

    impressions = FacebookField(name="impressions", field_name="impressions", fields=["impressions"], field_type=FacebookFieldType.SIMPLE)

    # STRUCTURE columns
    status = FacebookField(name="status", field_name="status", fields=["status"], field_type=FacebookFieldType.STRUCTURE)

    delivery = FacebookField(name="delivery", field_name="effective_status", fields=["effective_status"], field_type=FacebookFieldType.STRUCTURE)

    adset_delivery = FacebookField(name="adset_delivery", field_name="effective_status", fields=["adset", "effective_status"], field_type=FacebookFieldType.STRUCTURE)

    amount_spent = FacebookField(name="amount_spent", field_name="spend", fields=["spend"], field_type=FacebookFieldType.SIMPLE)

    social_spend = FacebookField(name="social_spend", field_name="social_spend", fields=["social_spend"], field_type=FacebookFieldType.SIMPLE)

    all_clicks = FacebookField(name="clicks_all", field_name="clicks", fields=["clicks"], field_type=FacebookFieldType.SIMPLE)

    all_cpc = FacebookField(name="cpc_all", field_name="cpc", fields=["cpc"], field_type=FacebookFieldType.SIMPLE)

    all_ctr = FacebookField(name="ctr_all", field_name="ctr", fields=["ctr"], field_type=FacebookFieldType.SIMPLE)

    all_cpp = FacebookField(name="cpp_all", field_name="cpp", fields=["cpp"], field_type=FacebookFieldType.SIMPLE)

    # impressions_gross TODO: FIND OUT WHERE FB GETS THIS INFO FROM

    # impressions_auto_refresh TODO: FIND OUT WHERE FB GETS THIS INFO FROM

    # ad relevance columns
    quality_ranking = FacebookField(name="quality_ranking", field_name="quality_rankingt", fields=["quality_ranking"], field_type=FacebookFieldType.SIMPLE)

    engagement_rate_ranking = FacebookField(name="engagement_rate_ranking", field_name="engagement_rate_ranking", fields=["engagement_rate_ranking"], field_type=FacebookFieldType.SIMPLE)

    conversion_rate_ranking = FacebookField(name="conversion_rate_ranking", field_name="conversion_rate_ranking", fields=["conversion_rate_ranking"], field_type=FacebookFieldType.SIMPLE)

    # COST
    # COST per result
    # TODO: ADD FROM ABOVE

    # COST per 1000 people reached
    # TODO: ADD FROM ABOVE

    cpm = FacebookField(name="cpm", field_name="cpm", fields=["cpm"], field_type=FacebookFieldType.SIMPLE)

    # ====== ENGAGEMENT ====== #
    # Page post

    page_engagement = FacebookField(name="page_engagement", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="page_engagement", action_field_name_key="action_type", field_type=FacebookFieldType.NESTED)

    page_like = FacebookField(name="page_like", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="like", action_field_name_key="action_type", field_type=FacebookFieldType.NESTED)

    post_comment = FacebookField(name="post_comment", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="comment", action_field_name_key="action_type", field_type=FacebookFieldType.NESTED)

    post_engagement = FacebookField(name="post_engagement", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="post_engagement", action_field_name_key="action_type", field_type=FacebookFieldType.NESTED)

    # TODO: Check this on FB
    post_reaction = FacebookField(name="post_reaction", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="post_reaction", action_field_name_key="action_type", field_type=FacebookFieldType.NESTED)

    post_save = FacebookField(name="post_save", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="onsite_conversion.post_save", action_field_name_key="action_type", field_type=FacebookFieldType.NESTED)

    post_share = FacebookField(name="post_share", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="post", action_field_name_key="action_type", field_type=FacebookFieldType.NESTED)

    photo_view = FacebookField(name="post_view", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="photo_view", action_field_name_key="action_type", field_type=FacebookFieldType.NESTED)

    event_responses = FacebookField(name="event_responses", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="rsvp", action_field_name_key="action_type", field_type=FacebookFieldType.NESTED)

    # checkins
    # TODO: FIND OUT WHERE FB GETS THIS INFO

    full_view_impressions = FacebookField(name="full_view_impressions", field_name="full_view_impressions", fields=["full_view_impressions"], field_type=FacebookFieldType.SIMPLE)

    full_view_reach = FacebookField(name="full_view_reach", field_name="full_view_reach", fields=["full_view_reach"], field_type=FacebookFieldType.SIMPLE)

    # effect share
    # TODO: FIND OUT WHERE FB GETS THIS INFO

    # COST page and post

    cost_per_page_engagement = FacebookField(name="cost_per_page_engagement", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="page_engagement", field_type=FacebookFieldType.NESTED)

    cost_per_page_like = FacebookField(name="cost_per_page_like", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="like", field_type=FacebookFieldType.NESTED)

    cost_per_post_engagement = FacebookField(name="cost_per_post_engagement", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="post_engagement", field_type=FacebookFieldType.NESTED)

    cost_per_event_response = FacebookField(name="cost_per_event_response", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="rsvp", field_type=FacebookFieldType.NESTED)

    # messaging
    new_messaging_connections = FacebookField(name="new_messaging_connections", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_first_reply", field_type=FacebookFieldType.NESTED)

    messaging_conversation_started_7d = FacebookField(name="messaging_conversation_started_7d", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_conversation_started.7d", field_type=FacebookFieldType.NESTED)

    blocked_messaging_connections = FacebookField(name="blocked_messaging_connections", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_block", field_type=FacebookFieldType.NESTED)

    #  COST per messaging
    cost_per_new_messaging_connection = FacebookField(name="cost_per_new_messaging_connection", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_first_reply", field_type=FacebookFieldType.NESTED)

    # media
    video_play = FacebookField(name="video_play", field_name="video_play_actions", fields=["video_play_actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FacebookFieldType.NESTED)

    thruplay = FacebookField(name="thruplay", field_name="video_thruplay_watched_actions", fields=["video_thruplay_watched_actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FacebookFieldType.NESTED)

    unique_2s_continuous_video_play = FacebookField(name="unique_two_second_continuous_video_play", field_name="unique_actions", fields=["unique_actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FacebookFieldType.NESTED)

    two_seconds_continuous_video_play = FacebookField(name="two_second_continuous_video_play", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FacebookFieldType.NESTED)

    total_video_25p_watched_actions = FacebookField(name="total_video_25p_watched_actions", field_name="video_p25_watched_actions", fields=["video_p25_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="TOTAL", field_type=FacebookFieldType.NESTED)

    click_to_play_video_25p_watched_actions = FacebookField(name="click_to_play_video_25p_watched_actions", field_name="video_p25_watched_actions", fields=["video_p25_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", field_type=FacebookFieldType.NESTED)

    autoplay_video_25p_watched_actions = FacebookField(name="auto_play_video_25p_watched_actions", field_name="video_p25_watched_actions", fields=["video_p25_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="auto_play", field_type=FacebookFieldType.NESTED)

    total_video_50p_watched_actions = FacebookField(name="total_video_50p_watched_actions", field_name="video_p50_watched_actions", fields=["video_p50_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="TOTAL", field_type=FacebookFieldType.NESTED)

    click_to_play_video_50p_watched_actions = FacebookField(name="click_to_play_video_50p_watched_actions", field_name="video_p50_watched_actions", fields=["video_p50_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", field_type=FacebookFieldType.NESTED)

    autoplay_video_50p_watched_actions = FacebookField(name="auto_play_video_50p_watched_actions", field_name="video_p50_watched_actions", fields=["video_p50_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="auto_play", field_type=FacebookFieldType.NESTED)

    total_video_75p_watched_actions = FacebookField(name="total_video_75p_watched_actions", field_name="video_p75_watched_actions", fields=["video_p75_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="TOTAL", field_type=FacebookFieldType.NESTED)

    click_to_play_video_75p_watched_actions = FacebookField(name="click_to_play_video_75p_watched_actions", field_name="video_p75_watched_actions", fields=["video_p75_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", field_type=FacebookFieldType.NESTED)

    autoplay_video_75p_watched_actions = FacebookField(name="auto_play_video_75p_watched_actions", field_name="video_p75_watched_actions", fields=["video_p75_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="auto_play", field_type=FacebookFieldType.NESTED)

    total_video_95p_watched_actions = FacebookField(name="total_video_95p_watched_actions", field_name="video_p95_watched_actions", fields=["video_p95_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="TOTAL", field_type=FacebookFieldType.NESTED)

    click_to_play_video_95p_watched_actions = FacebookField(name="click_to_play_video_95p_watched_actions", field_name="video_p95_watched_actions", fields=["video_p95_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", field_type=FacebookFieldType.NESTED)

    autoplay_video_95p_watched_actions = FacebookField(name="auto_play_video_95p_watched_actions", field_name="video_p95_watched_actions", fields=["video_p95_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="auto_play", field_type=FacebookFieldType.NESTED)

    total_video_100p_watched_actions = FacebookField(name="total_video_100p_watched_actions", field_name="video_p100_watched_actions", fields=["video_p100_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="TOTAL", field_type=FacebookFieldType.NESTED)

    click_to_play_video_100p_watched_actions = FacebookField(name="click_to_play_video_100p_watched_actions", field_name="video_p100_watched_actions", fields=["video_p100_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", field_type=FacebookFieldType.NESTED)

    autoplay_video_100p_watched_actions = FacebookField(name="auto_play_video_100p_watched_actions", field_name="video_p100_watched_actions", fields=["video_p100_watched_actions"], action_breakdowns=["action_video_type"], action_field_name_value="auto_play", field_type=FacebookFieldType.NESTED)

    instant_experience_view_time = FacebookField(name="canvas_avg_view_time", field_name="canvas_avg_view_time", fields=["canvas_avg_view_time"], field_type=FacebookFieldType.SIMPLE)

    instant_experience_view_percentage = FacebookField(name="canvas_avg_view_percent", field_name="canvas_avg_view_percent", fields=["canvas_avg_view_percent"], field_type=FacebookFieldType.SIMPLE)

    # COST media
    cost_per_2s_continuous_video_play = FacebookField(name="cost_per_two_second_continuous_video_play", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FacebookFieldType.NESTED)

    cost_per_thruplay = FacebookField(name="cost_per_thruplay_video_play", field_name="cost_per_thruplay", fields=["cost_per_thruplay"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", field_type=FacebookFieldType.NESTED)

    # clicks

    link_click = FacebookField(name="link_click", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", field_type=FacebookFieldType.NESTED)

    unique_link_click = FacebookField(name="unique_link_click", field_name="unique_actions", fields=["unique_actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", field_type=FacebookFieldType.NESTED)

    outbound_click = FacebookField(name="outbound_clicks", field_name="outbound_clicks", fields=["outbound_clicks"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FacebookFieldType.NESTED)

    unique_outbound_click = FacebookField(name="unique_outbound_clicks", field_name="unique_outbound_clicks", fields=["unique_outbound_clicks"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FacebookFieldType.NESTED)

    link_click_ctr = FacebookField(name="link_click_ctr", field_name="website_ctr", fields=["website_ctr"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", field_type=FacebookFieldType.NESTED)

    unique_link_click_ctr = FacebookField(name="unique_link_clicks_ctr", field_name="unique_link_clicks_ctr", fields=["unique_link_clicks_ctr"], field_type=FacebookFieldType.SIMPLE)

    outbound_link_click_ctr = FacebookField(name="outbound_clicks_ctr", field_name="outbound_clicks_ctr", fields=["outbound_clicks_ctr"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FacebookFieldType.NESTED)

    unique_outbound_link_click_ctr = FacebookField(name="unique_outbound_clicks_ctr", field_name="unique_outbound_clicks_ctr", fields=["unique_outbound_clicks_ctr"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FacebookFieldType.NESTED)

    unique_click = FacebookField(name="unique_clicks", field_name="unique_clicks", fields=["unique_clicks"], field_type=FacebookFieldType.SIMPLE)

    unique_ctr = FacebookField(name="unique_ctr", field_name="unique_ctr", fields=["unique_ctr"], field_type=FacebookFieldType.SIMPLE)

    instant_experience_click_to_open = FacebookField(name="instant_experience_clicks_to_open", field_name="instant_experience_clicks_to_open", fields=["instant_experience_clicks_to_open"], field_type=FacebookFieldType.SIMPLE)

    instant_experience_click_to_start = FacebookField(name="instant_experience_clicks_to_start", field_name="instant_experience_clicks_to_start", fields=["instant_experience_clicks_to_start"], field_type=FacebookFieldType.SIMPLE)

    instant_experience_outbound_click = FacebookField(name="instant_experience_outbound_clicks", field_name="instant_experience_outbound_clicks", fields=["instant_experience_outbound_clicks"], field_type=FacebookFieldType.SIMPLE)

    # COST clicks
    cost_per_link_click = FacebookField(name="cost_per_link_click", field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", field_type=FacebookFieldType.NESTED)

    cost_per_unique_link_click = FacebookField(name="cost_per_unique_link_click", field_name="cost_per_unique_action_type", fields=["cost_per_unique_action_type"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", field_type=FacebookFieldType.NESTED)

    cost_per_outbound_link_click = FacebookField(name="cost_per_outbound_click", field_name="cost_per_outbound_click", fields=["cost_per_outbound_click"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FacebookFieldType.NESTED)

    click_per_unique_outbound_link_click = FacebookField(name="cost_per_unique_outbound_click", field_name="cost_per_unique_outbound_click", fields=["cost_per_unique_outbound_click"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", field_type=FacebookFieldType.NESTED)

    cost_per_unique_click_all = FacebookField(name="cost_per_unique_click", field_name="cost_per_unique_click", fields=["cost_per_unique_click"], field_type=FacebookFieldType.SIMPLE)

    # awareness
    estimated_ad_recall_lift = FacebookField(name="estimated_ad_recallers", field_name="estimated_ad_recallers", fields=["estimated_ad_recallers"], field_type=FacebookFieldType.SIMPLE)

    estimated_ad_recall_rate = FacebookField(name="estimated_ad_recall_rate", field_name="estimated_ad_recall_rate", fields=["estimated_ad_recall_rate"], field_type=FacebookFieldType.SIMPLE)

    cost_per_estimated_ad_recall_lift = FacebookField(name="cost_per_estimated_ad_recallers", field_name="cost_per_estimated_ad_recallers", fields=["cost_per_estimated_ad_recallers"], field_type=FacebookFieldType.SIMPLE)

    website_purchase_roas = FacebookField(name="website_purchase_roas", field_name="website_purchase_roas", fields=["website_purchase_roas"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="offsite_conversion.", field_type=FacebookFieldType.NESTED)

    purchase_roas = FacebookField(name="purchase_roas", field_name="purchase_roas", fields=["purchase_roas"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="omni_purchase", field_type=FacebookFieldType.NESTED)

    # ======= Breakdowns ====== #

    # delivery
    age_breakdown = FacebookField(name="age_breakdown", field_name="age", breakdowns=["age"], field_type=FacebookFieldType.BREAKDOWN)

    gender_breakdown = FacebookField(name="gender_breakdown", field_name="gender", breakdowns=["gender"], field_type=FacebookFieldType.BREAKDOWN)

    country = FacebookField(name="country", field_name="country", breakdowns=["country"], field_type=FacebookFieldType.BREAKDOWN)

    dma = FacebookField(name="dma", field_name="dma", breakdowns=["dma"], field_type=FacebookFieldType.BREAKDOWN)

    impression_device = FacebookField(name="impression_device", field_name="impression_device", breakdowns=["impression_device"], field_type=FacebookFieldType.BREAKDOWN)

    publisher_platform = FacebookField(name="publisher_platform", field_name="publisher_platform", breakdowns=["publisher_platform"], field_type=FacebookFieldType.BREAKDOWN)

    placement = FacebookField(name="placement", field_name=["publisher_platform", "platform_position", "device_platform"], breakdowns=["publisher_platform", "platform_position", "device_platform"], field_type=FacebookFieldType.BREAKDOWN)

    product_id = FacebookField(name="product_id", field_name="product_id", breakdowns=["product_id"], field_type=FacebookFieldType.BREAKDOWN)

    frequency_value = FacebookField(name="frequency_value", field_name="frequency_value", breakdowns=["frequency_value"], field_type=FacebookFieldType.BREAKDOWN)

    hourly_stats_aggregated_by_advertiser_time_zone = FacebookField(name="hourly_stats_aggregated_by_advertiser_time_zone", field_name="hourly_stats_aggregated_by_advertiser_time_zone", breakdowns=["hourly_stats_aggregated_by_advertiser_time_zone"], field_type=FacebookFieldType.BREAKDOWN)

    hourly_stats_aggregated_by_audience_time_zone = FacebookField(name="hourly_stats_aggregated_by_audience_time_zone", field_name="hourly_stats_aggregated_by_audience_time_zone", breakdowns=["hourly_stats_aggregated_by_audience_time_zone"], field_type=FacebookFieldType.BREAKDOWN)

    business_locations = FacebookField(name="place_page_id", field_name="place_page_id", breakdowns=["place_page_id"], field_type=FacebookFieldType.BREAKDOWN)

    platform_position = FacebookField(name="platform_position", field_name="platform_position", breakdowns=["platform_position"], field_type=FacebookFieldType.BREAKDOWN)

    device_platform = FacebookField(name="device_platform", field_name="device_platform", breakdowns=["device_platform"], field_type=FacebookFieldType.BREAKDOWN)

    age_gender = FacebookField(name="age_gender", field_name=["age", "gender"], breakdowns=["age", "gender"], field_type=FacebookFieldType.BREAKDOWN)

    platform_and_device = FacebookField(name="platform_and_device", field_name=["publisher_platform", "impression_device"], breakdowns=["publisher_platform", "impression_device"], field_type=FacebookFieldType.BREAKDOWN)

    placement_and_device = FacebookField(name="placement_and_device", field_name=["publisher_platform", "platform_position", "device_platform", "impression_device"], breakdowns=["publisher_platform", "platform_position", "device_platform", "impression_device"], field_type=FacebookFieldType.BREAKDOWN)

    region = FacebookField(name="region", field_name="region", breakdowns=["region"], field_type=FacebookFieldType.BREAKDOWN)

    # action breakdowns # TODO: DEFINE THEM PROPERLY
    action_type = FacebookField(name="action_type", field_name="action_type", action_breakdowns=["action_type"], action_field_name_key="action_type", field_type=FacebookFieldType.ACTION_BREAKDOWN)

    device = FacebookField(name="action_device", field_name="action_device", action_breakdowns=["action_device"], action_field_name_key="action_device", field_type=FacebookFieldType.ACTION_BREAKDOWN)

    canvas_component = FacebookField(name="action_canvas_component_name", field_name="action_canvas_component_name", action_breakdowns=["action_canvas_component_name"], action_field_name_key="action_canvas_component_name", field_type=FacebookFieldType.ACTION_BREAKDOWN)

    carousel_card_id = FacebookField(name="action_carousel_card_id", field_name="action_carousel_card_id", action_breakdowns=["action_carousel_card_id"], action_field_name_key="action_carousel_card_id", field_type=FacebookFieldType.ACTION_BREAKDOWN)

    carousel_card_name = FacebookField(name="action_carousel_card_name", field_name="action_carousel_card_name", action_breakdowns=["action_carousel_card_name"], action_field_name_key="action_carousel_card_name", field_type=FacebookFieldType.ACTION_BREAKDOWN)

    destination_breakdown = FacebookField(name="action_destination", field_name="action_destination", action_breakdowns=["action_destination"], action_field_name_key="action_destination", field_type=FacebookFieldType.ACTION_BREAKDOWN)

    reaction = FacebookField(name="action_reaction", field_name="action_reaction", action_breakdowns=["action_reaction"], action_field_name_key="action_reaction", field_type=FacebookFieldType.ACTION_BREAKDOWN)

    target = FacebookField(name="action_target_id", field_name="action_target_id", action_breakdowns=["action_target_id"], action_field_name_key="action_target_id", field_type=FacebookFieldType.ACTION_BREAKDOWN)

    video_sound = FacebookField(name="action_video_sound", field_name="action_video_sound", action_breakdowns=["action_video_sound"], action_field_name_key="action_video_sound", field_type=FacebookFieldType.ACTION_BREAKDOWN)

    video_type = FacebookField(name="action_video_type", field_name="action_video_type", action_breakdowns=["action_video_type"], action_field_name_key="action_video_type", field_type=FacebookFieldType.ACTION_BREAKDOWN)

    # time
    day = FacebookField(name="day", field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value=1, field_type=FacebookFieldType.TIME_BREAKDOWN)

    week = FacebookField(name="week", field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value=7, field_type=FacebookFieldType.TIME_BREAKDOWN)

    two_weeks = FacebookField(name="two_weeks", field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value=14, field_type=FacebookFieldType.TIME_BREAKDOWN)

    monthly = FacebookField(name="monthly", field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value="monthly", field_type=FacebookFieldType.TIME_BREAKDOWN)

    # ====== Custom columns ====== #
    results = FacebookField(name="results", field_name="actions", fields=["actions", "objective"], action_breakdowns=["action_type"], action_field_name_key="action_type", field_type=FacebookFieldType.TOTAL)

    cost_per_result = FacebookField(name="cost_per_result", field_name="actions", fields=["actions", "objective", "spend"], action_breakdowns=["action_type"], action_field_name_key="action_type", field_type=FacebookFieldType.COST)

    conversions = FacebookField(name="conversions", field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="conversion", field_type=FacebookFieldType.TOTAL)

    cost_per_conversion = FacebookField(name="cost_per_conversion", field_name="actions", fields=["actions", "spend"], action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="conversion", field_type=FacebookFieldType.COST)

    cost_per_1000_people_reached = FacebookField("cost_per_1000_people_reached", field_name="reach", fields=["reach", "spend"], field_type=FacebookFieldType.COST)

    actions = FacebookField("actions", field_name="actions", fields=["actions"], field_type=FacebookFieldType.NESTED)