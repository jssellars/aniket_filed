# todo: clean up this list after complete metrics refactoring


class GraphAPIInsightsFields:
    #  ====== MISC ====== #
    since = "since"
    until = "until"

    #  ====== BREAKDOWNS ====== #
    age = "age"
    gender = "gender"
    country = "country"
    dma = "dma"
    region = "region"
    impression_device = "impression_device"
    publisher_platform = "publisher_platform"
    platform_position = "platform_position"
    device_platform = "device_platform"
    product_id = "product_id"
    frequency_value = "frequency_value"
    hourly_stats_aggregated_by_advertiser_time_zone = "hourly_stats_aggregated_by_advertiser_time_zone"
    hourly_stats_aggregated_by_audience_time_zone = "hourly_stats_aggregated_by_audience_time_zone"
    place_page_id = "place_page_id"

    # ====== ACTION BREAKDOWNS ====== #
    action_type = "action_type"
    action_device = "action_device"
    action_canvas_component_name = "action_canvas_component_name"
    action_carousel_card_id = "action_carousel_card_id"
    action_carousel_card_name = "action_carousel_card_name"
    action_destination = "action_destination"
    action_reaction = "action_reaction"
    action_target_id = "action_target_id"
    action_video_sound = "action_video_sound"
    action_video_type = "action_video_type"

    # ====== INSIGHTS ====== #
    date_start = "date_start"
    date_stop = "date_stop"
    account_id = "account_id"
    account_name = "account_name"
    ad_id = "ad_id"
    ad_name = "ad_name"
    adset_id = "adset_id"
    adset_name = "adset_name"
    campaign_id = "campaign_id"
    campaign_name = "campaign_name"
    objective = "objective"
    full_view_impressions = "full_view_impressions"
    full_view_reach = "full_view_reach"
    social_spend = "social_spend"
    cost_per_estimated_ad_recall_lift = "cost_per_estimated_ad_recall_lift"
    estimated_ad_recall_rate = "estimated_ad_recall_rate"
    estimated_ad_recallers = "estimated_ad_recallers"
    cost_per_unique_click = "cost_per_unique_click"
    canvas_avg_view_time = "canvas_avg_view_time"
    canvas_avg_view_percent = "canvas_avg_view_percent"
    unique_link_clicks_ctr = "unique_link_clicks_ctr"
    unique_clicks = "unique_clicks"
    unique_ctr = "unique_ctr"
    instant_experience_clicks_to_open = "instant_experience_clicks_to_open"
    instant_experience_clicks_to_start = "instant_experience_clicks_to_start"
    instant_experience_outbound_clicks = "instant_experience_outbound_clicks"
    conversion_rate_ranking = "conversion_rate_ranking"
    reach = "reach"
    frequency = "frequency"
    impressions = "impressions"
    spend = "spend"
    clicks = "clicks"
    cpc = "cpc"
    ctr = "ctr"
    impressions_gross = "impressions_gross"
    impressions_auto_refresh = "impressions_auto_refresh"
    quality_ranking = "quality_ranking"
    engagement_rate_ranking = "engagement_rate_ranking"
    cpp = "cpp"
    cpm = "cpm"

    # ====== ACTION INSIGHTS ====== #
    actions = "actions"
    action_device_other = "other"
    action_device_web = "desktop"
    action_device_iphone = "iphone"
    action_device_ipad = "ipad"
    action_device_ipod = "ipod"
    action_device_android = "android"
    action_device_smartphone = "smartphone"
    action_device_tablet = "tablet"
    action_device_offline = "offline"
    page_engagement = "page_engagement"
    page_like = "like"
    post_comment = "comment"
    post_engagement = "post_engagement"
    post_reaction = "post_reaction"
    post_saves = "onsite_conversion.post_save"
    post_shares = "post"
    photo_views = "post_view"
    post_likes = "like"
    event_responses = "rsvp"
    checkins = "checkin"
    cost_per_action_type = "cost_per_action_type"
    new_messaging_connections = "onsite_conversion.messaging_first_reply"
    blocked_messaging_connections = "onsite_conversion.messaging_block"
    messaging_conversation_started_7d = "onsite_conversion.messaging_conversation_started_7d"
    unique_actions = "unique_actions"
    video_view = "video_view"
    thru_plays = "video_thruplay_watched_actions"
    video_p25_watched_actions = "video_p25_watched_actions"
    video_p50_watched_actions = "video_p50_watched_actions"
    video_p75_watched_actions = "video_p75_watched_actions"
    video_p95_watched_actions = "video_p95_watched_actions"
    video_p100_watched_actions = "video_p100_watched_actions"
    video_view_total = "total"
    video_avg_time_watched_actions = "video_avg_time_watched_actions"
    video_play_actions = "video_play_actions"
    cost_per_thruplay = "cost_per_thruplay"
    link_click = "link_click"
    inline_link_click = "inline_link_clicks"
    inline_link_click_ctr = "inline_link_click_ctr"
    unique_inline_link_click = "unique_inline_link_clicks"
    unique_inline_link_click_ctr = "unique_inline_link_click_ctr"
    cost_per_inline_link_click = "cost_per_inline_link_click"
    cost_per_unique_inline_link_click = "cost_per_unique_inline_link_click"
    inline_post_engagement = "inline_post_engagements"
    cost_per_inline_post_engagement = "cost_per_inline_post_engagement"
    outbound_clicks = "outbound_clicks"
    outbound_click = "outbound_click"
    unique_outbound_clicks = "unique_outbound_clicks"
    website_ctr = "website_ctr"
    outbound_clicks_ctr = "outbound_clicks_ctr"
    unique_outbound_clicks_ctr = "unique_outbound_clicks_ctr"
    cost_per_unique_action_type = "cost_per_unique_action_type"
    cost_per_outbound_click = "cost_per_outbound_click"
    cost_per_unique_outbound_click = "cost_per_unique_outbound_click"
    website_purchase_roas = "offsite_conversion."
    omni_purchase = "omni_purchase"
    purchase_roas = "purchase_roas"
    results = "results"
    conversions = "offsite_conversion.fb_pixel_purchase"
    product_catalog_sales = "omni_purchase"  # "offsite_conversion.fb_pixel_purchase:catalog_sales"
    value = "value"
    video_auto_play = "auto_play"
    video_click_to_play = "click_to_play"
    action_values = "action_values"
    mobile_achievement_unlocked = "app_custom_event.fb_mobile_achievement_unlocked"
    app_adds_of_payment_info = "offsite_conversion.fb_pixel_add_payment_info"
    adds_to_wish_list = "offsite_conversion.fb_pixel_add_to_wishlist"
    adds_to_cart = "offsite_conversion.fb_pixel_add_to_cart"
    app_activations = "app_custom_event.fb_mobile_activate_app"
    app_installs = "app_install"
    mobile_app_checkouts_initiated = "app_custom_event.fb_mobile_initiated_checkout"
    website_checkouts_initiated = "offsite_conversion.fb_pixel_initiate_checkout"
    mobile_app_content_views = "app_custom_event.fb_mobile_content_view"
    website_content_views = "offsite_conversion.fb_pixel_view_content"
    content_views = "view_content"
    credit_spends = "credit_spent"
    custom_events = "offsite_conversion.fb_pixel_custom"
    desktop_app_engagements = "app_engagement"
    desktop_app_story_engagements = "app_story"
    desktop_app_uses = "app_use"
    game_plays = "game_plays"
    landing_page_views = "landing_page_view"
    leads = "lead"
    website_leads = "offsite_conversion.fb_pixel_lead"
    on_facebook_leads = "onsite_conversion.lead_grouped"
    on_facebook_workflow_completions = "onsite_conversion.flow_complete"
    mobile_app_purchase_roas = "mobile_app_roas"
    website_purchases = "offsite_conversion.fb_pixel_purchase"
    purchases = "purchase"
    on_facebook_purchases = "onsite_conversion.purchase"
    registrations_completed = "complete_registration"
    mobile_app_registrations_completed = "app_custom_event.fb_mobile_complete_registration"
    website_registrations_completed = "offsite_conversion.fb_pixel_complete_registration"
    searches = "search"
    website_searches = "offsite_conversion.fb_pixel_search"
    subscriptions = "subscribe"
    tutorials_completed = "omni_tutorial_completed"

    # ====== STRUCTURE ====== #
    name = "name"
    account_status = "account_status"
    business = business_manager = business_id = "business"
    currency = "currency"
    campaign_name_structure = "campaign{name}"
    adset_name_structure = "adset{name}"
    structure_id = "id"
    buying_type = "buying_type"
    effective_status = "effective_status"
    tags = "tags"
    created_time = "created_time"
    last_significant_edit = "last_significant_edit"
    start_time = "start_time"
    stop_time = "stop_time"
    bid_strategy = "bid_strategy"
    amount_spent_percentage = "amount_spent_percentage"
    bid_cap = "bid_cap"
    budget = "budget"
    budget_remaining = "budget_remaining"
    adlabels = "adlabels"
    boosted_object_id = "boosted_object_id"
    brand_lift_studies = "brand_lift_studies"
    budget_rebalance_flag = "budget_rebalance_flag"
    can_create_brand_lift_study = "can_create_brand_lift_study"
    configured_status = "configured_status"
    can_use_spend_cap = "can_use_spend_cap"
    daily_budget = "daily_budget"
    last_budget_toggling_time = "last_budget_toggling_time"
    lifetime_budget = "lifetime_budget"
    pacing_type = "pacing_type"
    recommendations = "recommendations"
    promoted_object = "promoted_object"
    custom_event_type = "custom_event_type"
    source_campaign = "source_campaign"
    special_ad_category = "special_ad_category"
    source_campaign_id = "source_campaign_id"
    spend_cap = "spend_cap"
    topline_id = "topline_id"
    adrules_governed = "adrules_governed"
    updated_time = "updated_time"
    copies = "copies"
    adset_schedule = "adset_schedule"
    asset_feed_id = "asset_feed_id"
    attribution_spec = "attribution_spec"
    bid_adjustments = "bid_adjustments"
    bid_constraints = "bid_constraints"
    bid_amount = "bid_amount"
    bid_info = "bid_info"
    billing_event = "billing_event"
    campaign = "campaign"
    daily_min_spend_target = "daily_min_spend_target"
    destination_type = "destination_type"
    end_time = "end_time"
    frequency_control_specs = "frequency_control_specs"
    instagram_actor_id = "instagram_actor_id"
    is_dynamic_creative = "is_dynamic_creative"
    issues_info = "issues_info"
    lifetime_imps = "lifetime_imps"
    lifetime_spend_cap = "lifetime_spend_cap"
    optimization_goal = "optimization_goal"
    optimization_sub_event = "optimization_sub_event"
    source_adset = "source_adset"
    source_adset_id = "source_adset_id"
    targeting = "targeting"
    time_based_ad_rotation_id_blocks = "time_based_ad_rotation_id_blocks"
    time_based_ad_rotation_intervals = "time_based_ad_rotation_intervals"
    use_new_app_click = "use_new_app_click"
    lifetime_min_spend_target = "lifetime_min_spend_target"
    targetingsentencelines = "targetingsentencelines"
    daily_spend_cap = "daily_spend_cap"
    adset = "adset"
    creative = "creative"
    last_updated_by_app_id = "last_updated_by_app_id"
    source_ad = "source_ad"
    source_ad_id = "source_ad_id"
    tracking_specs = "tracking_specs"
    adcreatives = (
        "adcreatives{account_id,"
        "auto_update,"
        "effective_authorization_category,"
        "enable_launch_instant_app,"
        "link_url,"
        "platform_customizations,"
        "title}"
    )
    adcreatives_fields = (
        "actor_id,"
        "applink_treatment,"
        "asset_feed_spec,"
        "authorization_category,"
        "body,"
        "branded_content_sponsor_page_id,"
        "call_to_action_type,"
        "categorization_criteria,"
        "bundle_folder_id,"
        "category_media_source,"
        "destination_set_id,"
        "effective_instagram_story_id,"
        "dynamic_ad_voice,"
        "effective_object_story_id,"
        "enable_direct_install,"
        "id,"
        "image_crops,"
        "image_hash,"
        "image_url,"
        "instagram_permalink_url,"
        "instagram_story_id,"
        "instagram_actor_id,"
        "interactive_components_spec,"
        "link_deep_link_url,"
        "messenger_sponsored_message,"
        "link_og_id,"
        "name,"
        "object_id,"
        "object_story_id,"
        "object_story_spec,"
        "object_store_url,"
        "object_type,"
        "object_url,"
        "playable_asset_id,"
        "place_page_set_id,"
        "portrait_customizations,"
        "product_set_id,"
        "status,"
        "template_url,"
        "recommender_settings,"
        "thumbnail_url,"
        "url_tags,"
        "use_page_actor_override,"
        "video_id,"
        "template_url_spec"
    )
    status = "status"
    lifetime_spent = "lifetime_spent"
    targeting_sentence_lines_content = "content"
    targeting_sentence_lines_children = "children"
    age_structure = "Age"
    location_structure = "Location"
    gender_structure = "Gender"
    included_custom_audiences_structure = "Including Custom Audiences"
    excluded_custom_audiences_structure = "Excluding Custom Audiences"
    destination = "Placements"
    facebook_pixel_structure = "pixel_id"
    adcreatives_structure = "adcretives"
    data_field = "data"
    headline = "title"
    body = "body"
    link_url = "link_url"
    url_parameters = "url_tags"
    page_id_structure = "page"
    app_event_structure = "application"
    learning_stage_info = "learning_stage_info"

    # ====== MOBILE APP STANDARD EVENTS ====== #
    mobile_app_achievement_unlocked = "app_custom_event.fb_mobile_achievement_unlocked"
    mobile_app_activate_app = "app_custom_event.fb_mobile_activate_app"
    mobile_app_add_payment_info = "app_custom_event.fb_mobile_add_payment_info"
    mobile_app_add_to_cart = "app_custom_event.fb_mobile_add_to_cart"
    mobile_app_add_to_wishlist = "app_custom_event.fb_mobile_add_to_wishlist"
    mobile_app_complete_registration = "app_custom_event.fb_mobile_complete_registration"
    mobile_app_content_view = "app_custom_event.fb_mobile_content_view"
    mobile_app_initiated_checkout = "app_custom_event.fb_mobile_initiated_checkout"
    mobile_app_level_achieved = "app_custom_event.fb_mobile_level_achieved"
    mobile_app_purchases = "app_custom_event.fb_mobile_purchase"
    mobile_app_rating = "app_custom_event.fb_mobile_rate"
    mobile_app_searches = "app_custom_event.fb_mobile_search"
    mobile_app_credit_spends = "app_custom_event.fb_mobile_spent_credits"
    mobile_app_tutorials_completed = "app_custom_event.fb_mobile_tutorial_completion"
    mobile_app_other = "app_custom_event.other"
    mobile_app_install = "mobile_app_install"
    mobile_app_retention = "mobile_app_retention"
    mobile_app_roas = "mobile_app_roas"
