from Core.Metadata.Columns.ColumnMetadata import ColumnMetadata
from Core.Metadata.Columns.ColumnType import ColumnType

from GoogleTuring.Infrastructure.Domain.GoogleAttributeFieldsMetadata import GoogleAttributeFieldsMetadata


class GoogleAttributeMetadataColumnsPool:
    # Structure fields and parameters
    # Object names, IDs, statuses, and dates
    accent_color = ColumnMetadata(GoogleAttributeFieldsMetadata.accent_color.name, ColumnType.text)

    account_currency_code = ColumnMetadata(GoogleAttributeFieldsMetadata.account_currency_code.name,
                                           ColumnType.text)

    account_time_zone = ColumnMetadata(GoogleAttributeFieldsMetadata.account_time_zone.name, ColumnType.text)

    ad_group_status = ColumnMetadata(GoogleAttributeFieldsMetadata.ad_group_status.name, ColumnType.text)

    ad_strength_info = ColumnMetadata(GoogleAttributeFieldsMetadata.ad_strength_info.name, ColumnType.text)

    ad_type = ColumnMetadata(GoogleAttributeFieldsMetadata.ad_type.name, ColumnType.text)

    allow_flexible_color = ColumnMetadata(GoogleAttributeFieldsMetadata.allow_flexible_color.name,
                                          ColumnType.text)

    automated = ColumnMetadata(GoogleAttributeFieldsMetadata.automated.name, ColumnType.text)

    base_ad_group_id = ColumnMetadata(GoogleAttributeFieldsMetadata.base_ad_group_id.name, ColumnType.text)

    base_campaignId = ColumnMetadata(GoogleAttributeFieldsMetadata.base_campaignId.name, ColumnType.text)

    business_name = ColumnMetadata(GoogleAttributeFieldsMetadata.business_name.name, ColumnType.text)

    call_only_phone_number = ColumnMetadata(GoogleAttributeFieldsMetadata.call_only_phone_number.name,
                                            ColumnType.text)

    call_to_action_text = ColumnMetadata(GoogleAttributeFieldsMetadata.call_to_action_text.name, ColumnType.text)

    campaign_id = ColumnMetadata(GoogleAttributeFieldsMetadata.campaign_id.name, ColumnType.text)

    campaign_name = ColumnMetadata(GoogleAttributeFieldsMetadata.campaign_name.name, ColumnType.text)

    campaign_status = ColumnMetadata(GoogleAttributeFieldsMetadata.campaign_status.name, ColumnType.text)

    combined_approval_status = ColumnMetadata(GoogleAttributeFieldsMetadata.combined_approval_status.name,
                                              ColumnType.text)

    conversion_adjustment = ColumnMetadata(GoogleAttributeFieldsMetadata.conversion_adjustment.name,
                                           ColumnType.text)

    creative_destination_url = ColumnMetadata(GoogleAttributeFieldsMetadata.creative_destination_url.name,
                                              ColumnType.text)

    creative_final_app_urls = ColumnMetadata(GoogleAttributeFieldsMetadata.creative_final_app_urls.name,
                                             ColumnType.text)

    creative_final_mobile_urls = ColumnMetadata(GoogleAttributeFieldsMetadata.creative_final_mobile_urls.name,
                                                ColumnType.text)

    creative_final_urls = ColumnMetadata(GoogleAttributeFieldsMetadata.creative_final_urls.name, ColumnType.text)

    creative_final_url_suffix = ColumnMetadata(GoogleAttributeFieldsMetadata.creative_final_url_suffix.name,
                                               ColumnType.text)

    creative_tracking_url_template = ColumnMetadata(
        GoogleAttributeFieldsMetadata.creative_tracking_url_template.name,
        ColumnType.text)

    creative_url_custom_parameters = ColumnMetadata(
        GoogleAttributeFieldsMetadata.creative_url_custom_parameters.name,
        ColumnType.text)

    customer_descriptive_name = ColumnMetadata(GoogleAttributeFieldsMetadata.customer_descriptive_name.name,
                                               ColumnType.text)

    description = ColumnMetadata(GoogleAttributeFieldsMetadata.description.name, ColumnType.text)

    description_1 = ColumnMetadata(GoogleAttributeFieldsMetadata.description_1.name, ColumnType.text)

    description_2 = ColumnMetadata(GoogleAttributeFieldsMetadata.description_2.name, ColumnType.text)

    device_preference = ColumnMetadata(GoogleAttributeFieldsMetadata.device_preference.name, ColumnType.text)

    display_url = ColumnMetadata(GoogleAttributeFieldsMetadata.display_url.name, ColumnType.text)

    enhanced_display_creative_landscape_logo_image_media_id = ColumnMetadata(
        GoogleAttributeFieldsMetadata.enhanced_display_creative_landscape_logo_image_media_id.name,
        ColumnType.text)

    enhanced_display_creative_logo_image_media_id = ColumnMetadata(
        GoogleAttributeFieldsMetadata.enhanced_display_creative_logo_image_media_id.name,
        ColumnType.text)

    enhanced_display_creative_marketing_image_media_id = ColumnMetadata(
        GoogleAttributeFieldsMetadata.enhanced_display_creative_marketing_image_media_id.name,
        ColumnType.text)

    enhanced_display_creative_marketing_image_square_media_id = ColumnMetadata(
        GoogleAttributeFieldsMetadata.enhanced_display_creative_marketing_image_square_media_id.name,
        ColumnType.text)

    expanded_dynamic_search_creative_description_2 = ColumnMetadata(
        GoogleAttributeFieldsMetadata.expanded_dynamic_search_creative_description_2.name,
        ColumnType.text)

    expanded_text_ad_description_2 = ColumnMetadata(
        GoogleAttributeFieldsMetadata.expanded_text_ad_description_2.name,
        ColumnType.text)

    expanded_text_ad_headline_part_3 = ColumnMetadata(
        GoogleAttributeFieldsMetadata.expanded_text_ad_headline_part_3.name,
        ColumnType.text)

    external_customer_id = ColumnMetadata(GoogleAttributeFieldsMetadata.external_customer_id.name,
                                          ColumnType.text)

    format_setting = ColumnMetadata(GoogleAttributeFieldsMetadata.format_setting.name, ColumnType.text)

    gmail_creative_header_image_media_id = ColumnMetadata(
        GoogleAttributeFieldsMetadata.gmail_creative_header_image_media_id.name, ColumnType.text)

    gmail_creative_logo_image_media_id = ColumnMetadata(
        GoogleAttributeFieldsMetadata.gmail_creative_logo_image_media_id.name, ColumnType.text)

    gmail_creative_marketing_image_media_id = ColumnMetadata(
        GoogleAttributeFieldsMetadata.gmail_creative_marketing_image_media_id.name, ColumnType.text)

    gmail_teaser_business_name = ColumnMetadata(GoogleAttributeFieldsMetadata.gmail_teaser_business_name.name,
                                                ColumnType.text)

    gmail_teaser_description = ColumnMetadata(GoogleAttributeFieldsMetadata.gmail_teaser_description.name,
                                              ColumnType.text)

    gmail_teaser_headline = ColumnMetadata(GoogleAttributeFieldsMetadata.gmail_teaser_headline.name,
                                           ColumnType.text)

    headline = ColumnMetadata(GoogleAttributeFieldsMetadata.headline.name, ColumnType.text)

    headline_part_1 = ColumnMetadata(GoogleAttributeFieldsMetadata.headline_part_1.name, ColumnType.text)

    headline_part_2 = ColumnMetadata(GoogleAttributeFieldsMetadata.headline_part_2.name, ColumnType.text)

    id = ColumnMetadata(GoogleAttributeFieldsMetadata.id.name, ColumnType.text)

    ad_id = ColumnMetadata(GoogleAttributeFieldsMetadata.ad_id.name, ColumnType.text)

    image_ad_url = ColumnMetadata(GoogleAttributeFieldsMetadata.image_ad_url.name, ColumnType.text)

    image_creative_image_height = ColumnMetadata(GoogleAttributeFieldsMetadata.image_creative_image_height.name,
                                                 ColumnType.text)

    image_creative_image_width = ColumnMetadata(GoogleAttributeFieldsMetadata.image_creative_image_width.name,
                                                ColumnType.text)

    image_creative_mime_type = ColumnMetadata(GoogleAttributeFieldsMetadata.image_creative_mime_type.name,
                                              ColumnType.text)

    image_creative_name = ColumnMetadata(GoogleAttributeFieldsMetadata.image_creative_name.name, ColumnType.text)

    is_negative = ColumnMetadata(GoogleAttributeFieldsMetadata.is_negative.name, ColumnType.text)

    label_ids = ColumnMetadata(GoogleAttributeFieldsMetadata.label_ids.name, ColumnType.text)

    labels = ColumnMetadata(GoogleAttributeFieldsMetadata.labels.name, ColumnType.text)

    long_headline = ColumnMetadata(GoogleAttributeFieldsMetadata.long_headline.name, ColumnType.text)

    main_color = ColumnMetadata(GoogleAttributeFieldsMetadata.main_color.name, ColumnType.text)

    marketing_image_call_to_action_text = ColumnMetadata(
        GoogleAttributeFieldsMetadata.marketing_image_call_to_action_text.name, ColumnType.text)

    marketing_image_call_to_action_text_color = ColumnMetadata(
        GoogleAttributeFieldsMetadata.marketing_image_call_to_action_text_color.name, ColumnType.text)

    marketing_image_description = ColumnMetadata(GoogleAttributeFieldsMetadata.marketing_image_description.name,
                                                 ColumnType.text)

    marketing_image_headline = ColumnMetadata(GoogleAttributeFieldsMetadata.marketing_image_headline.name,
                                              ColumnType.text)

    multi_asset_responsive_display_ad_accent_color = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_accent_color.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_allow_flexible_color = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_allow_flexible_color.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_business_name = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_business_name.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_call_to_action_text = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_call_to_action_text.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_descriptions = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_descriptions.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_dynamic_settings_price_prefix = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_dynamic_settings_price_prefix.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_dynamic_settings_promo_text = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_dynamic_settings_promo_text.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_format_setting = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_format_setting.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_headlines = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_headlines.name, ColumnType.text)

    multi_asset_responsive_display_ad_landscape_logo_images = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_landscape_logo_images.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_logo_images = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_logo_images.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_long_headline = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_long_headline.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_main_color = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_main_color.name, ColumnType.text)

    multi_asset_responsive_display_ad_marketing_images = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_marketing_images.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_square_marketing_images = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_square_marketing_images.name,
        ColumnType.text)

    multi_asset_responsive_display_ad_you_tube_videos = ColumnMetadata(
        GoogleAttributeFieldsMetadata.multi_asset_responsive_display_ad_you_tube_videos.name,
        ColumnType.text)

    path_1 = ColumnMetadata(GoogleAttributeFieldsMetadata.path_1.name, ColumnType.text)

    path_2 = ColumnMetadata(GoogleAttributeFieldsMetadata.path_2.name, ColumnType.text)

    policy_summary = ColumnMetadata(GoogleAttributeFieldsMetadata.policy_summary.name, ColumnType.text)

    price_prefix = ColumnMetadata(GoogleAttributeFieldsMetadata.price_prefix.name, ColumnType.text)

    promo_text = ColumnMetadata(GoogleAttributeFieldsMetadata.promo_text.name, ColumnType.text)

    responsive_search_ad_descriptions = ColumnMetadata(
        GoogleAttributeFieldsMetadata.responsive_search_ad_descriptions.name, ColumnType.text)

    responsive_search_ad_headlines = ColumnMetadata(
        GoogleAttributeFieldsMetadata.responsive_search_ad_headlines.name,
        ColumnType.text)

    responsive_search_ad_path_1 = ColumnMetadata(GoogleAttributeFieldsMetadata.responsive_search_ad_path_1.name,
                                                 ColumnType.text)

    responsive_search_ad_path_2 = ColumnMetadata(GoogleAttributeFieldsMetadata.responsive_search_ad_path_2.name,
                                                 ColumnType.text)

    short_headline = ColumnMetadata(GoogleAttributeFieldsMetadata.short_headline.name, ColumnType.text)

    status = ColumnMetadata(GoogleAttributeFieldsMetadata.status.name, ColumnType.text)

    system_managed_entity_source = ColumnMetadata(
        GoogleAttributeFieldsMetadata.system_managed_entity_source.name,
        ColumnType.text)

    universal_app_ad_descriptions = ColumnMetadata(
        GoogleAttributeFieldsMetadata.universal_app_ad_descriptions.name,
        ColumnType.text)

    universal_app_ad_headlines = ColumnMetadata(GoogleAttributeFieldsMetadata.universal_app_ad_headlines.name,
                                                ColumnType.text)

    universal_app_ad_html_5_media_bundles = ColumnMetadata(
        GoogleAttributeFieldsMetadata.universal_app_ad_html_5_media_bundles.name, ColumnType.text)

    universal_app_ad_images = ColumnMetadata(GoogleAttributeFieldsMetadata.universal_app_ad_images.name,
                                             ColumnType.text)

    universal_app_ad_mandatory_ad_text = ColumnMetadata(
        GoogleAttributeFieldsMetadata.universal_app_ad_mandatory_ad_text.name, ColumnType.text)

    universal_app_ad_you_tube_videos = ColumnMetadata(
        GoogleAttributeFieldsMetadata.universal_app_ad_you_tube_videos.name,
        ColumnType.text)

    account_descriptive_name = ColumnMetadata(GoogleAttributeFieldsMetadata.account_descriptive_name.name,
                                              ColumnType.text)

    ad_group_desktop_bid_modifier = ColumnMetadata(
        GoogleAttributeFieldsMetadata.ad_group_desktop_bid_modifier.name,
        ColumnType.text)

    ad_group_id = ColumnMetadata(GoogleAttributeFieldsMetadata.ad_group_id.name, ColumnType.text)

    ad_group_mobile_bid_modifier = ColumnMetadata(
        GoogleAttributeFieldsMetadata.ad_group_mobile_bid_modifier.name,
        ColumnType.text)

    ad_group_name = ColumnMetadata(GoogleAttributeFieldsMetadata.ad_group_name.name, ColumnType.text)

    ad_group_tablet_bid_modifier = ColumnMetadata(
        GoogleAttributeFieldsMetadata.ad_group_tablet_bid_modifier.name,
        ColumnType.text)

    ad_group_type = ColumnMetadata(GoogleAttributeFieldsMetadata.ad_group_type.name, ColumnType.text)

    ad_rotation_mode = ColumnMetadata(GoogleAttributeFieldsMetadata.ad_rotation_mode.name, ColumnType.text)

    bidding_strategy_id = ColumnMetadata(GoogleAttributeFieldsMetadata.bidding_strategy_id.name, ColumnType.text)

    bidding_strategy_name = ColumnMetadata(GoogleAttributeFieldsMetadata.bidding_strategy_name.name,
                                           ColumnType.text)

    bidding_strategy_source = ColumnMetadata(GoogleAttributeFieldsMetadata.bidding_strategy_source.name,
                                             ColumnType.text)

    bidding_strategy_type = ColumnMetadata(GoogleAttributeFieldsMetadata.bidding_strategy_type.name,
                                           ColumnType.text)

    content_bid_criterion_type_group = ColumnMetadata(
        GoogleAttributeFieldsMetadata.content_bid_criterion_type_group.name,
        ColumnType.text)

    cpc_bid = ColumnMetadata(GoogleAttributeFieldsMetadata.cpc_bid.name, ColumnType.text)

    cpm_bid = ColumnMetadata(GoogleAttributeFieldsMetadata.cpm_bid.name, ColumnType.text)

    cpv_bid = ColumnMetadata(GoogleAttributeFieldsMetadata.cpv_bid.name, ColumnType.text)

    effective_target_roas = ColumnMetadata(GoogleAttributeFieldsMetadata.effective_target_roas.name,
                                           ColumnType.text)

    effective_target_roas_source = ColumnMetadata(
        GoogleAttributeFieldsMetadata.effective_target_roas_source.name,
        ColumnType.text)

    enhanced_cpc_enabled = ColumnMetadata(GoogleAttributeFieldsMetadata.enhanced_cpc_enabled.name,
                                          ColumnType.text)

    final_url_suffix = ColumnMetadata(GoogleAttributeFieldsMetadata.final_url_suffix.name, ColumnType.text)

    target_cpa = ColumnMetadata(GoogleAttributeFieldsMetadata.target_cpa.name, ColumnType.text)

    target_cpa_bid_source = ColumnMetadata(GoogleAttributeFieldsMetadata.target_cpa_bid_source.name,
                                           ColumnType.text)

    tracking_url_template = ColumnMetadata(GoogleAttributeFieldsMetadata.tracking_url_template.name,
                                           ColumnType.text)

    url_custom_parameters = ColumnMetadata(GoogleAttributeFieldsMetadata.url_custom_parameters.name,
                                           ColumnType.text)

    advertising_channel_sub_type = ColumnMetadata(
        GoogleAttributeFieldsMetadata.advertising_channel_sub_type.name,
        ColumnType.text)

    advertising_channel_type = ColumnMetadata(GoogleAttributeFieldsMetadata.advertising_channel_type.name,
                                              ColumnType.text)

    amount = ColumnMetadata(GoogleAttributeFieldsMetadata.amount.name, ColumnType.text)

    budget_id = ColumnMetadata(GoogleAttributeFieldsMetadata.budget_id.name, ColumnType.text)

    campaign_desktop_bid_modifier = ColumnMetadata(
        GoogleAttributeFieldsMetadata.campaign_desktop_bid_modifier.name,
        ColumnType.text)

    campaign_group_id = ColumnMetadata(GoogleAttributeFieldsMetadata.campaign_group_id.name, ColumnType.text)

    campaign_mobile_bid_modifier = ColumnMetadata(
        GoogleAttributeFieldsMetadata.campaign_mobile_bid_modifier.name,
        ColumnType.text)

    campaign_tablet_bid_modifier = ColumnMetadata(
        GoogleAttributeFieldsMetadata.campaign_tablet_bid_modifier.name,
        ColumnType.text)

    campaign_trial_type = ColumnMetadata(GoogleAttributeFieldsMetadata.campaign_trial_type.name, ColumnType.text)

    end_date = ColumnMetadata(GoogleAttributeFieldsMetadata.end_date.name, ColumnType.text)

    has_recommended_budget = ColumnMetadata(GoogleAttributeFieldsMetadata.has_recommended_budget.name,
                                            ColumnType.text)

    is_budget_explicitly_shared = ColumnMetadata(GoogleAttributeFieldsMetadata.is_budget_explicitly_shared.name,
                                                 ColumnType.text)

    maximize_conversion_value_target_roas = ColumnMetadata(
        GoogleAttributeFieldsMetadata.maximize_conversion_value_target_roas.name, ColumnType.text)

    period = ColumnMetadata(GoogleAttributeFieldsMetadata.period.name, ColumnType.text)

    recommended_budget_amount = ColumnMetadata(GoogleAttributeFieldsMetadata.recommended_budget_amount.name,
                                               ColumnType.text)

    serving_status = ColumnMetadata(GoogleAttributeFieldsMetadata.serving_status.name, ColumnType.text)

    start_date = ColumnMetadata(GoogleAttributeFieldsMetadata.start_date.name, ColumnType.text)

    total_amount = ColumnMetadata(GoogleAttributeFieldsMetadata.total_amount.name, ColumnType.text)

    approval_status = ColumnMetadata(GoogleAttributeFieldsMetadata.approval_status.name, ColumnType.text)

    cpc_bid_source = ColumnMetadata(GoogleAttributeFieldsMetadata.cpc_bid_source.name, ColumnType.text)

    creative_quality_score = ColumnMetadata(GoogleAttributeFieldsMetadata.creative_quality_score.name,
                                            ColumnType.text)

    criteria = ColumnMetadata(GoogleAttributeFieldsMetadata.criteria.name, ColumnType.text)

    gender = ColumnMetadata(GoogleAttributeFieldsMetadata.gender.name, ColumnType.text)

    age_range = ColumnMetadata(GoogleAttributeFieldsMetadata.age_range.name, ColumnType.text)

    keywords = ColumnMetadata(GoogleAttributeFieldsMetadata.keywords.name, ColumnType.text)

    criteria_destination_url = ColumnMetadata(GoogleAttributeFieldsMetadata.criteria_destination_url.name,
                                              ColumnType.text)

    estimated_add_clicks_at_first_position_cpc = ColumnMetadata(
        GoogleAttributeFieldsMetadata.estimated_add_clicks_at_first_position_cpc.name, ColumnType.text)

    estimated_add_cost_at_first_position_cpc = ColumnMetadata(
        GoogleAttributeFieldsMetadata.estimated_add_cost_at_first_position_cpc.name, ColumnType.text)

    final_app_urls = ColumnMetadata(GoogleAttributeFieldsMetadata.final_app_urls.name, ColumnType.text)

    final_mobile_urls = ColumnMetadata(GoogleAttributeFieldsMetadata.final_mobile_urls.name, ColumnType.text)

    final_urls = ColumnMetadata(GoogleAttributeFieldsMetadata.final_urls.name, ColumnType.text)

    first_page_cpc = ColumnMetadata(GoogleAttributeFieldsMetadata.first_page_cpc.name, ColumnType.text)

    first_position_cpc = ColumnMetadata(GoogleAttributeFieldsMetadata.first_position_cpc.name, ColumnType.text)

    has_quality_score = ColumnMetadata(GoogleAttributeFieldsMetadata.has_quality_score.name, ColumnType.text)

    keyword_match_type = ColumnMetadata(GoogleAttributeFieldsMetadata.keyword_match_type.name, ColumnType.text)

    post_click_quality_score = ColumnMetadata(GoogleAttributeFieldsMetadata.post_click_quality_score.name,
                                              ColumnType.text)

    quality_score = ColumnMetadata(GoogleAttributeFieldsMetadata.quality_score.name, ColumnType.text)

    search_predicted_ctr = ColumnMetadata(GoogleAttributeFieldsMetadata.search_predicted_ctr.name,
                                          ColumnType.text)

    system_serving_status = ColumnMetadata(GoogleAttributeFieldsMetadata.system_serving_status.name,
                                           ColumnType.text)

    top_of_page_cpc = ColumnMetadata(GoogleAttributeFieldsMetadata.top_of_page_cpc.name, ColumnType.text)

    vertical_id = ColumnMetadata(GoogleAttributeFieldsMetadata.vertical_id.name, ColumnType.text)

    city_name = ColumnMetadata(GoogleAttributeFieldsMetadata.city_name.name, ColumnType.text)

    country_name = ColumnMetadata(GoogleAttributeFieldsMetadata.country_name.name, ColumnType.text)

    is_targeting_location = ColumnMetadata(GoogleAttributeFieldsMetadata.is_targeting_location.name,
                                           ColumnType.text)

    metro_criteria_id = ColumnMetadata(GoogleAttributeFieldsMetadata.metro_criteria_id.name, ColumnType.text)

    most_specific_criteria_id = ColumnMetadata(GoogleAttributeFieldsMetadata.most_specific_criteria_id.name,
                                               ColumnType.text)

    region_name = ColumnMetadata(GoogleAttributeFieldsMetadata.region_name.name, ColumnType.text)

    base_campaign_id = ColumnMetadata(GoogleAttributeFieldsMetadata.base_campaign_id.name, ColumnType.text)

    bid_modifier = ColumnMetadata(GoogleAttributeFieldsMetadata.bid_modifier.name, ColumnType.text)

    cpm_bid_source = ColumnMetadata(GoogleAttributeFieldsMetadata.cpm_bid_source.name, ColumnType.text)

    is_restrict = ColumnMetadata(GoogleAttributeFieldsMetadata.is_restrict.name, ColumnType.text)
