from Models.FacebookFields.Field import Field
from Models.FacebookFields.Field import FieldType

ad_creatives_field_definition = 'adcreatives{account_id, actor_id, applink_treatment, asset_feed_spec, authorization_category,' \
                               'auto_update, body, branded_content_sponsor_page_id, call_to_action_type, categorization_criteria,' \
                               ' bundle_folder_id, category_media_source, destination_set_id,' \
                               'effective_authorization_category, effective_instagram_story_id, dynamic_ad_voice, effective_object_story_id, enable_direct_install, id, image_crops,' \
                               'enable_launch_instant_app, image_hash, image_url, instagram_permalink_url, instagram_story_id,' \
                               ' instagram_actor_id, interactive_components_spec, link_deep_link_url,' \
                               'link_url, messenger_sponsored_message, link_og_id, name, object_id, object_story_id, object_story_spec, object_store_url, object_type, object_url,' \
                               'platform_customizations, playable_asset_id, place_page_set_id, portrait_customizations,' \
                               ' product_set_id, status, template_url, recommender_settings, thumbnail_url,' \
                               'title, url_tags, use_page_actor_override, video_id, template_url_spec}'


class FieldMetadata:
    # ====== STRUCTURE ====== #
    name = Field(name="name", source_field_name="name", fields=["name"], type_id=FieldType.structure)

    id = Field(name="id", source_field_name="id", fields=["id"], type_id=FieldType.structure)

    ad_account_id = Field(name="account_id", source_field_name="account_id", fields=["account_id"], type_id=FieldType.simple)

    account_name = Field(name="account_name", source_field_name="account_name", fields=["account_name"], type_id=FieldType.simple)

    ad_id = Field(name="ad_id", source_field_name="ad_id", fields=["ad_id"], type_id=FieldType.simple)

    ad_name = Field(name="ad_name", source_field_name="ad_name", fields=["ad_name"], type_id=FieldType.simple)

    adset_id = Field(name="adset_id", source_field_name="adset_id", fields=["adset_id"], type_id=FieldType.simple)

    adset_name = Field(name="adset_name", source_field_name="adset_name", fields=["adset_name"], type_id=FieldType.simple)

    buying_type = Field(name="buying_type", source_field_name="buying_type", fields=["buying_type"], type_id=FieldType.structure)

    campaign_id = Field(name="campaign_id", source_field_name="campaign_id", fields=["campaign_id"], type_id=FieldType.simple)

    campaign_name = Field(name="campaign_name", source_field_name="campaign_name", fields=["campaign_name"], type_id=FieldType.simple)

    effective_status = Field(name="effective_status", source_field_name="effective_status", fields=["effective_status"], type_id=FieldType.structure)

    tags = Field(name="tags", source_field_name="tags", fields=["tags"], type_id=FieldType.structure)

    objective = Field(name="objective", source_field_name="objective", fields=["objective"], type_id=FieldType.simple)

    created_at = Field(name="created_time", source_field_name="created_time", fields=["created_time"], type_id=FieldType.structure)

    last_significant_edit = Field(name="last_significant_edit", source_field_name="last_significant_edit", fields=["last_significant_edit"], type_id=FieldType.structure)

    start_date = Field(name="start_time", source_field_name="start_time", fields=["start_time"], type_id=FieldType.structure)

    end_date = Field(name="stop_time", source_field_name="stop_time", fields=["stop_time"], type_id=FieldType.structure)

    bid_strategy = Field(name="bid_strategy", source_field_name="bid_strategy", fields=["bid_strategy"], type_id=FieldType.structure)

    amount_spent_percentage = Field(name="amount_spent_percentage", source_field_name="amount_spent_percentage", fields=["amount_spent_percentage"], type_id=FieldType.structure)

    bid_cap = Field(name="bid_cap", source_field_name="bid_cap", fields=["bid_cap"], type_id=FieldType.structure)

    budget = Field(name="budget", source_field_name="budget", fields=["budget"], type_id=FieldType.structure)

    budget_remaining = Field(name="budget_remaining", source_field_name="budget_remaining", fields=["budget_remaining"], type_id=FieldType.structure)

    date_start = Field(name="date_start", source_field_name="date_start", fields=["date_start"], type_id=FieldType.simple)

    date_stop = Field(name="date_stop", source_field_name="date_stop", fields=["date_stop"], type_id=FieldType.simple)

    ad_labels = Field(name="ad_labels", source_field_name="adlabels", fields=["adlabels"], type_id=FieldType.structure)

    boosted_object_id = Field(name="boosted_object_id", source_field_name="boosted_object_id", fields=["boosted_object_id"], type_id=FieldType.structure)

    brand_lift_studies = Field(name="brand_lift_studies", source_field_name="brand_lift_studies", fields=["brand_lift_studies"], type_id=FieldType.structure)

    budget_rebalance_flag = Field(name="budget_rebalance_flag", source_field_name="budget_rebalance_flag", fields=["budget_rebalance_flag"], type_id=FieldType.structure)

    can_create_brand_lift_study = Field(name="can_create_brand_lift_study", source_field_name="can_create_brand_lift_study", fields=["can_create_brand_lift_study"],
                                        type_id=FieldType.structure)

    configured_status = Field(name="configured_status", source_field_name="configured_status", fields=["configured_status"], type_id=FieldType.structure)

    can_use_spend_cap = Field(name="can_use_spend_cap", source_field_name="can_use_spend_cap", fields=["can_use_spend_cap"], type_id=FieldType.structure)

    daily_budget = Field(name="daily_budget", source_field_name="daily_budget", fields=["daily_budget"], type_id=FieldType.structure)

    last_budget_toggling_time = Field(name="last_budget_toggling_time", source_field_name="last_budget_toggling_time", fields=["last_budget_toggling_time"], type_id=FieldType.structure)

    lifetime_budget = Field(name="lifetime_budget", source_field_name="lifetime_budget", fields=["lifetime_budget"], type_id=FieldType.structure)

    pacing_type = Field(name="pacing_type", source_field_name="pacing_type", fields=["pacing_type"], type_id=FieldType.structure)

    recommendations = Field(name="recommendations", source_field_name="recommendations", fields=["recommendations"], type_id=FieldType.structure)

    promoted_object = Field(name="promoted_object", source_field_name="promoted_object", fields=["promoted_object"], type_id=FieldType.structure)

    source_campaign = Field(name="source_campaign", source_field_name="source_campaign", fields=["source_campaign"], type_id=FieldType.structure)

    special_ad_category = Field(name="special_ad_category", source_field_name="special_ad_category", fields=["special_ad_category"], type_id=FieldType.structure)

    source_campaign_id = Field(name="source_campaign_id", source_field_name="source_campaign_id", fields=["source_campaign_id"], type_id=FieldType.structure)

    spend_cap = Field(name="spend_cap", source_field_name="spend_cap", fields=["spend_cap"], type_id=FieldType.structure)

    topline_id = Field(name="topline_id", source_field_name="topline_id", fields=["topline_id"], type_id=FieldType.structure)

    ad_rules_governed = Field(name="adrules_governed", source_field_name="adrules_governed", fields=["adrules_governed"], type_id=FieldType.structure)

    updated_time = Field(name="updated_time", source_field_name="updated_time", fields=["updated_time"], type_id=FieldType.structure)

    copies = Field(name="copies", source_field_name="copies", fields=["copies"], type_id=FieldType.structure)

    adset_schedule = Field(name="adset_schedule", source_field_name="adset_schedule", fields=["adset_schedule"], type_id=FieldType.structure)

    asset_feed_id = Field(name="asset_feed_id", source_field_name="asset_feed_id", fields=["asset_feed_id"], type_id=FieldType.structure)

    attribution_spec = Field(name="attribution_spec", source_field_name="attribution_spec", fields=["attribution_spec"], type_id=FieldType.structure)

    bid_adjustments = Field(name="bid_adjustments", source_field_name="bid_adjustments", fields=["bid_adjustments"], type_id=FieldType.structure)

    bid_constraints = Field(name="bid_constraints", source_field_name="bid_constraints", fields=["bid_constraints"], type_id=FieldType.structure)

    bid_amount = Field(name="bid_amount", source_field_name="bid_amount", fields=["bid_amount"], type_id=FieldType.structure)

    bid_info = Field(name="bid_info", source_field_name="bid_info", fields=["bid_info"], type_id=FieldType.structure)

    billing_event = Field(name="billing_event", source_field_name="billing_event", fields=["billing_event"], type_id=FieldType.structure)

    campaign = Field(name="campaign", source_field_name="campaign", fields=["campaign"], type_id=FieldType.structure)

    daily_min_spend_target = Field(name="daily_min_spend_target", source_field_name="daily_min_spend_target", fields=["daily_min_spend_target"], type_id=FieldType.structure)

    destination_type = Field(name="destination_type", source_field_name="destination_type", fields=["destination_type"], type_id=FieldType.structure)

    end_time = Field(name="end_time", source_field_name="end_time", fields=["end_time"], type_id=FieldType.structure)

    frequency_control_specs = Field(name="frequency_control_specs", source_field_name="frequency_control_specs", fields=["frequency_control_specs"], type_id=FieldType.structure)

    instagram_actor_id = Field(name="instagram_actor_id", source_field_name="instagram_actor_id", fields=["instagram_actor_id"], type_id=FieldType.structure)

    is_dynamic_creative = Field(name="is_dynamic_creative", source_field_name="is_dynamic_creative", fields=["is_dynamic_creative"], type_id=FieldType.structure)

    issues_info = Field(name="issues_info", source_field_name="issues_info", fields=["issues_info"], type_id=FieldType.structure)

    lifetime_imps = Field(name="lifetime_imps", source_field_name="lifetime_imps", fields=["lifetime_imps"], type_id=FieldType.structure)

    lifetime_spend_cap = Field(name="lifetime_spend_cap", source_field_name="lifetime_spend_cap", fields=["lifetime_spend_cap"], type_id=FieldType.structure)

    optimization_goal = Field(name="optimization_goal", source_field_name="optimization_goal", fields=["optimization_goal"], type_id=FieldType.structure)

    optimization_sub_event = Field(name="optimization_sub_event", source_field_name="optimization_sub_event", fields=["optimization_sub_event"], type_id=FieldType.structure)

    source_adset = Field(name="source_adset", source_field_name="source_adset", fields=["source_adset"], type_id=FieldType.structure)

    source_adset_id = Field(name="source_adset_id", source_field_name="source_adset_id", fields=["source_adset_id"], type_id=FieldType.structure)

    targeting = Field(name="targeting", source_field_name="targeting", fields=["targeting"], type_id=FieldType.structure)

    time_based_ad_rotation_id_blocks = Field(name="time_based_ad_rotation_id_blocks", source_field_name="time_based_ad_rotation_id_blocks", fields=["time_based_ad_rotation_id_blocks"],
                                             type_id=FieldType.structure)

    time_based_ad_rotation_intervals = Field(name="time_based_ad_rotation_intervals", source_field_name="time_based_ad_rotation_intervals", fields=["time_based_ad_rotation_intervals"],
                                             type_id=FieldType.structure)

    use_new_app_click = Field(name="use_new_app_click", source_field_name="use_new_app_click", fields=["use_new_app_click"], type_id=FieldType.structure)

    lifetime_min_spend_target = Field(name="lifetime_min_spend_target", source_field_name="lifetime_min_spend_target", fields=["lifetime_min_spend_target"], type_id=FieldType.structure)

    targeting_sentence_lines = Field(name="targetingsentencelines", source_field_name="targetingsentencelines", fields=["targetingsentencelines"], type_id=FieldType.structure)

    daily_spend_cap = Field(name="daily_spend_cap", source_field_name="daily_spend_cap", fields=["daily_spend_cap"], type_id=FieldType.structure)

    adset = Field(name="adset", source_field_name="adset", fields=["adset"], type_id=FieldType.structure)

    creative = Field(name="creative", source_field_name="creative", fields=["creative"], type_id=FieldType.structure)

    last_updated_by_app_id = Field(name="last_updated_by_app_id", source_field_name="last_updated_by_app_id", fields=["last_updated_by_app_id"], type_id=FieldType.structure)

    source_ad = Field(name="source_ad", source_field_name="source_ad", fields=["source_ad"], type_id=FieldType.structure)

    source_ad_id = Field(name="source_ad_id", source_field_name="source_ad_id", fields=["source_ad_id"], type_id=FieldType.structure)

    tracking_specs = Field(name="tracking_specs", source_field_name="tracking_specs", fields=["tracking_specs"], type_id=FieldType.structure)

    ad_creatives = Field(name="ad_creative", source_field_name="adcreatives", fields=[ad_creatives_field_definition], type_id=FieldType.structure)

    campaign_structure_name = Field(name="campaign_name", source_field_name="campaign_name", fields=["campaign_name"], type_id=FieldType.structure)

    campaign_structure_id = Field(name="campaign_id", source_field_name="campaign_id", fields=["campaign_id"], type_id=FieldType.structure)

    ad_set_structure_name = Field(name="adset_name", source_field_name="adset_name", fields=["adset_name"], type_id=FieldType.structure)

    ad_set_structure_id = Field(name="adset_id", source_field_name="adset_id", fields=["adset_id"], type_id=FieldType.structure)

    ad_account_structure_id = Field(name="account_id", source_field_name="account_id", fields=["account_id"], type_id=FieldType.structure)

    objective_structure = Field(name="objective", source_field_name="objective", fields=["objective"], type_id=FieldType.structure)

    account_structure_name = Field(name="account_name", source_field_name="account_name", fields=["account_name"], type_id=FieldType.structure)

    # Targeting

    location = Field(name="location", source_field_name="location", fields=["location"], type_id=FieldType.structure)

    age = Field(name="age", source_field_name="age", fields=["age"], type_id=FieldType.structure)

    gender = Field(name="gender", source_field_name="gender", fields=["gender"], type_id=FieldType.structure)

    included_custom_audiences = Field(name="included_custom_audiences", source_field_name="included_custom_audiences", fields=["included_custom_audiences"], type_id=FieldType.structure)

    excluded_custom_audiences = Field(name="excluded_custom_audiences", source_field_name="excluded_custom_audiences", fields=["excluded_custom_audiences"], type_id=FieldType.structure)

    # Ad creative

    page_name = Field(name="page_name", source_field_name="page_name", fields=["page_name"], type_id=FieldType.structure)

    headline = Field(name="headline", source_field_name="headline", fields=["headline"], type_id=FieldType.structure)

    body = Field(name="body", source_field_name="body", fields=["body"], type_id=FieldType.structure)

    link = Field(name="link", source_field_name="link", fields=["link"], type_id=FieldType.structure)

    destination = Field(name="destination", source_field_name="destination", fields=["destination"], type_id=FieldType.structure)

    # Tracking
    url_parameters = Field(name="url_parameters", source_field_name="url_parameters", fields=["url_parameters"], type_id=FieldType.structure)

    pixel = Field(name="pixel", source_field_name="pixel", fields=["pixel"], type_id=FieldType.structure)

    app_event = Field(name="app_event", source_field_name="app_event", fields=["app_event"], type_id=FieldType.structure)

    offline_event = Field(name="offline_event", source_field_name="offline_event", fields=["offline_event"], type_id=FieldType.structure)

    # ====== PERFORMANCE ====== #

    # TODO: add from above
    reach = Field(name="reach", source_field_name="reach", fields=["reach"], type_id=FieldType.simple)

    frequency = Field(name="frequency", source_field_name="frequency", fields=["frequency"], type_id=FieldType.simple)

    impressions = Field(name="impressions", source_field_name="impressions", fields=["impressions"], type_id=FieldType.simple)

    # structure columns
    status = Field(name="status", source_field_name="effective_status", fields=["effective_status"], type_id=FieldType.structure)

    delivery = Field(name="delivery", source_field_name="effective_status", fields=["effective_status"], type_id=FieldType.structure)

    ad_set_delivery = Field(name="adset_delivery", source_field_name="effective_status", fields=["adset", "effective_status"], type_id=FieldType.structure)

    amount_spent = Field(name="amount_spent", source_field_name="spend", fields=["spend"], type_id=FieldType.simple)

    social_spend = Field(name="social_spend", source_field_name="social_spend", fields=["social_spend"], type_id=FieldType.simple)

    all_clicks = Field(name="clicks_all", source_field_name="clicks", fields=["clicks"], type_id=FieldType.simple)

    all_cpc = Field(name="cpc_all", source_field_name="cpc", fields=["cpc"], type_id=FieldType.simple)

    all_ctr = Field(name="ctr_all", source_field_name="ctr", fields=["ctr"], type_id=FieldType.simple)

    all_cpp = Field(name="cpp_all", source_field_name="cpp", fields=["cpp"], type_id=FieldType.simple)

    # impressions_gross TODO: FIND OUT WHERE FB GETS THIS INFO FROM

    #  impressions_auto_refresh TODO: FIND OUT WHERE FB GETS THIS INFO FROM

    # ad relevance columns
    quality_ranking = Field(name="quality_ranking", source_field_name="quality_rankingt", fields=["quality_ranking"], type_id=FieldType.simple)

    engagement_rate_ranking = Field(name="engagement_rate_ranking", source_field_name="engagement_rate_ranking", fields=["engagement_rate_ranking"], type_id=FieldType.simple)

    conversion_rate_ranking = Field(name="conversion_rate_ranking", source_field_name="conversion_rate_ranking", fields=["conversion_rate_ranking"], type_id=FieldType.simple)

    # cost
    # cost per result
    # TODO: ADD FROM ABOVE

    # cost per 1000 people reached
    #  TODO: ADD FROM ABOVE

    cpm = Field(name="cpm", source_field_name="cpm", fields=["cpm"], type_id=FieldType.simple)

    # ====== ENGAGEMENT ====== #
    # Page post

    page_engagement = Field(name="page_engagement", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="page_engagement",
                            action_field_name_key="action_type", type_id=FieldType.nested)

    page_like = Field(name="page_like", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="like",
                      action_field_name_key="action_type", type_id=FieldType.nested)

    post_comment = Field(name="post_comment", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="comment",
                         action_field_name_key="action_type", type_id=FieldType.nested)

    post_engagement = Field(name="post_engagement", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="post_engagement",
                            action_field_name_key="action_type", type_id=FieldType.nested)

    #  TODO: Check this on FB
    post_reaction = Field(name="post_reaction", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="post_reaction",
                          action_field_name_key="action_type", type_id=FieldType.nested)

    post_save = Field(name="post_save", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="onsite_conversion.post_save",
                      action_field_name_key="action_type", type_id=FieldType.nested)

    post_share = Field(name="post_share", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="post",
                       action_field_name_key="action_type", type_id=FieldType.nested)

    photo_view = Field(name="post_view", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="photo_view",
                       action_field_name_key="action_type", type_id=FieldType.nested)

    event_responses = Field(name="event_responses", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_value="rsvp",
                            action_field_name_key="action_type", type_id=FieldType.nested)

    # checkins
    # TODO: FIND OUT WHERE FB GETS THIS INFO

    full_view_impressions = Field(name="full_view_impressions", source_field_name="full_view_impressions", fields=["full_view_impressions"], type_id=FieldType.simple)

    full_view_reach = Field(name="full_view_reach", source_field_name="full_view_reach", fields=["full_view_reach"], type_id=FieldType.simple)

    # effect share
    # TODO: FIND OUT WHERE FB GETS THIS INFO

    # cost page and post

    cost_per_page_engagement = Field(name="cost_per_page_engagement", source_field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"],
                                     action_field_name_key="action_type", action_field_name_value="page_engagement", type_id=FieldType.nested)

    cost_per_page_like = Field(name="cost_per_page_like", source_field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"],
                               action_field_name_key="action_type", action_field_name_value="like", type_id=FieldType.nested)

    cost_per_post_engagement = Field(name="cost_per_post_engagement", source_field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"],
                                     action_field_name_key="action_type", action_field_name_value="post_engagement", type_id=FieldType.nested)

    cost_per_event_response = Field(name="cost_per_event_response", source_field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"],
                                    action_field_name_key="action_type", action_field_name_value="rsvp", type_id=FieldType.nested)

    # messaging
    new_messaging_connections = Field(name="new_messaging_connections", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"],
                                      action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_first_reply", type_id=FieldType.nested)

    messaging_conversation_started7d = Field(name="messaging_conversation_started_7d", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"],
                                             action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_conversation_started.7d", type_id=FieldType.nested)

    blocked_messaging_connections = Field(name="blocked_messaging_connections", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"],
                                          action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_block", type_id=FieldType.nested)

    #  cost per messaging
    cost_per_new_messaging_connection = Field(name="cost_per_new_messaging_connection", source_field_name="cost_per_action_type", fields=["cost_per_action_type"],
                                              action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="onsite_conversion.messaging_first_reply",
                                              type_id=FieldType.nested)

    # media
    video_play = Field(name="video_play", source_field_name="video_play_actions", fields=["video_play_actions"], action_breakdowns=["action_type"], action_field_name_key="action_type",
                       action_field_name_value="video_view", type_id=FieldType.nested)

    thru_play = Field(name="thruplay", source_field_name="video_thruplay_watched_actions", fields=["video_thruplay_watched_actions"], action_breakdowns=["action_type"],
                      action_field_name_key="action_type", action_field_name_value="video_view", type_id=FieldType.nested)

    unique_two_seconds_continuous_video_play = Field(name="unique_two_second_continuous_video_play", source_field_name="unique_actions", fields=["unique_actions"],
                                                     action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", type_id=FieldType.nested)

    two_seconds_continuous_video_play = Field(name="two_second_continuous_video_play", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"],
                                              action_field_name_key="action_type", action_field_name_value="video_view", type_id=FieldType.nested)

    total_video25_p_watched_actions = Field(name="total_video_25p_watched_actions", source_field_name="video_p25_watched_actions", fields=["video_p25_watched_actions"],
                                            action_breakdowns=["action_video_type"], action_field_name_value="total", type_id=FieldType.nested)

    click_to_play_video25_p_watched_actions = Field(name="click_to_play_video_25p_watched_actions", source_field_name="video_p25_watched_actions", fields=["video_p25_watched_actions"],
                                                    action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", type_id=FieldType.nested)

    auto_play_video25_p_watched_actions = Field(name="auto_play_video_25p_watched_actions", source_field_name="video_p25_watched_actions", fields=["video_p25_watched_actions"],
                                                action_breakdowns=["action_video_type"], action_field_name_value="auto_play", type_id=FieldType.nested)

    total_video50_p_watched_actions = Field(name="total_video_50p_watched_actions", source_field_name="video_p50_watched_actions", fields=["video_p50_watched_actions"],
                                            action_breakdowns=["action_video_type"], action_field_name_value="total", type_id=FieldType.nested)

    click_to_play_video50_p_watched_actions = Field(name="click_to_play_video_50p_watched_actions", source_field_name="video_p50_watched_actions", fields=["video_p50_watched_actions"],
                                                    action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", type_id=FieldType.nested)

    auto_play_video50_p_watched_actions = Field(name="auto_play_video_50p_watched_actions", source_field_name="video_p50_watched_actions", fields=["video_p50_watched_actions"],
                                                action_breakdowns=["action_video_type"], action_field_name_value="auto_play", type_id=FieldType.nested)

    total_video75_p_watched_actions = Field(name="total_video_75p_watched_actions", source_field_name="video_p75_watched_actions", fields=["video_p75_watched_actions"],
                                            action_breakdowns=["action_video_type"], action_field_name_value="total", type_id=FieldType.nested)

    click_to_play_video75_p_watched_actions = Field(name="click_to_play_video_75p_watched_actions", source_field_name="video_p75_watched_actions", fields=["video_p75_watched_actions"],
                                                    action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", type_id=FieldType.nested)

    auto_play_video75_p_watched_actions = Field(name="auto_play_video_75p_watched_actions", source_field_name="video_p75_watched_actions", fields=["video_p75_watched_actions"],
                                                action_breakdowns=["action_video_type"], action_field_name_value="auto_play", type_id=FieldType.nested)

    total_video95_p_watched_actions = Field(name="total_video_95p_watched_actions", source_field_name="video_p95_watched_actions", fields=["video_p95_watched_actions"],
                                            action_breakdowns=["action_video_type"], action_field_name_value="total", type_id=FieldType.nested)

    click_to_play_video95_p_watched_actions = Field(name="click_to_play_video_95p_watched_actions", source_field_name="video_p95_watched_actions", fields=["video_p95_watched_actions"],
                                                    action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", type_id=FieldType.nested)

    auto_play_video95_p_watched_actions = Field(name="auto_play_video_95p_watched_actions", source_field_name="video_p95_watched_actions", fields=["video_p95_watched_actions"],
                                                action_breakdowns=["action_video_type"], action_field_name_value="auto_play", type_id=FieldType.nested)

    total_video100_p_watched_actions = Field(name="total_video_100p_watched_actions", source_field_name="video_p100_watched_actions", fields=["video_p100_watched_actions"],
                                             action_breakdowns=["action_video_type"], action_field_name_value="total", type_id=FieldType.nested)

    click_to_play_video100_p_watched_actions = Field(name="click_to_play_video_100p_watched_actions", source_field_name="video_p100_watched_actions", fields=["video_p100_watched_actions"],
                                                     action_breakdowns=["action_video_type"], action_field_name_value="click_to_play", type_id=FieldType.nested)

    auto_play_video100_p_watched_actions = Field(name="auto_play_video_100p_watched_actions", source_field_name="video_p100_watched_actions", fields=["video_p100_watched_actions"],
                                                 action_breakdowns=["action_video_type"], action_field_name_value="auto_play", type_id=FieldType.nested)

    instant_experience_view_time = Field(name="canvas_avg_view_time", source_field_name="canvas_avg_view_time", fields=["canvas_avg_view_time"], type_id=FieldType.simple)

    instant_experience_view_percentage = Field(name="canvas_avg_view_percent", source_field_name="canvas_avg_view_percent", fields=["canvas_avg_view_percent"], type_id=FieldType.simple)

    # cost media
    cost_per_two_seconds_continuous_video_play = Field(name="cost_per_two_second_continuous_video_play", source_field_name="cost_per_action_type", fields=["cost_per_action_type"],
                                                       action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="video_view", type_id=FieldType.nested)

    cost_per_thruplay = Field(name="cost_per_thruplay_video_play", source_field_name="cost_per_thruplay", fields=["cost_per_thruplay"], action_breakdowns=["action_type"],
                              action_field_name_key="action_type", action_field_name_value="video_view", type_id=FieldType.nested)

    #  clicks

    link_click = Field(name="link_click", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type",
                       action_field_name_value="link_click", type_id=FieldType.nested)

    unique_link_click = Field(name="unique_link_click", source_field_name="unique_actions", fields=["unique_actions"], action_breakdowns=["action_type"], action_field_name_key="action_type",
                              action_field_name_value="link_click", type_id=FieldType.nested)

    outbound_click = Field(name="outbound_clicks", source_field_name="outbound_clicks", fields=["outbound_clicks"], action_breakdowns=["action_type"], action_field_name_key="action_type",
                           action_field_name_value="outbound_click", type_id=FieldType.nested)

    unique_outbound_click = Field(name="unique_outbound_clicks", source_field_name="unique_outbound_clicks", fields=["unique_outbound_clicks"], action_breakdowns=["action_type"],
                                  action_field_name_key="action_type", action_field_name_value="outbound_click", type_id=FieldType.nested)

    link_click_ctr = Field(name="link_click_ctr", source_field_name="website_ctr", fields=["website_ctr"], action_breakdowns=["action_type"], action_field_name_key="action_type",
                           action_field_name_value="link_click", type_id=FieldType.nested)

    unique_link_click_ctr = Field(name="unique_link_clicks_ctr", source_field_name="unique_link_clicks_ctr", fields=["unique_link_clicks_ctr"], type_id=FieldType.simple)

    outbound_link_click_ctr = Field(name="outbound_clicks_ctr", source_field_name="outbound_clicks_ctr", fields=["outbound_clicks_ctr"], action_breakdowns=["action_type"],
                                    action_field_name_key="action_type", action_field_name_value="outbound_click", type_id=FieldType.nested)

    unique_outbound_link_click_ctr = Field(name="unique_outbound_clicks_ctr", source_field_name="unique_outbound_clicks_ctr", fields=["unique_outbound_clicks_ctr"],
                                           action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", type_id=FieldType.nested)

    unique_click = Field(name="unique_clicks", source_field_name="unique_clicks", fields=["unique_clicks"], type_id=FieldType.simple)

    unique_ctr = Field(name="unique_ctr", source_field_name="unique_ctr", fields=["unique_ctr"], type_id=FieldType.simple)

    instant_experience_click_to_open = Field(name="instant_experience_clicks_to_open", source_field_name="instant_experience_clicks_to_open", fields=["instant_experience_clicks_to_open"],
                                             type_id=FieldType.simple)

    instant_experience_click_to_start = Field(name="instant_experience_clicks_to_start", source_field_name="instant_experience_clicks_to_start",
                                              fields=["instant_experience_clicks_to_start"], type_id=FieldType.simple)

    instant_experience_outbound_click = Field(name="instant_experience_outbound_clicks", source_field_name="instant_experience_outbound_clicks",
                                              fields=["instant_experience_outbound_clicks"], type_id=FieldType.simple)

    # cost clicks
    cost_per_link_click = Field(name="cost_per_link_click", source_field_name="cost_per_action_type", fields=["cost_per_action_type"], action_breakdowns=["action_type"],
                                action_field_name_key="action_type", action_field_name_value="link_click", type_id=FieldType.nested)

    cost_per_unique_link_click = Field(name="cost_per_unique_link_click", source_field_name="cost_per_unique_action_type", fields=["cost_per_unique_action_type"],
                                       action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="link_click", type_id=FieldType.nested)

    cost_per_outbound_link_click = Field(name="cost_per_outbound_click", source_field_name="cost_per_outbound_click", fields=["cost_per_outbound_click"], action_breakdowns=["action_type"],
                                         action_field_name_key="action_type", action_field_name_value="outbound_click", type_id=FieldType.nested)

    cost_per_unique_outbound_link_click = Field(name="cost_per_unique_outbound_click", source_field_name="cost_per_unique_outbound_click", fields=["cost_per_unique_outbound_click"],
                                                action_breakdowns=["action_type"], action_field_name_key="action_type", action_field_name_value="outbound_click", type_id=FieldType.nested)

    cost_per_unique_click_all = Field(name="cost_per_unique_click", source_field_name="cost_per_unique_click", fields=["cost_per_unique_click"], type_id=FieldType.simple)

    # awareness
    estimated_ad_recall_lift = Field(name="estimated_ad_recallers", source_field_name="estimated_ad_recallers", fields=["estimated_ad_recallers"], type_id=FieldType.simple)

    estimated_ad_recall_rate = Field(name="estimated_ad_recall_rate", source_field_name="estimated_ad_recall_rate", fields=["estimated_ad_recall_rate"], type_id=FieldType.simple)

    cost_per_estimated_ad_recall_lift = Field(name="cost_per_estimated_ad_recallers", source_field_name="cost_per_estimated_ad_recallers", fields=["cost_per_estimated_ad_recallers"],
                                              type_id=FieldType.simple)

    # ======= breakdowns ====== #

    # delivery
    age_breakdown = Field(name="age_breakdown", source_field_name="age", breakdowns=["age"], type_id=FieldType.breakdown)

    gender_breakdown = Field(name="gender_breakdown", source_field_name="gender", breakdowns=["gender"], type_id=FieldType.breakdown)

    country = Field(name="country", source_field_name="country", breakdowns=["country"], type_id=FieldType.breakdown)

    dma = Field(name="dma", source_field_name="dma", breakdowns=["dma"], type_id=FieldType.breakdown)

    impression_device = Field(name="impression_device", source_field_name="impression_device", breakdowns=["impression_device"], type_id=FieldType.breakdown)

    publisher_platform = Field(name="publisher_platform", source_field_name="publisher_platform", breakdowns=["publisher_platform"], type_id=FieldType.breakdown)

    placement = Field(name="placement", source_field_name=["publisher_platform", "platform_position", "device_platform"],
                      breakdowns=["publisher_platform", "platform_position", "device_platform"], type_id=FieldType.breakdown)

    product_id = Field(name="product_id", source_field_name="product_id", breakdowns=["product_id"], type_id=FieldType.breakdown)

    frequency_value = Field(name="frequency_value", source_field_name="frequency_value", breakdowns=["frequency_value"], type_id=FieldType.breakdown)

    hourly_stats_aggregated_by_advertiser_time_zone = Field(name="hourly_stats_aggregated_by_advertiser_time_zone", source_field_name="hourly_stats_aggregated_by_advertiser_time_zone",
                                                            breakdowns=["hourly_stats_aggregated_by_advertiser_time_zone"], type_id=FieldType.breakdown)

    hourly_stats_aggregated_by_audience_time_zone = Field(name="hourly_stats_aggregated_by_audience_time_zone", source_field_name="hourly_stats_aggregated_by_audience_time_zone",
                                                          breakdowns=["hourly_stats_aggregated_by_audience_time_zone"], type_id=FieldType.breakdown)

    business_locations = Field(name="place_page_id", source_field_name="place_page_id", breakdowns=["place_page_id"], type_id=FieldType.breakdown)

    platform_position = Field(name="platform_position", source_field_name="platform_position", breakdowns=["platform_position"], type_id=FieldType.breakdown)

    device_platform = Field(name="device_platform", source_field_name="device_platform", breakdowns=["device_platform"], type_id=FieldType.breakdown)

    age_gender = Field(name="age_gender", source_field_name=["age", "gender"], breakdowns=["age", "gender"], type_id=FieldType.breakdown)

    platform_and_device = Field(name="platform_and_device", source_field_name=["publisher_platform", "impression_device"], breakdowns=["publisher_platform", "impression_device"],
                                type_id=FieldType.breakdown)

    placement_and_device = Field(name="placement_and_device", source_field_name=["publisher_platform", "platform_position", "device_platform", "impression_device"],
                                 breakdowns=["publisher_platform", "platform_position", "device_platform", "impression_device"], type_id=FieldType.breakdown)

    region = Field(name="region", source_field_name="region", breakdowns=["region"], type_id=FieldType.breakdown)

    # action breakdowns # TODO: DEFINE THEM PROPERLY
    device = Field(name="action_device", action_breakdowns=["action_device"], action_field_name_key="action_device", type_id=FieldType.action_breakdown)

    canvas_component = Field(name="action_canvas_component_name", action_breakdowns=["action_canvas_component_name"], action_field_name_key="action_canvas_component_name",
                             type_id=FieldType.action_breakdown)

    carouse_card_id = Field(name="action_carousel_card_id", action_breakdowns=["action_carousel_card_id"], action_field_name_key="action_carousel_card_id",
                            type_id=FieldType.action_breakdown)

    carouse_card_name = Field(name="action_carousel_card_name", action_breakdowns=["action_carousel_card_name"], action_field_name_key="action_carousel_card_name",
                              type_id=FieldType.action_breakdown)

    destination_breakdown = Field(name="action_destination", action_breakdowns=["action_destination"], action_field_name_key="action_destination", type_id=FieldType.action_breakdown)

    reaction = Field(name="action_reaction", action_breakdowns=["action_reaction"], action_field_name_key="action_reaction", type_id=FieldType.action_breakdown)

    target = Field(name="action_target_id", action_breakdowns=["action_target_id"], action_field_name_key="action_target_id", type_id=FieldType.action_breakdown)

    video_sound = Field(name="action_video_sound", action_breakdowns=["action_video_sound"], action_field_name_key="action_video_sound", type_id=FieldType.action_breakdown)

    video_type = Field(name="action_video_type", action_breakdowns=["action_video_type"], action_field_name_key="action_video_type", type_id=FieldType.action_breakdown)

    # time
    day = Field(name="day", source_field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value=1, type_id=FieldType.time_breakdown)

    week = Field(name="week", source_field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value=7, type_id=FieldType.time_breakdown)

    two_weeks = Field(name="two_weeks", source_field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value=14, type_id=FieldType.time_breakdown)

    monthly = Field(name="monthly", source_field_name=["date_start", "date_stop"], fields=["date_start", "date_stop"], action_field_name_value="monthly", type_id=FieldType.time_breakdown)

    #  ====== Custom columns ====== #
    results = Field(name="results", source_field_name="actions", fields=["actions", "objective"], action_breakdowns=["action_type"], action_field_name_key="action_type",
                    type_id=FieldType.total)

    cost_per_result = Field(name="cost_per_result", source_field_name="actions", fields=["actions", "objective", "spend"], action_breakdowns=["action_type"],
                            action_field_name_key="action_type", type_id=FieldType.cost)

    conversions = Field(name="conversions", source_field_name="actions", fields=["actions"], action_breakdowns=["action_type"], action_field_name_key="action_type",
                        action_field_name_value="conversion", type_id=FieldType.total)

    cost_per_conversion = Field(name="cost_per_conversion", source_field_name="actions", fields=["actions", "spend"], action_breakdowns=["action_type"], action_field_name_key="action_type",
                                action_field_name_value="conversion", type_id=FieldType.cost)

    cost_per1000_people_reached = Field("cost_per_1000_people_reached", source_field_name="reach", fields=["reach", "spend"], type_id=FieldType.cost)
