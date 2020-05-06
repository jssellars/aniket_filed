from GoogleTuring.Infrastructure.Domain.ConversionFunctions import id_to_string, percentage_to_float, id_to_location_name, money_conversion
from GoogleTuring.Infrastructure.Domain.GoogleField import GoogleField
from GoogleTuring.Infrastructure.Domain.GoogleFieldType import GoogleFieldType
from GoogleTuring.Infrastructure.Domain.JoinCondition import JoinCondition


class GoogleFieldsMetadata:
    # Attributes
    accent_color = GoogleField(name="AccentColor", field_name="AccentColor", field_type=GoogleFieldType.ATTRIBUTE)

    account_currency_code = GoogleField(name="AccountCurrencyCode", field_name="AccountCurrencyCode", field_type=GoogleFieldType.ATTRIBUTE)

    account_time_zone = GoogleField(name="AccountTimeZone", field_name="AccountTimeZone", field_type=GoogleFieldType.ATTRIBUTE)

    ad_group_status = GoogleField(name="AdGroupStatus", field_name="AdGroupStatus", field_type=GoogleFieldType.ATTRIBUTE)

    ad_strength_info = GoogleField(name="AdStrengthInfo", field_name="AdStrengthInfo", field_type=GoogleFieldType.ATTRIBUTE)

    ad_type = GoogleField(name="AdType", field_name="AdType", field_type=GoogleFieldType.ATTRIBUTE)

    allow_flexible_color = GoogleField(name="AllowFlexibleColor", field_name="AllowFlexibleColor", field_type=GoogleFieldType.ATTRIBUTE)

    automated = GoogleField(name="Automated", field_name="Automated", field_type=GoogleFieldType.ATTRIBUTE)

    base_ad_group_id = GoogleField(name="BaseAdGroupId", field_name="BaseAdGroupId", field_type=GoogleFieldType.ATTRIBUTE)

    base_campaignId = GoogleField(name="BaseCampaignId", field_name="BaseCampaignId", field_type=GoogleFieldType.ATTRIBUTE)

    business_name = GoogleField(name="BusinessName", field_name="BusinessName", field_type=GoogleFieldType.ATTRIBUTE)

    call_only_phone_number = GoogleField(name="CallOnlyPhoneNumber", field_name="CallOnlyPhoneNumber", field_type=GoogleFieldType.ATTRIBUTE)

    call_to_action_text = GoogleField(name="CallToActionText", field_name="CallToActionText", field_type=GoogleFieldType.ATTRIBUTE)

    campaign_id = GoogleField(name="campaign_id", field_name="CampaignId", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=id_to_string)

    campaign_name = GoogleField(name="campaign_name", field_name="CampaignName", field_type=GoogleFieldType.ATTRIBUTE)

    campaign_status = GoogleField(name="CampaignStatus", field_name="CampaignStatus", field_type=GoogleFieldType.ATTRIBUTE)

    combined_approval_status = GoogleField(name="CombinedApprovalStatus", field_name="CombinedApprovalStatus", field_type=GoogleFieldType.ATTRIBUTE)

    conversion_adjustment = GoogleField(name="ConversionAdjustment", field_name="ConversionAdjustment", field_type=GoogleFieldType.ATTRIBUTE)

    creative_destination_url = GoogleField(name="CreativeDestinationUrl", field_name="CreativeDestinationUrl", field_type=GoogleFieldType.ATTRIBUTE)

    creative_final_app_urls = GoogleField(name="CreativeFinalAppUrls", field_name="CreativeFinalAppUrls", field_type=GoogleFieldType.ATTRIBUTE)

    creative_final_mobile_urls = GoogleField(name="CreativeFinalMobileUrls", field_name="CreativeFinalMobileUrls", field_type=GoogleFieldType.ATTRIBUTE)

    creative_final_urls = GoogleField(name="CreativeFinalUrls", field_name="CreativeFinalUrls", field_type=GoogleFieldType.ATTRIBUTE)

    creative_final_url_suffix = GoogleField(name="CreativeFinalUrlSuffix", field_name="CreativeFinalUrlSuffix", field_type=GoogleFieldType.ATTRIBUTE)

    creative_tracking_url_template = GoogleField(name="CreativeTrackingUrlTemplate", field_name="CreativeTrackingUrlTemplate",
                                                 field_type=GoogleFieldType.ATTRIBUTE)

    creative_url_custom_parameters = GoogleField(name="CreativeUrlCustomParameters", field_name="CreativeUrlCustomParameters",
                                                 field_type=GoogleFieldType.ATTRIBUTE)

    customer_descriptive_name = GoogleField(name="CustomerDescriptiveName", field_name="CustomerDescriptiveName", field_type=GoogleFieldType.ATTRIBUTE)

    description = GoogleField(name="Description", field_name="Description", field_type=GoogleFieldType.ATTRIBUTE)

    description_1 = GoogleField(name="Description1", field_name="Description1", field_type=GoogleFieldType.ATTRIBUTE)

    description_2 = GoogleField(name="Description2", field_name="Description2", field_type=GoogleFieldType.ATTRIBUTE)

    device_preference = GoogleField(name="DevicePreference", field_name="DevicePreference", field_type=GoogleFieldType.ATTRIBUTE)

    display_url = GoogleField(name="DisplayUrl", field_name="DisplayUrl", field_type=GoogleFieldType.ATTRIBUTE)

    enhanced_display_creative_landscape_logo_image_media_id = GoogleField(name="EnhancedDisplayCreativeLandscapeLogoImageMediaId",
                                                                          field_name="EnhancedDisplayCreativeLandscapeLogoImageMediaId",
                                                                          field_type=GoogleFieldType.ATTRIBUTE)

    enhanced_display_creative_logo_image_media_id = GoogleField(name="EnhancedDisplayCreativeLogoImageMediaId",
                                                                field_name="EnhancedDisplayCreativeLogoImageMediaId", field_type=GoogleFieldType.ATTRIBUTE)

    enhanced_display_creative_marketing_image_media_id = GoogleField(name="EnhancedDisplayCreativeMarketingImageMediaId",
                                                                     field_name="EnhancedDisplayCreativeMarketingImageMediaId",
                                                                     field_type=GoogleFieldType.ATTRIBUTE)

    enhanced_display_creative_marketing_image_square_media_id = GoogleField(name="EnhancedDisplayCreativeMarketingImageSquareMediaId",
                                                                            field_name="EnhancedDisplayCreativeMarketingImageSquareMediaId",
                                                                            field_type=GoogleFieldType.ATTRIBUTE)

    expanded_dynamic_search_creative_description_2 = GoogleField(name="ExpandedDynamicSearchCreativeDescription2",
                                                                 field_name="ExpandedDynamicSearchCreativeDescription2", field_type=GoogleFieldType.ATTRIBUTE)

    expanded_text_ad_description_2 = GoogleField(name="ExpandedTextAdDescription2", field_name="ExpandedTextAdDescription2", field_type=GoogleFieldType.ATTRIBUTE)

    expanded_text_ad_headline_part_3 = GoogleField(name="ExpandedTextAdHeadlinePart3", field_name="ExpandedTextAdHeadlinePart3",
                                                   field_type=GoogleFieldType.ATTRIBUTE)

    external_customer_id = GoogleField(name="account_id", field_name="ExternalCustomerId", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=id_to_string)

    format_setting = GoogleField(name="FormatSetting", field_name="FormatSetting", field_type=GoogleFieldType.ATTRIBUTE)

    gmail_creative_header_image_media_id = GoogleField(name="GmailCreativeHeaderImageMediaId", field_name="GmailCreativeHeaderImageMediaId",
                                                       field_type=GoogleFieldType.ATTRIBUTE)

    gmail_creative_logo_image_media_id = GoogleField(name="GmailCreativeLogoImageMediaId", field_name="GmailCreativeLogoImageMediaId",
                                                     field_type=GoogleFieldType.ATTRIBUTE)

    gmail_creative_marketing_image_media_id = GoogleField(name="GmailCreativeMarketingImageMediaId", field_name="GmailCreativeMarketingImageMediaId",
                                                          field_type=GoogleFieldType.ATTRIBUTE)

    gmail_teaser_business_name = GoogleField(name="GmailTeaserBusinessName", field_name="GmailTeaserBusinessName", field_type=GoogleFieldType.ATTRIBUTE)

    gmail_teaser_description = GoogleField(name="GmailTeaserDescription", field_name="GmailTeaserDescription", field_type=GoogleFieldType.ATTRIBUTE)

    gmail_teaser_headline = GoogleField(name="GmailTeaserHeadline", field_name="GmailTeaserHeadline", field_type=GoogleFieldType.ATTRIBUTE)

    headline = GoogleField(name="Headline", field_name="Headline", field_type=GoogleFieldType.ATTRIBUTE)

    headline_part_1 = GoogleField(name="headline_part_1", field_name="HeadlinePart1", field_type=GoogleFieldType.ATTRIBUTE)

    headline_part_2 = GoogleField(name="headline_part_2", field_name="HeadlinePart2", field_type=GoogleFieldType.ATTRIBUTE)

    ad_name = GoogleField(name='ad_name', required_fields=[headline_part_1, headline_part_2], field_type=GoogleFieldType.ATTRIBUTE)

    id = GoogleField(name="Id", field_name="Id", field_type=GoogleFieldType.ATTRIBUTE)

    ad_id = GoogleField(name="ad_id", field_name="Id", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=id_to_string)

    image_ad_url = GoogleField(name="ImageAdUrl", field_name="ImageAdUrl", field_type=GoogleFieldType.ATTRIBUTE)

    image_creative_image_height = GoogleField(name="ImageCreativeImageHeight", field_name="ImageCreativeImageHeight", field_type=GoogleFieldType.ATTRIBUTE)

    image_creative_image_width = GoogleField(name="ImageCreativeImageWidth", field_name="ImageCreativeImageWidth", field_type=GoogleFieldType.ATTRIBUTE)

    image_creative_mime_type = GoogleField(name="ImageCreativeMimeType", field_name="ImageCreativeMimeType", field_type=GoogleFieldType.ATTRIBUTE)

    image_creative_name = GoogleField(name="ImageCreativeName", field_name="ImageCreativeName", field_type=GoogleFieldType.ATTRIBUTE)

    is_negative = GoogleField(name="IsNegative", field_name="IsNegative", field_type=GoogleFieldType.ATTRIBUTE)

    label_ids = GoogleField(name="LabelIds", field_name="LabelIds", field_type=GoogleFieldType.ATTRIBUTE)

    labels = GoogleField(name="Labels", field_name="Labels", field_type=GoogleFieldType.ATTRIBUTE)

    long_headline = GoogleField(name="LongHeadline", field_name="LongHeadline", field_type=GoogleFieldType.ATTRIBUTE)

    main_color = GoogleField(name="MainColor", field_name="MainColor", field_type=GoogleFieldType.ATTRIBUTE)

    marketing_image_call_to_action_text = GoogleField(name="MarketingImageCallToActionText", field_name="MarketingImageCallToActionText",
                                                      field_type=GoogleFieldType.ATTRIBUTE)

    marketing_image_call_to_action_text_color = GoogleField(name="MarketingImageCallToActionTextColor", field_name="MarketingImageCallToActionTextColor",
                                                            field_type=GoogleFieldType.ATTRIBUTE)

    marketing_image_description = GoogleField(name="MarketingImageDescription", field_name="MarketingImageDescription", field_type=GoogleFieldType.ATTRIBUTE)

    marketing_image_headline = GoogleField(name="MarketingImageHeadline", field_name="MarketingImageHeadline", field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_accent_color = GoogleField(name="MultiAssetResponsiveDisplayAdAccentColor",
                                                                 field_name="MultiAssetResponsiveDisplayAdAccentColor", field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_allow_flexible_color = GoogleField(name="MultiAssetResponsiveDisplayAdAllowFlexibleColor",
                                                                         field_name="MultiAssetResponsiveDisplayAdAllowFlexibleColor",
                                                                         field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_business_name = GoogleField(name="MultiAssetResponsiveDisplayAdBusinessName",
                                                                  field_name="MultiAssetResponsiveDisplayAdBusinessName", field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_call_to_action_text = GoogleField(name="MultiAssetResponsiveDisplayAdCallToActionText",
                                                                        field_name="MultiAssetResponsiveDisplayAdCallToActionText",
                                                                        field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_descriptions = GoogleField(name="MultiAssetResponsiveDisplayAdDescriptions",
                                                                 field_name="MultiAssetResponsiveDisplayAdDescriptions", field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_dynamic_settings_price_prefix = GoogleField(name="MultiAssetResponsiveDisplayAdDynamicSettingsPricePrefix",
                                                                                  field_name="MultiAssetResponsiveDisplayAdDynamicSettingsPricePrefix",
                                                                                  field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_dynamic_settings_promo_text = GoogleField(name="MultiAssetResponsiveDisplayAdDynamicSettingsPromoText",
                                                                                field_name="MultiAssetResponsiveDisplayAdDynamicSettingsPromoText",
                                                                                field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_format_setting = GoogleField(name="MultiAssetResponsiveDisplayAdFormatSetting",
                                                                   field_name="MultiAssetResponsiveDisplayAdFormatSetting", field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_headlines = GoogleField(name="MultiAssetResponsiveDisplayAdHeadlines",
                                                              field_name="MultiAssetResponsiveDisplayAdHeadlines",
                                                              field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_landscape_logo_images = GoogleField(name="MultiAssetResponsiveDisplayAdLandscapeLogoImages",
                                                                          field_name="MultiAssetResponsiveDisplayAdLandscapeLogoImages",
                                                                          field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_logo_images = GoogleField(name="MultiAssetResponsiveDisplayAdLogoImages",
                                                                field_name="MultiAssetResponsiveDisplayAdLogoImages", field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_long_headline = GoogleField(name="MultiAssetResponsiveDisplayAdLongHeadline",
                                                                  field_name="MultiAssetResponsiveDisplayAdLongHeadline", field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_main_color = GoogleField(name="MultiAssetResponsiveDisplayAdMainColor",
                                                               field_name="MultiAssetResponsiveDisplayAdMainColor",
                                                               field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_marketing_images = GoogleField(name="MultiAssetResponsiveDisplayAdMarketingImages",
                                                                     field_name="MultiAssetResponsiveDisplayAdMarketingImages",
                                                                     field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_square_marketing_images = GoogleField(name="MultiAssetResponsiveDisplayAdSquareMarketingImages",
                                                                            field_name="MultiAssetResponsiveDisplayAdSquareMarketingImages",
                                                                            field_type=GoogleFieldType.ATTRIBUTE)

    multi_asset_responsive_display_ad_you_tube_videos = GoogleField(name="MultiAssetResponsiveDisplayAdYouTubeVideos",
                                                                    field_name="MultiAssetResponsiveDisplayAdYouTubeVideos", field_type=GoogleFieldType.ATTRIBUTE)

    path_1 = GoogleField(name="Path1", field_name="Path1", field_type=GoogleFieldType.ATTRIBUTE)

    path_2 = GoogleField(name="Path2", field_name="Path2", field_type=GoogleFieldType.ATTRIBUTE)

    policy_summary = GoogleField(name="PolicySummary", field_name="PolicySummary", field_type=GoogleFieldType.ATTRIBUTE)

    price_prefix = GoogleField(name="PricePrefix", field_name="PricePrefix", field_type=GoogleFieldType.ATTRIBUTE)

    promo_text = GoogleField(name="PromoText", field_name="PromoText", field_type=GoogleFieldType.ATTRIBUTE)

    responsive_search_ad_descriptions = GoogleField(name="ResponsiveSearchAdDescriptions", field_name="ResponsiveSearchAdDescriptions",
                                                    field_type=GoogleFieldType.ATTRIBUTE)

    responsive_search_ad_headlines = GoogleField(name="ResponsiveSearchAdHeadlines", field_name="ResponsiveSearchAdHeadlines",
                                                 field_type=GoogleFieldType.ATTRIBUTE)

    responsive_search_ad_path_1 = GoogleField(name="ResponsiveSearchAdPath1", field_name="ResponsiveSearchAdPath1", field_type=GoogleFieldType.ATTRIBUTE)

    responsive_search_ad_path_2 = GoogleField(name="ResponsiveSearchAdPath2", field_name="ResponsiveSearchAdPath2", field_type=GoogleFieldType.ATTRIBUTE)

    short_headline = GoogleField(name="ShortHeadline", field_name="ShortHeadline", field_type=GoogleFieldType.ATTRIBUTE)

    status = GoogleField(name="Status", field_name="Status", field_type=GoogleFieldType.ATTRIBUTE)

    system_managed_entity_source = GoogleField(name="SystemManagedEntitySource", field_name="SystemManagedEntitySource", field_type=GoogleFieldType.ATTRIBUTE)

    universal_app_ad_descriptions = GoogleField(name="UniversalAppAdDescriptions", field_name="UniversalAppAdDescriptions", field_type=GoogleFieldType.ATTRIBUTE)

    universal_app_ad_headlines = GoogleField(name="UniversalAppAdHeadlines", field_name="UniversalAppAdHeadlines", field_type=GoogleFieldType.ATTRIBUTE)

    universal_app_ad_html_5_media_bundles = GoogleField(name="UniversalAppAdHtml5MediaBundles", field_name="UniversalAppAdHtml5MediaBundles",
                                                        field_type=GoogleFieldType.ATTRIBUTE)

    universal_app_ad_images = GoogleField(name="UniversalAppAdImages", field_name="UniversalAppAdImages", field_type=GoogleFieldType.ATTRIBUTE)

    universal_app_ad_mandatory_ad_text = GoogleField(name="UniversalAppAdMandatoryAdText", field_name="UniversalAppAdMandatoryAdText",
                                                     field_type=GoogleFieldType.ATTRIBUTE)

    universal_app_ad_you_tube_videos = GoogleField(name="UniversalAppAdYouTubeVideos", field_name="UniversalAppAdYouTubeVideos",
                                                   field_type=GoogleFieldType.ATTRIBUTE)

    account_descriptive_name = GoogleField(name="account_name", field_name="AccountDescriptiveName", field_type=GoogleFieldType.ATTRIBUTE)

    ad_group_desktop_bid_modifier = GoogleField(name="AdGroupDesktopBidModifier", field_name="AdGroupDesktopBidModifier", field_type=GoogleFieldType.ATTRIBUTE)

    ad_group_id = GoogleField(name="ad_group_id", field_name="AdGroupId", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=id_to_string)

    ad_group_mobile_bid_modifier = GoogleField(name="AdGroupMobileBidModifier", field_name="AdGroupMobileBidModifier", field_type=GoogleFieldType.ATTRIBUTE)

    ad_group_name = GoogleField(name="ad_group_name", field_name="AdGroupName", field_type=GoogleFieldType.ATTRIBUTE)

    ad_group_tablet_bid_modifier = GoogleField(name="AdGroupTabletBidModifier", field_name="AdGroupTabletBidModifier", field_type=GoogleFieldType.ATTRIBUTE)

    ad_group_type = GoogleField(name="AdGroupType", field_name="AdGroupType", field_type=GoogleFieldType.ATTRIBUTE)

    ad_rotation_mode = GoogleField(name="AdRotationMode", field_name="AdRotationMode", field_type=GoogleFieldType.ATTRIBUTE)

    bidding_strategy_id = GoogleField(name="BiddingStrategyId", field_name="BiddingStrategyId", field_type=GoogleFieldType.ATTRIBUTE)

    bidding_strategy_name = GoogleField(name="bidding_strategy_name", field_name="BiddingStrategyName", field_type=GoogleFieldType.ATTRIBUTE)

    bidding_strategy_source = GoogleField(name="BiddingStrategySource", field_name="BiddingStrategySource", field_type=GoogleFieldType.ATTRIBUTE)

    bidding_strategy_type = GoogleField(name="bidding_strategy_type", field_name="BiddingStrategyType", field_type=GoogleFieldType.ATTRIBUTE)

    content_bid_criterion_type_group = GoogleField(name="ContentBidCriterionTypeGroup", field_name="ContentBidCriterionTypeGroup",
                                                   field_type=GoogleFieldType.ATTRIBUTE)

    cpc_bid = GoogleField(name="CpcBid", field_name="CpcBid", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=money_conversion)

    cpm_bid = GoogleField(name="CpmBid", field_name="CpmBid", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=money_conversion)

    cpv_bid = GoogleField(name="CpvBid", field_name="CpvBid", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=money_conversion)

    effective_target_roas = GoogleField(name="effective_target_roas", field_name="EffectiveTargetRoas", field_type=GoogleFieldType.ATTRIBUTE)

    effective_target_roas_source = GoogleField(name="EffectiveTargetRoasSource", field_name="EffectiveTargetRoasSource", field_type=GoogleFieldType.ATTRIBUTE)

    enhanced_cpc_enabled = GoogleField(name="EnhancedCpcEnabled", field_name="EnhancedCpcEnabled", field_type=GoogleFieldType.ATTRIBUTE)

    final_url_suffix = GoogleField(name="FinalUrlSuffix", field_name="FinalUrlSuffix", field_type=GoogleFieldType.ATTRIBUTE)

    target_cpa = GoogleField(name="TargetCpa", field_name="TargetCpa", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=money_conversion)

    target_cpa_bid_source = GoogleField(name="TargetCpaBidSource", field_name="TargetCpaBidSource", field_type=GoogleFieldType.ATTRIBUTE)

    tracking_url_template = GoogleField(name="TrackingUrlTemplate", field_name="TrackingUrlTemplate", field_type=GoogleFieldType.ATTRIBUTE)

    url_custom_parameters = GoogleField(name="UrlCustomParameters", field_name="UrlCustomParameters", field_type=GoogleFieldType.ATTRIBUTE)

    advertising_channel_sub_type = GoogleField(name="AdvertisingChannelSubType", field_name="AdvertisingChannelSubType", field_type=GoogleFieldType.ATTRIBUTE)

    advertising_channel_type = GoogleField(name="AdvertisingChannelType", field_name="AdvertisingChannelType", field_type=GoogleFieldType.ATTRIBUTE)

    amount = GoogleField(name="Amount", field_name="Amount", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=money_conversion)

    budget_id = GoogleField(name="BudgetId", field_name="BudgetId", field_type=GoogleFieldType.ATTRIBUTE)

    campaign_desktop_bid_modifier = GoogleField(name="CampaignDesktopBidModifier", field_name="CampaignDesktopBidModifier", field_type=GoogleFieldType.ATTRIBUTE)

    campaign_group_id = GoogleField(name="CampaignGroupId", field_name="CampaignGroupId", field_type=GoogleFieldType.ATTRIBUTE)

    campaign_mobile_bid_modifier = GoogleField(name="CampaignMobileBidModifier", field_name="CampaignMobileBidModifier", field_type=GoogleFieldType.ATTRIBUTE)

    campaign_tablet_bid_modifier = GoogleField(name="CampaignTabletBidModifier", field_name="CampaignTabletBidModifier", field_type=GoogleFieldType.ATTRIBUTE)

    campaign_trial_type = GoogleField(name="CampaignTrialType", field_name="CampaignTrialType", field_type=GoogleFieldType.ATTRIBUTE)

    end_date = GoogleField(name="EndDate", field_name="EndDate", field_type=GoogleFieldType.ATTRIBUTE)

    has_recommended_budget = GoogleField(name="HasRecommendedBudget", field_name="HasRecommendedBudget", field_type=GoogleFieldType.ATTRIBUTE)

    is_budget_explicitly_shared = GoogleField(name="IsBudgetExplicitlyShared", field_name="IsBudgetExplicitlyShared", field_type=GoogleFieldType.ATTRIBUTE)

    maximize_conversion_value_target_roas = GoogleField(name="maximize_conversion_value_target_roas", field_name="MaximizeConversionValueTargetRoas",
                                                        field_type=GoogleFieldType.ATTRIBUTE)

    period = GoogleField(name="Period", field_name="Period", field_type=GoogleFieldType.ATTRIBUTE)

    recommended_budget_amount = GoogleField(name="RecommendedBudgetAmount", field_name="RecommendedBudgetAmount", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=money_conversion)

    serving_status = GoogleField(name="ServingStatus", field_name="ServingStatus", field_type=GoogleFieldType.ATTRIBUTE)

    start_date = GoogleField(name="StartDate", field_name="StartDate", field_type=GoogleFieldType.ATTRIBUTE)

    total_amount = GoogleField(name="TotalAmount", field_name="TotalAmount", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=money_conversion)

    approval_status = GoogleField(name="ApprovalStatus", field_name="ApprovalStatus", field_type=GoogleFieldType.ATTRIBUTE)

    cpc_bid_source = GoogleField(name="CpcBidSource", field_name="CpcBidSource", field_type=GoogleFieldType.ATTRIBUTE)

    creative_quality_score = GoogleField(name="CreativeQualityScore", field_name="CreativeQualityScore", field_type=GoogleFieldType.ATTRIBUTE)

    criteria = GoogleField(name="criteria", field_name="Criteria", field_type=GoogleFieldType.ATTRIBUTE)

    gender = GoogleField(name="gender", field_name="Criteria", field_type=GoogleFieldType.ATTRIBUTE)

    age_range = GoogleField(name="age_range", field_name="Criteria", field_type=GoogleFieldType.ATTRIBUTE)

    keywords = GoogleField(name="keywords", field_name="Criteria", field_type=GoogleFieldType.ATTRIBUTE)

    criteria_destination_url = GoogleField(name="CriteriaDestinationUrl", field_name="CriteriaDestinationUrl", field_type=GoogleFieldType.ATTRIBUTE)

    estimated_add_clicks_at_first_position_cpc = GoogleField(name="EstimatedAddClicksAtFirstPositionCpc", field_name="EstimatedAddClicksAtFirstPositionCpc",
                                                             field_type=GoogleFieldType.ATTRIBUTE)

    estimated_add_cost_at_first_position_cpc = GoogleField(name="EstimatedAddCostAtFirstPositionCpc", field_name="EstimatedAddCostAtFirstPositionCpc",
                                                           field_type=GoogleFieldType.ATTRIBUTE, conversion_function=money_conversion)

    final_app_urls = GoogleField(name="FinalAppUrls", field_name="FinalAppUrls", field_type=GoogleFieldType.ATTRIBUTE)

    final_mobile_urls = GoogleField(name="FinalMobileUrls", field_name="FinalMobileUrls", field_type=GoogleFieldType.ATTRIBUTE)

    final_urls = GoogleField(name="FinalUrls", field_name="FinalUrls", field_type=GoogleFieldType.ATTRIBUTE)

    first_page_cpc = GoogleField(name="FirstPageCpc", field_name="FirstPageCpc", field_type=GoogleFieldType.ATTRIBUTE)

    first_position_cpc = GoogleField(name="FirstPositionCpc", field_name="FirstPositionCpc", field_type=GoogleFieldType.ATTRIBUTE)

    has_quality_score = GoogleField(name="HasQualityScore", field_name="HasQualityScore", field_type=GoogleFieldType.ATTRIBUTE)

    keyword_match_type = GoogleField(name="KeywordMatchType", field_name="KeywordMatchType", field_type=GoogleFieldType.ATTRIBUTE)

    post_click_quality_score = GoogleField(name="PostClickQualityScore", field_name="PostClickQualityScore", field_type=GoogleFieldType.ATTRIBUTE)

    quality_score = GoogleField(name="QualityScore", field_name="QualityScore", field_type=GoogleFieldType.ATTRIBUTE)

    search_predicted_ctr = GoogleField(name="SearchPredictedCtr", field_name="SearchPredictedCtr", field_type=GoogleFieldType.ATTRIBUTE)

    system_serving_status = GoogleField(name="SystemServingStatus", field_name="SystemServingStatus", field_type=GoogleFieldType.ATTRIBUTE)

    top_of_page_cpc = GoogleField(name="TopOfPageCpc", field_name="TopOfPageCpc", field_type=GoogleFieldType.ATTRIBUTE)

    vertical_id = GoogleField(name="VerticalId", field_name="VerticalId", field_type=GoogleFieldType.ATTRIBUTE)

    city_name = GoogleField(name="city_name", field_name="CityCriteriaId", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=id_to_location_name)

    country_name = GoogleField(name="country_name", field_name="CountryCriteriaId", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=id_to_location_name)

    is_targeting_location = GoogleField(name="IsTargetingLocation", field_name="IsTargetingLocation", field_type=GoogleFieldType.ATTRIBUTE)

    metro_criteria_id = GoogleField(name="MetroCriteriaId", field_name="MetroCriteriaId", field_type=GoogleFieldType.ATTRIBUTE)

    most_specific_criteria_id = GoogleField(name="MostSpecificCriteriaId", field_name="MostSpecificCriteriaId", field_type=GoogleFieldType.ATTRIBUTE)

    region_name = GoogleField(name="region_name", field_name="RegionCriteriaId", field_type=GoogleFieldType.ATTRIBUTE, conversion_function=id_to_location_name)

    base_campaign_id = GoogleField(name="BaseCampaignId", field_name="BaseCampaignId", field_type=GoogleFieldType.ATTRIBUTE)

    bid_modifier = GoogleField(name="BidModifier", field_name="BidModifier", field_type=GoogleFieldType.ATTRIBUTE)

    cpm_bid_source = GoogleField(name="CpmBidSource", field_name="CpmBidSource", field_type=GoogleFieldType.ATTRIBUTE)

    is_restrict = GoogleField(name="IsRestrict", field_name="IsRestrict", field_type=GoogleFieldType.ATTRIBUTE)

    # Segments
    ad_network_type_1 = GoogleField(name="AdNetworkType1", field_name="AdNetworkType1", field_type=GoogleFieldType.SEGMENT)

    ad_network_type_2 = GoogleField(name="AdNetworkType2", field_name="AdNetworkType2", field_type=GoogleFieldType.SEGMENT)

    click_type = GoogleField(name="ClickType", field_name="ClickType", field_type=GoogleFieldType.SEGMENT)

    conversion_adjustment_lag_bucket = GoogleField(name="ConversionAdjustmentLagBucket", field_name="ConversionAdjustmentLagBucket",
                                                   field_type=GoogleFieldType.SEGMENT)

    conversion_lag_bucket = GoogleField(name="ConversionLagBucket", field_name="ConversionLagBucket", field_type=GoogleFieldType.SEGMENT)

    conversion_tracker_id = GoogleField(name="ConversionTrackerId", field_name="ConversionTrackerId", field_type=GoogleFieldType.SEGMENT)

    conversion_type_name = GoogleField(name="ConversionTypeName", field_name="ConversionTypeName", field_type=GoogleFieldType.SEGMENT)

    criterion_id = GoogleField(name="CriterionId", field_name="CriterionId", field_type=GoogleFieldType.SEGMENT)

    criterion_type = GoogleField(name="CriterionType", field_name="CriterionType", field_type=GoogleFieldType.SEGMENT)

    date = GoogleField(name="date", field_name="Date", field_type=GoogleFieldType.SEGMENT)

    day_of_week = GoogleField(name="DayOfWeek", field_name="DayOfWeek", field_type=GoogleFieldType.SEGMENT)

    device = GoogleField(name="device", field_name="Device", field_type=GoogleFieldType.SEGMENT)

    external_conversion_source = GoogleField(name="ExternalConversionSource", field_name="ExternalConversionSource", field_type=GoogleFieldType.SEGMENT)

    month = GoogleField(name="Month", field_name="Month", field_type=GoogleFieldType.SEGMENT)

    month_of_year = GoogleField(name="MonthOfYear", field_name="MonthOfYear", field_type=GoogleFieldType.SEGMENT)

    quarter = GoogleField(name="Quarter", field_name="Quarter", field_type=GoogleFieldType.SEGMENT)

    slot = GoogleField(name="Slot", field_name="Slot", field_type=GoogleFieldType.SEGMENT)

    week = GoogleField(name="Week", field_name="Week", field_type=GoogleFieldType.SEGMENT)

    year = GoogleField(name="Year", field_name="Year", field_type=GoogleFieldType.SEGMENT)

    hour_of_day = GoogleField(name="HourOfDay", field_name="HourOfDay", field_type=GoogleFieldType.SEGMENT)

    conversion_attribution_event_type = GoogleField(name="ConversionAttributionEventType", field_name="ConversionAttributionEventType",
                                                    field_type=GoogleFieldType.SEGMENT)

    ad_format = GoogleField(name="HourOfDay", field_name="HourOfDay", field_type=GoogleFieldType.SEGMENT)

    location_type = GoogleField(name="LocationType", field_name="LocationType", field_type=GoogleFieldType.SEGMENT)

    conversion_category_name = GoogleField(name="ConversionCategoryName", field_name="ConversionCategoryName", field_type=GoogleFieldType.SEGMENT)

    ad_group_id_segment = GoogleField(name="AdGroupIdSegment", field_name="AdGroupId", field_type=GoogleFieldType.SEGMENT)

    ad_group_name_segment = GoogleField(name="AdGroupNameSegment", field_name="AdGroupName", field_type=GoogleFieldType.SEGMENT)

    ad_group_status_segment = GoogleField(name="AdGroupStatusSegment", field_name="AdGroupStatus", field_type=GoogleFieldType.SEGMENT)

    # Metrics
    absolute_top_impression_percentage = GoogleField(name="AbsoluteTopImpressionPercentage", field_name="AbsoluteTopImpressionPercentage",
                                                     field_type=GoogleFieldType.METRIC)

    active_view_cpm = GoogleField(name="ActiveViewCpm", field_name="ActiveViewCpm", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    active_view_ctr = GoogleField(name="ActiveViewCtr", field_name="ActiveViewCtr", field_type=GoogleFieldType.METRIC)

    active_view_impressions = GoogleField(name="ActiveViewImpressions", field_name="ActiveViewImpressions", field_type=GoogleFieldType.METRIC)

    active_view_measurability = GoogleField(name="ActiveViewMeasurability", field_name="ActiveViewMeasurability", field_type=GoogleFieldType.METRIC)

    active_view_measurable_cost = GoogleField(name="ActiveViewMeasurableCost", field_name="ActiveViewMeasurableCost", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    active_view_measurable_impressions = GoogleField(name="ActiveViewMeasurableImpressions", field_name="ActiveViewMeasurableImpressions",
                                                     field_type=GoogleFieldType.METRIC)

    active_view_viewability = GoogleField(name="ActiveViewViewability", field_name="ActiveViewViewability", field_type=GoogleFieldType.METRIC)

    all_conversion_rate = GoogleField(name="AllConversionRate", field_name="AllConversionRate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    all_conversions = GoogleField(name="all_conversions", field_name="AllConversions", field_type=GoogleFieldType.METRIC)

    all_conversion_value = GoogleField(name="AllConversionValue", field_name="AllConversionValue", field_type=GoogleFieldType.METRIC)

    average_cost = GoogleField(name="AverageCost", field_name="AverageCost", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    average_cpc = GoogleField(name="average_cpc", field_name="AverageCpc", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    average_cpe = GoogleField(name="AverageCpe", field_name="AverageCpe", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    average_cpm = GoogleField(name="average_cpm", field_name="AverageCpm", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    average_cpv = GoogleField(name="AverageCpv", field_name="AverageCpv", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    average_pageviews = GoogleField(name="AveragePageviews", field_name="AveragePageviews", field_type=GoogleFieldType.METRIC)

    average_position = GoogleField(name="AveragePosition", field_name="AveragePosition", field_type=GoogleFieldType.METRIC)

    average_time_on_site = GoogleField(name="AverageTimeOnSite", field_name="AverageTimeOnSite", field_type=GoogleFieldType.METRIC)

    bounce_rate = GoogleField(name="BounceRate", field_name="BounceRate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    click_assisted_conversions = GoogleField(name="ClickAssistedConversions", field_name="ClickAssistedConversions", field_type=GoogleFieldType.METRIC)

    click_assisted_conversions_over_last_click_conversions = GoogleField(name="ClickAssistedConversionsOverLastClickConversions",
                                                                         field_name="ClickAssistedConversionsOverLastClickConversions",
                                                                         field_type=GoogleFieldType.METRIC)

    click_assisted_conversion_value = GoogleField(name="ClickAssistedConversionValue", field_name="ClickAssistedConversionValue",
                                                  field_type=GoogleFieldType.METRIC)

    clicks = GoogleField(name="clicks", field_name="Clicks", field_type=GoogleFieldType.METRIC)

    link_clicks = GoogleField(name='link_clicks', join_condition=JoinCondition(compare_field=click_type, equal_to='URL_CLICKS', target_field=clicks))

    conversion_rate = GoogleField(name="ConversionRate", field_name="ConversionRate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    conversions = GoogleField(name="conversions", field_name="Conversions", field_type=GoogleFieldType.METRIC)

    leads = GoogleField(name='leads', join_condition=JoinCondition(compare_field=conversion_category_name, equal_to='Lead', target_field=conversions))

    purchases = GoogleField(name='purchases', join_condition=JoinCondition(compare_field=conversion_category_name, equal_to='Purchase/Sale', target_field=conversions))

    conversion_value = GoogleField(name="conversion_value", field_name="ConversionValue", field_type=GoogleFieldType.METRIC)

    cost = GoogleField(name="cost", field_name="Cost", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    cost_per_all_conversion = GoogleField(name="CostPerAllConversion", field_name="CostPerAllConversion", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    cost_per_conversion = GoogleField(name="CostPerConversion", field_name="CostPerConversion", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    cost_per_current_model_attributed_conversion = GoogleField(name="CostPerCurrentModelAttributedConversion",
                                                               field_name="CostPerCurrentModelAttributedConversion", field_type=GoogleFieldType.METRIC, conversion_function=money_conversion)

    cross_device_conversions = GoogleField(name="CrossDeviceConversions", field_name="CrossDeviceConversions", field_type=GoogleFieldType.METRIC)

    ctr = GoogleField(name="ctr", field_name="Ctr", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    current_model_attributed_conversions = GoogleField(name="CurrentModelAttributedConversions", field_name="CurrentModelAttributedConversions",
                                                       field_type=GoogleFieldType.METRIC)

    current_model_attributed_conversion_value = GoogleField(name="CurrentModelAttributedConversionValue",
                                                            field_name="CurrentModelAttributedConversionValue",
                                                            field_type=GoogleFieldType.METRIC)

    engagement_rate = GoogleField(name="engagement_rate", field_name="EngagementRate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    engagements = GoogleField(name="engagements", field_name="Engagements", field_type=GoogleFieldType.METRIC)

    gmail_forwards = GoogleField(name="GmailForwards", field_name="GmailForwards", field_type=GoogleFieldType.METRIC)

    gmail_saves = GoogleField(name="GmailSaves", field_name="GmailSaves", field_type=GoogleFieldType.METRIC)

    gmail_secondary_clicks = GoogleField(name="GmailSecondaryClicks", field_name="GmailSecondaryClicks", field_type=GoogleFieldType.METRIC)

    impression_assisted_conversions = GoogleField(name="ImpressionAssistedConversions", field_name="ImpressionAssistedConversions",
                                                  field_type=GoogleFieldType.METRIC)

    impression_assisted_conversions_over_last_click_conversions = GoogleField(name="ImpressionAssistedConversionsOverLastClickConversions",
                                                                              field_name="ImpressionAssistedConversionsOverLastClickConversions",
                                                                              field_type=GoogleFieldType.METRIC)

    impression_assisted_conversion_value = GoogleField(name="ImpressionAssistedConversionValue", field_name="ImpressionAssistedConversionValue",
                                                       field_type=GoogleFieldType.METRIC)

    impressions = GoogleField(name="impressions", field_name="Impressions", field_type=GoogleFieldType.METRIC)

    interaction_rate = GoogleField(name="interaction_rate", field_name="InteractionRate", field_type=GoogleFieldType.METRIC,
                                   conversion_function=percentage_to_float)

    interactions = GoogleField(name="interactions", field_name="Interactions", field_type=GoogleFieldType.METRIC)

    interaction_types = GoogleField(name="InteractionTypes", field_name="InteractionTypes", field_type=GoogleFieldType.METRIC)

    percent_new_visitors = GoogleField(name="PercentNewVisitors", field_name="PercentNewVisitors", field_type=GoogleFieldType.METRIC)

    top_impression_percentage = GoogleField(name="TopImpressionPercentage", field_name="TopImpressionPercentage", field_type=GoogleFieldType.METRIC)

    value_per_all_conversion = GoogleField(name="ValuePerAllConversion", field_name="ValuePerAllConversion", field_type=GoogleFieldType.METRIC)

    value_per_conversion = GoogleField(name="ValuePerConversion", field_name="ValuePerConversion", field_type=GoogleFieldType.METRIC)

    value_per_current_model_attributed_conversion = GoogleField(name="ValuePerCurrentModelAttributedConversion",
                                                                field_name="ValuePerCurrentModelAttributedConversion", field_type=GoogleFieldType.METRIC)

    video_quartile_100_rate = GoogleField(name="VideoQuartile100Rate", field_name="VideoQuartile100Rate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    video_quartile_25_rate = GoogleField(name="VideoQuartile25Rate", field_name="VideoQuartile25Rate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    video_quartile_50_rate = GoogleField(name="VideoQuartile50Rate", field_name="VideoQuartile50Rate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    video_quartile_75_rate = GoogleField(name="VideoQuartile75Rate", field_name="VideoQuartile75Rate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    video_view_rate = GoogleField(name="VideoViewRate", field_name="VideoViewRate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    video_views = GoogleField(name="VideoViews", field_name="VideoViews", field_type=GoogleFieldType.METRIC)

    view_through_conversions = GoogleField(name="ViewThroughConversions", field_name="ViewThroughConversions", field_type=GoogleFieldType.METRIC)

    content_impression_share = GoogleField(name="ContentImpressionShare", field_name="ContentImpressionShare", field_type=GoogleFieldType.METRIC)

    content_rank_lost_impression_share = GoogleField(name="ContentRankLostImpressionShare", field_name="ContentRankLostImpressionShare",
                                                     field_type=GoogleFieldType.METRIC)

    num_offline_impressions = GoogleField(name="NumOfflineImpressions", field_name="NumOfflineImpressions", field_type=GoogleFieldType.METRIC)

    num_offline_interactions = GoogleField(name="NumOfflineInteractions", field_name="NumOfflineInteractions", field_type=GoogleFieldType.METRIC)

    offline_interaction_rate = GoogleField(name="OfflineInteractionRate", field_name="OfflineInteractionRate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    relative_ctr = GoogleField(name="RelativeCtr", field_name="RelativeCtr", field_type=GoogleFieldType.METRIC)

    search_absolute_top_impression_share = GoogleField(name="SearchAbsoluteTopImpressionShare", field_name="SearchAbsoluteTopImpressionShare",
                                                       field_type=GoogleFieldType.METRIC)

    search_budget_lost_absolute_top_impression_share = GoogleField(name="SearchBudgetLostAbsoluteTopImpressionShare",
                                                                   field_name="SearchBudgetLostAbsoluteTopImpressionShare", field_type=GoogleFieldType.METRIC)

    search_budget_lost_top_impression_share = GoogleField(name="SearchBudgetLostTopImpressionShare", field_name="SearchBudgetLostTopImpressionShare",
                                                          field_type=GoogleFieldType.METRIC)

    search_exact_match_impression_share = GoogleField(name="SearchExactMatchImpressionShare", field_name="SearchExactMatchImpressionShare",
                                                      field_type=GoogleFieldType.METRIC)

    search_impression_share = GoogleField(name="SearchImpressionShare", field_name="SearchImpressionShare", field_type=GoogleFieldType.METRIC)

    search_rank_lost_absolute_top_impression_share = GoogleField(name="SearchRankLostAbsoluteTopImpressionShare",
                                                                 field_name="SearchRankLostAbsoluteTopImpressionShare", field_type=GoogleFieldType.METRIC)

    search_rank_lost_impression_share = GoogleField(name="SearchRankLostImpressionShare", field_name="SearchRankLostImpressionShare",
                                                    field_type=GoogleFieldType.METRIC)

    search_rank_lost_top_impression_share = GoogleField(name="SearchRankLostTopImpressionShare", field_name="SearchRankLostTopImpressionShare",
                                                        field_type=GoogleFieldType.METRIC)

    search_top_impression_share = GoogleField(name="SearchTopImpressionShare", field_name="SearchTopImpressionShare", field_type=GoogleFieldType.METRIC)

    average_frequency = GoogleField(name="AverageFrequency", field_name="AverageFrequency", field_type=GoogleFieldType.METRIC)

    content_budget_lost_impression_share = GoogleField(name="ContentBudgetLostImpressionShare", field_name="ContentBudgetLostImpressionShare",
                                                       field_type=GoogleFieldType.METRIC)

    impression_reach = GoogleField(name="ImpressionReach", field_name="ImpressionReach", field_type=GoogleFieldType.METRIC)

    invalid_click_rate = GoogleField(name="InvalidClickRate", field_name="InvalidClickRate", field_type=GoogleFieldType.METRIC, conversion_function=percentage_to_float)

    invalid_clicks = GoogleField(name="InvalidClicks", field_name="InvalidClicks", field_type=GoogleFieldType.METRIC)

    search_budget_lost_impression_share = GoogleField(name="SearchBudgetLostImpressionShare", field_name="SearchBudgetLostImpressionShare",
                                                      field_type=GoogleFieldType.METRIC)

    search_click_share = GoogleField(name="SearchClickShare", field_name="SearchClickShare", field_type=GoogleFieldType.METRIC)

    historical_creative_quality_score = GoogleField(name="HistoricalCreativeQualityScore", field_name="HistoricalCreativeQualityScore",
                                                    field_type=GoogleFieldType.METRIC)

    historical_landing_page_quality_score = GoogleField(name="HistoricalLandingPageQualityScore", field_name="HistoricalLandingPageQualityScore",
                                                        field_type=GoogleFieldType.METRIC)

    historical_quality_score = GoogleField(name="HistoricalQualityScore", field_name="HistoricalQualityScore", field_type=GoogleFieldType.METRIC)

    historical_search_predicted_ctr = GoogleField(name="HistoricalSearchPredictedCtr", field_name="HistoricalSearchPredictedCtr",
                                                  field_type=GoogleFieldType.METRIC)
