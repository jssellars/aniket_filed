from Core.Metadata.Columns.ViewColumns.ViewColumn import ViewColumn
from Core.Tools.Misc.Autoincrement import Autoincrement
from GoogleTuring.Api.Catalogs.Columns.GoogleMetadataColumnsPool import GoogleMetadataColumnsPool
from GoogleTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnCategory import ViewColumnCategory
from GoogleTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnType import ViewColumnType


class ViewColumnsMaster:
    __id = Autoincrement(0)
    accent_color = ViewColumn(__id.increment_as_string(), display_name='Accent color',
                              primary_value=GoogleMetadataColumnsPool.accent_color, type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    account_currency_code = ViewColumn(__id.increment_as_string(), display_name='Account currency code',
                                       primary_value=GoogleMetadataColumnsPool.account_currency_code,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    account_time_zone = ViewColumn(__id.increment_as_string(), display_name='Account time zone',
                                   primary_value=GoogleMetadataColumnsPool.account_time_zone,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    ad_group_status = ViewColumn(__id.increment_as_string(), display_name='Status',
                                 primary_value=GoogleMetadataColumnsPool.ad_group_status,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    enable_pause_ad_group = ViewColumn(__id.increment_as_string(), display_name='Enable/Pause',
                                       primary_value=GoogleMetadataColumnsPool.ad_group_status,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    ad_strength_info = ViewColumn(__id.increment_as_string(), display_name='Ad strength info',
                                  primary_value=GoogleMetadataColumnsPool.ad_strength_info,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    ad_type = ViewColumn(__id.increment_as_string(), display_name='Ad type',
                         primary_value=GoogleMetadataColumnsPool.ad_type, type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    allow_flexible_color = ViewColumn(__id.increment_as_string(), display_name='Allow flexible color',
                                      primary_value=GoogleMetadataColumnsPool.allow_flexible_color,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    automated = ViewColumn(__id.increment_as_string(), display_name='Automated',
                           primary_value=GoogleMetadataColumnsPool.automated, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    base_ad_group_id = ViewColumn(__id.increment_as_string(), display_name='Base ad group id',
                                  primary_value=GoogleMetadataColumnsPool.base_ad_group_id,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    base_campaignId = ViewColumn(__id.increment_as_string(), display_name='Base campaign id',
                                 primary_value=GoogleMetadataColumnsPool.base_campaignId,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    business_name = ViewColumn(__id.increment_as_string(), display_name='Business name',
                               primary_value=GoogleMetadataColumnsPool.business_name, type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    call_only_phone_number = ViewColumn(__id.increment_as_string(), display_name='Call only phone number',
                                        primary_value=GoogleMetadataColumnsPool.call_only_phone_number,
                                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                        actions=[])

    call_to_action_text = ViewColumn(__id.increment_as_string(), display_name='Call to action text',
                                     primary_value=GoogleMetadataColumnsPool.call_to_action_text,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    campaign_id = ViewColumn(__id.increment_as_string(), display_name='Campaign id',
                             primary_value=GoogleMetadataColumnsPool.campaign_id, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    campaign_name = ViewColumn(__id.increment_as_string(), display_name='Campaign',
                               primary_value=GoogleMetadataColumnsPool.campaign_name, type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    campaign_status = ViewColumn(__id.increment_as_string(), display_name='Status',
                                 primary_value=GoogleMetadataColumnsPool.campaign_status,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    enable_pause_campaign = ViewColumn(__id.increment_as_string(), display_name='Enable/Pause',
                                       primary_value=GoogleMetadataColumnsPool.campaign_status,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    combined_approval_status = ViewColumn(__id.increment_as_string(), display_name='Combined approval status',
                                          primary_value=GoogleMetadataColumnsPool.combined_approval_status,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    conversion_adjustment = ViewColumn(__id.increment_as_string(), display_name='Conversion adjustment',
                                       primary_value=GoogleMetadataColumnsPool.conversion_adjustment,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    creative_destination_url = ViewColumn(__id.increment_as_string(), display_name='Creative destination url',
                                          primary_value=GoogleMetadataColumnsPool.creative_destination_url,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    creative_final_app_urls = ViewColumn(__id.increment_as_string(), display_name='Creative final app urls',
                                         primary_value=GoogleMetadataColumnsPool.creative_final_app_urls,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    creative_final_mobile_urls = ViewColumn(__id.increment_as_string(), display_name='Creative final mobile urls',
                                            primary_value=GoogleMetadataColumnsPool.creative_final_mobile_urls,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[])

    creative_final_urls = ViewColumn(__id.increment_as_string(), display_name='Creative final urls',
                                     primary_value=GoogleMetadataColumnsPool.creative_final_urls,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    creative_final_url_suffix = ViewColumn(__id.increment_as_string(), display_name='Creative final url suffix',
                                           primary_value=GoogleMetadataColumnsPool.creative_final_url_suffix,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[])

    creative_tracking_url_template = ViewColumn(__id.increment_as_string(),
                                                display_name='Creative tracking url template',
                                                primary_value=GoogleMetadataColumnsPool.creative_tracking_url_template,
                                                type_id=ViewColumnType.text.id,
                                                category_id=ViewColumnCategory.common.id, actions=[])

    creative_url_custom_parameters = ViewColumn(__id.increment_as_string(),
                                                display_name='Creative url custom parameters',
                                                primary_value=GoogleMetadataColumnsPool.creative_url_custom_parameters,
                                                type_id=ViewColumnType.text.id,
                                                category_id=ViewColumnCategory.common.id, actions=[])

    customer_descriptive_name = ViewColumn(__id.increment_as_string(), display_name='Customer descriptive name',
                                           primary_value=GoogleMetadataColumnsPool.customer_descriptive_name,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[])

    description = ViewColumn(__id.increment_as_string(), display_name='Description',
                             primary_value=GoogleMetadataColumnsPool.description, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    description_1 = ViewColumn(__id.increment_as_string(), display_name='Description 1',
                               primary_value=GoogleMetadataColumnsPool.description_1, type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    description_2 = ViewColumn(__id.increment_as_string(), display_name='Description 2',
                               primary_value=GoogleMetadataColumnsPool.description_2, type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    device_preference = ViewColumn(__id.increment_as_string(), display_name='Device preference',
                                   primary_value=GoogleMetadataColumnsPool.device_preference,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    display_url = ViewColumn(__id.increment_as_string(), display_name='Display url',
                             primary_value=GoogleMetadataColumnsPool.display_url, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    enhanced_display_creative_landscape_logo_image_media_id = ViewColumn(__id.increment_as_string(),
                                                                         display_name='Enhanced display creative landscape logo image media id',
                                                                         primary_value=GoogleMetadataColumnsPool.enhanced_display_creative_landscape_logo_image_media_id,
                                                                         type_id=ViewColumnType.text.id,
                                                                         category_id=ViewColumnCategory.common.id,
                                                                         actions=[])

    enhanced_display_creative_logo_image_media_id = ViewColumn(__id.increment_as_string(),
                                                               display_name='Enhanced display creative logo image media id',
                                                               primary_value=GoogleMetadataColumnsPool.enhanced_display_creative_logo_image_media_id,
                                                               type_id=ViewColumnType.text.id,
                                                               category_id=ViewColumnCategory.common.id, actions=[])

    enhanced_display_creative_marketing_image_media_id = ViewColumn(__id.increment_as_string(),
                                                                    display_name='Enhanced display creative marketing image media id',
                                                                    primary_value=GoogleMetadataColumnsPool.enhanced_display_creative_marketing_image_media_id,
                                                                    type_id=ViewColumnType.text.id,
                                                                    category_id=ViewColumnCategory.common.id,
                                                                    actions=[])

    enhanced_display_creative_marketing_image_square_media_id = ViewColumn(__id.increment_as_string(),
                                                                           display_name='Enhanced display creative marketing image square media id',
                                                                           primary_value=GoogleMetadataColumnsPool.enhanced_display_creative_marketing_image_square_media_id,
                                                                           type_id=ViewColumnType.text.id,
                                                                           category_id=ViewColumnCategory.common.id,
                                                                           actions=[])

    expanded_dynamic_search_creative_description_2 = ViewColumn(__id.increment_as_string(),
                                                                display_name='Expanded dynamic search creative description 2',
                                                                primary_value=GoogleMetadataColumnsPool.expanded_dynamic_search_creative_description_2,
                                                                type_id=ViewColumnType.text.id,
                                                                category_id=ViewColumnCategory.common.id, actions=[])

    expanded_text_ad_description_2 = ViewColumn(__id.increment_as_string(),
                                                display_name='Expanded text ad description 2',
                                                primary_value=GoogleMetadataColumnsPool.expanded_text_ad_description_2,
                                                type_id=ViewColumnType.text.id,
                                                category_id=ViewColumnCategory.common.id, actions=[])

    expanded_text_ad_headline_part_3 = ViewColumn(__id.increment_as_string(),
                                                  display_name='Expanded text ad headline part 3',
                                                  primary_value=GoogleMetadataColumnsPool.expanded_text_ad_headline_part_3,
                                                  type_id=ViewColumnType.text.id,
                                                  category_id=ViewColumnCategory.common.id, actions=[])

    external_customer_id = ViewColumn(__id.increment_as_string(), display_name='External customer id',
                                      primary_value=GoogleMetadataColumnsPool.external_customer_id,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    format_setting = ViewColumn(__id.increment_as_string(), display_name='Format setting',
                                primary_value=GoogleMetadataColumnsPool.format_setting, type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    gmail_creative_header_image_media_id = ViewColumn(__id.increment_as_string(),
                                                      display_name='Gmail creative header image media id',
                                                      primary_value=GoogleMetadataColumnsPool.gmail_creative_header_image_media_id,
                                                      type_id=ViewColumnType.text.id,
                                                      category_id=ViewColumnCategory.common.id, actions=[])

    gmail_creative_logo_image_media_id = ViewColumn(__id.increment_as_string(),
                                                    display_name='Gmail creative logo image media id',
                                                    primary_value=GoogleMetadataColumnsPool.gmail_creative_logo_image_media_id,
                                                    type_id=ViewColumnType.text.id,
                                                    category_id=ViewColumnCategory.common.id, actions=[])

    gmail_creative_marketing_image_media_id = ViewColumn(__id.increment_as_string(),
                                                         display_name='Gmail creative marketing image media id',
                                                         primary_value=GoogleMetadataColumnsPool.gmail_creative_marketing_image_media_id,
                                                         type_id=ViewColumnType.text.id,
                                                         category_id=ViewColumnCategory.common.id, actions=[])

    gmail_teaser_business_name = ViewColumn(__id.increment_as_string(), display_name='Gmail teaser business name',
                                            primary_value=GoogleMetadataColumnsPool.gmail_teaser_business_name,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[])

    gmail_teaser_description = ViewColumn(__id.increment_as_string(), display_name='Gmail teaser description',
                                          primary_value=GoogleMetadataColumnsPool.gmail_teaser_description,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    gmail_teaser_headline = ViewColumn(__id.increment_as_string(), display_name='Gmail teaser headline',
                                       primary_value=GoogleMetadataColumnsPool.gmail_teaser_headline,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    headline = ViewColumn(__id.increment_as_string(), display_name='Headline',
                          primary_value=GoogleMetadataColumnsPool.headline, type_id=ViewColumnType.text.id,
                          category_id=ViewColumnCategory.common.id, actions=[])

    headline_part_1 = ViewColumn(__id.increment_as_string(), display_name='Headline part 1',
                                 primary_value=GoogleMetadataColumnsPool.headline_part_1,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    headline_part_2 = ViewColumn(__id.increment_as_string(), display_name='Headline part 2',
                                 primary_value=GoogleMetadataColumnsPool.headline_part_2,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    ad_name = ViewColumn(__id.increment_as_string(), display_name='Ad name',
                         primary_value=GoogleMetadataColumnsPool.ad_name, type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    id = ViewColumn(__id.increment_as_string(), display_name='Id', primary_value=GoogleMetadataColumnsPool.id,
                    type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                    actions=[])

    ad_id = ViewColumn(__id.increment_as_string(), display_name='Ad id', primary_value=GoogleMetadataColumnsPool.ad_id,
                       type_id=ViewColumnType.text.id,
                       category_id=ViewColumnCategory.common.id, actions=[])

    image_ad_url = ViewColumn(__id.increment_as_string(), display_name='Image ad url',
                              primary_value=GoogleMetadataColumnsPool.image_ad_url, type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    image_creative_image_height = ViewColumn(__id.increment_as_string(), display_name='Image creative image height',
                                             primary_value=GoogleMetadataColumnsPool.image_creative_image_height,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    image_creative_image_width = ViewColumn(__id.increment_as_string(), display_name='Image creative image width',
                                            primary_value=GoogleMetadataColumnsPool.image_creative_image_width,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[])

    image_creative_mime_type = ViewColumn(__id.increment_as_string(), display_name='Image creative mime type',
                                          primary_value=GoogleMetadataColumnsPool.image_creative_mime_type,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    image_creative_name = ViewColumn(__id.increment_as_string(), display_name='Image creative name',
                                     primary_value=GoogleMetadataColumnsPool.image_creative_name,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    is_negative = ViewColumn(__id.increment_as_string(), display_name='Is negative',
                             primary_value=GoogleMetadataColumnsPool.is_negative, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    label_ids = ViewColumn(__id.increment_as_string(), display_name='Label ids',
                           primary_value=GoogleMetadataColumnsPool.label_ids, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    labels = ViewColumn(__id.increment_as_string(), display_name='Labels',
                        primary_value=GoogleMetadataColumnsPool.labels, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    long_headline = ViewColumn(__id.increment_as_string(), display_name='Long headline',
                               primary_value=GoogleMetadataColumnsPool.long_headline, type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    main_color = ViewColumn(__id.increment_as_string(), display_name='Main color',
                            primary_value=GoogleMetadataColumnsPool.main_color, type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    marketing_image_call_to_action_text = ViewColumn(__id.increment_as_string(),
                                                     display_name='Marketing image call to action text',
                                                     primary_value=GoogleMetadataColumnsPool.marketing_image_call_to_action_text,
                                                     type_id=ViewColumnType.text.id,
                                                     category_id=ViewColumnCategory.common.id, actions=[])

    marketing_image_call_to_action_text_color = ViewColumn(__id.increment_as_string(),
                                                           display_name='Marketing image call to action text color',
                                                           primary_value=GoogleMetadataColumnsPool.marketing_image_call_to_action_text_color,
                                                           type_id=ViewColumnType.text.id,
                                                           category_id=ViewColumnCategory.common.id, actions=[])

    marketing_image_description = ViewColumn(__id.increment_as_string(), display_name='Marketing image description',
                                             primary_value=GoogleMetadataColumnsPool.marketing_image_description,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    marketing_image_headline = ViewColumn(__id.increment_as_string(), display_name='Marketing image headline',
                                          primary_value=GoogleMetadataColumnsPool.marketing_image_headline,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    multi_asset_responsive_display_ad_accent_color = ViewColumn(__id.increment_as_string(),
                                                                display_name='Multi asset responsive display ad accent color',
                                                                primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_accent_color,
                                                                type_id=ViewColumnType.text.id,
                                                                category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_allow_flexible_color = ViewColumn(__id.increment_as_string(),
                                                                        display_name='Multi asset responsive display ad allow flexible color',
                                                                        primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_allow_flexible_color,
                                                                        type_id=ViewColumnType.text.id,
                                                                        category_id=ViewColumnCategory.common.id,
                                                                        actions=[])

    multi_asset_responsive_display_ad_business_name = ViewColumn(__id.increment_as_string(),
                                                                 display_name='Multi asset responsive display ad business name',
                                                                 primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_business_name,
                                                                 type_id=ViewColumnType.text.id,
                                                                 category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_call_to_action_text = ViewColumn(__id.increment_as_string(),
                                                                       display_name='Multi asset responsive display ad call to action text',
                                                                       primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_call_to_action_text,
                                                                       type_id=ViewColumnType.text.id,
                                                                       category_id=ViewColumnCategory.common.id,
                                                                       actions=[])

    multi_asset_responsive_display_ad_descriptions = ViewColumn(__id.increment_as_string(),
                                                                display_name='Multi asset responsive display ad descriptions',
                                                                primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_descriptions,
                                                                type_id=ViewColumnType.text.id,
                                                                category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_dynamic_settings_price_prefix = ViewColumn(__id.increment_as_string(),
                                                                                 display_name='Multi asset responsive display ad dynamic settings price prefix',
                                                                                 primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_dynamic_settings_price_prefix,
                                                                                 type_id=ViewColumnType.text.id,
                                                                                 category_id=ViewColumnCategory.common.id,
                                                                                 actions=[])

    multi_asset_responsive_display_ad_dynamic_settings_promo_text = ViewColumn(__id.increment_as_string(),
                                                                               display_name='Multi asset responsive display ad dynamic settings promo text',
                                                                               primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_dynamic_settings_promo_text,
                                                                               type_id=ViewColumnType.text.id,
                                                                               category_id=ViewColumnCategory.common.id,
                                                                               actions=[])

    multi_asset_responsive_display_ad_format_setting = ViewColumn(__id.increment_as_string(),
                                                                  display_name='Multi asset responsive display ad format setting',
                                                                  primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_format_setting,
                                                                  type_id=ViewColumnType.text.id,
                                                                  category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_headlines = ViewColumn(__id.increment_as_string(),
                                                             display_name='Multi asset responsive display ad headlines',
                                                             primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_headlines,
                                                             type_id=ViewColumnType.text.id,
                                                             category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_landscape_logo_images = ViewColumn(__id.increment_as_string(),
                                                                         display_name='Multi asset responsive display ad landscape logo images',
                                                                         primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_landscape_logo_images,
                                                                         type_id=ViewColumnType.text.id,
                                                                         category_id=ViewColumnCategory.common.id,
                                                                         actions=[])

    multi_asset_responsive_display_ad_logo_images = ViewColumn(__id.increment_as_string(),
                                                               display_name='Multi asset responsive display ad logo images',
                                                               primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_logo_images,
                                                               type_id=ViewColumnType.text.id,
                                                               category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_long_headline = ViewColumn(__id.increment_as_string(),
                                                                 display_name='Multi asset responsive display ad long headline',
                                                                 primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_long_headline,
                                                                 type_id=ViewColumnType.text.id,
                                                                 category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_main_color = ViewColumn(__id.increment_as_string(),
                                                              display_name='Multi asset responsive display ad main color',
                                                              primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_main_color,
                                                              type_id=ViewColumnType.text.id,
                                                              category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_marketing_images = ViewColumn(__id.increment_as_string(),
                                                                    display_name='Multi asset responsive display ad marketing images',
                                                                    primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_marketing_images,
                                                                    type_id=ViewColumnType.text.id,
                                                                    category_id=ViewColumnCategory.common.id,
                                                                    actions=[])

    multi_asset_responsive_display_ad_square_marketing_images = ViewColumn(__id.increment_as_string(),
                                                                           display_name='Multi asset responsive display ad square marketing images',
                                                                           primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_square_marketing_images,
                                                                           type_id=ViewColumnType.text.id,
                                                                           category_id=ViewColumnCategory.common.id,
                                                                           actions=[])

    multi_asset_responsive_display_ad_you_tube_videos = ViewColumn(__id.increment_as_string(),
                                                                   display_name='Multi asset responsive display ad you tube videos',
                                                                   primary_value=GoogleMetadataColumnsPool.multi_asset_responsive_display_ad_you_tube_videos,
                                                                   type_id=ViewColumnType.text.id,
                                                                   category_id=ViewColumnCategory.common.id,
                                                                   actions=[])

    path_1 = ViewColumn(__id.increment_as_string(), display_name='Path 1',
                        primary_value=GoogleMetadataColumnsPool.path_1, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    path_2 = ViewColumn(__id.increment_as_string(), display_name='Path 2',
                        primary_value=GoogleMetadataColumnsPool.path_2, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    policy_summary = ViewColumn(__id.increment_as_string(), display_name='Policy summary',
                                primary_value=GoogleMetadataColumnsPool.policy_summary, type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    price_prefix = ViewColumn(__id.increment_as_string(), display_name='Price prefix',
                              primary_value=GoogleMetadataColumnsPool.price_prefix, type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    promo_text = ViewColumn(__id.increment_as_string(), display_name='Promo text',
                            primary_value=GoogleMetadataColumnsPool.promo_text, type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    responsive_search_ad_descriptions = ViewColumn(__id.increment_as_string(),
                                                   display_name='Responsive search ad descriptions',
                                                   primary_value=GoogleMetadataColumnsPool.responsive_search_ad_descriptions,
                                                   type_id=ViewColumnType.text.id,
                                                   category_id=ViewColumnCategory.common.id, actions=[])

    responsive_search_ad_headlines = ViewColumn(__id.increment_as_string(),
                                                display_name='Responsive search ad headlines',
                                                primary_value=GoogleMetadataColumnsPool.responsive_search_ad_headlines,
                                                type_id=ViewColumnType.text.id,
                                                category_id=ViewColumnCategory.common.id, actions=[])

    responsive_search_ad_path_1 = ViewColumn(__id.increment_as_string(), display_name='Responsive search ad path 1',
                                             primary_value=GoogleMetadataColumnsPool.responsive_search_ad_path_1,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    responsive_search_ad_path_2 = ViewColumn(__id.increment_as_string(), display_name='Responsive search ad path 2',
                                             primary_value=GoogleMetadataColumnsPool.responsive_search_ad_path_2,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    short_headline = ViewColumn(__id.increment_as_string(), display_name='Short headline',
                                primary_value=GoogleMetadataColumnsPool.short_headline,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    status = ViewColumn(__id.increment_as_string(), display_name='Status',
                        primary_value=GoogleMetadataColumnsPool.status, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    enable_pause_keyword = ViewColumn(__id.increment_as_string(), display_name='Enable/Pause',
                                      primary_value=GoogleMetadataColumnsPool.status,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    enable_pause_ad = ViewColumn(__id.increment_as_string(), display_name='Enable/Pause',
                                 primary_value=GoogleMetadataColumnsPool.status,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    system_managed_entity_source = ViewColumn(__id.increment_as_string(), display_name='System managed entity source',
                                              primary_value=GoogleMetadataColumnsPool.system_managed_entity_source,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    universal_app_ad_descriptions = ViewColumn(__id.increment_as_string(),
                                               display_name='Universal app ad descriptions',
                                               primary_value=GoogleMetadataColumnsPool.universal_app_ad_descriptions,
                                               type_id=ViewColumnType.text.id,
                                               category_id=ViewColumnCategory.common.id, actions=[])

    universal_app_ad_headlines = ViewColumn(__id.increment_as_string(), display_name='Universal app ad headlines',
                                            primary_value=GoogleMetadataColumnsPool.universal_app_ad_headlines,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[])

    universal_app_ad_html_5_media_bundles = ViewColumn(__id.increment_as_string(),
                                                       display_name='Universal app ad html 5 media bundles',
                                                       primary_value=GoogleMetadataColumnsPool.universal_app_ad_html_5_media_bundles,
                                                       type_id=ViewColumnType.text.id,
                                                       category_id=ViewColumnCategory.common.id, actions=[])

    universal_app_ad_images = ViewColumn(__id.increment_as_string(), display_name='Universal app ad images',
                                         primary_value=GoogleMetadataColumnsPool.universal_app_ad_images,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    universal_app_ad_mandatory_ad_text = ViewColumn(__id.increment_as_string(),
                                                    display_name='Universal app ad mandatory ad text',
                                                    primary_value=GoogleMetadataColumnsPool.universal_app_ad_mandatory_ad_text,
                                                    type_id=ViewColumnType.text.id,
                                                    category_id=ViewColumnCategory.common.id, actions=[])

    universal_app_ad_you_tube_videos = ViewColumn(__id.increment_as_string(),
                                                  display_name='Universal app ad you tube videos',
                                                  primary_value=GoogleMetadataColumnsPool.universal_app_ad_you_tube_videos,
                                                  type_id=ViewColumnType.text.id,
                                                  category_id=ViewColumnCategory.common.id, actions=[])

    account_descriptive_name = ViewColumn(__id.increment_as_string(), display_name='Account descriptive name',
                                          primary_value=GoogleMetadataColumnsPool.account_descriptive_name,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    ad_group_desktop_bid_modifier = ViewColumn(__id.increment_as_string(),
                                               display_name='Ad group desktop bid modifier',
                                               primary_value=GoogleMetadataColumnsPool.ad_group_desktop_bid_modifier,
                                               type_id=ViewColumnType.text.id,
                                               category_id=ViewColumnCategory.common.id, actions=[])

    ad_group_id = ViewColumn(__id.increment_as_string(), display_name='Ad group id',
                             primary_value=GoogleMetadataColumnsPool.ad_group_id, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    ad_group_mobile_bid_modifier = ViewColumn(__id.increment_as_string(), display_name='Ad group mobile bid modifier',
                                              primary_value=GoogleMetadataColumnsPool.ad_group_mobile_bid_modifier,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    ad_group_name = ViewColumn(__id.increment_as_string(), display_name='Ad group',
                               primary_value=GoogleMetadataColumnsPool.ad_group_name, type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    ad_group_tablet_bid_modifier = ViewColumn(__id.increment_as_string(), display_name='Ad group tablet bid modifier',
                                              primary_value=GoogleMetadataColumnsPool.ad_group_tablet_bid_modifier,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    ad_group_type = ViewColumn(__id.increment_as_string(), display_name='Ad group type',
                               primary_value=GoogleMetadataColumnsPool.ad_group_type, type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    ad_rotation_mode = ViewColumn(__id.increment_as_string(), display_name='Ad rotation mode',
                                  primary_value=GoogleMetadataColumnsPool.ad_rotation_mode,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    bidding_strategy_id = ViewColumn(__id.increment_as_string(), display_name='Bidding strategy id',
                                     primary_value=GoogleMetadataColumnsPool.bidding_strategy_id,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    bidding_strategy_name = ViewColumn(__id.increment_as_string(), display_name='Bidding strategy name',
                                       primary_value=GoogleMetadataColumnsPool.bidding_strategy_name,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    bidding_strategy_source = ViewColumn(__id.increment_as_string(), display_name='Bidding strategy source',
                                         primary_value=GoogleMetadataColumnsPool.bidding_strategy_source,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    bidding_strategy_type = ViewColumn(__id.increment_as_string(), display_name='Bidding strategy type',
                                       primary_value=GoogleMetadataColumnsPool.bidding_strategy_type,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    content_bid_criterion_type_group = ViewColumn(__id.increment_as_string(),
                                                  display_name='Content bid criterion type group',
                                                  primary_value=GoogleMetadataColumnsPool.content_bid_criterion_type_group,
                                                  type_id=ViewColumnType.text.id,
                                                  category_id=ViewColumnCategory.common.id, actions=[])

    cpc_bid = ViewColumn(__id.increment_as_string(), display_name='Default max. CPC',
                         primary_value=GoogleMetadataColumnsPool.cpc_bid,
                         type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    max_cpc = ViewColumn(__id.increment_as_string(), display_name='Max. CPC',
                         primary_value=GoogleMetadataColumnsPool.cpc_bid, type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    cpm_bid = ViewColumn(__id.increment_as_string(), display_name='Cpm bid',
                         primary_value=GoogleMetadataColumnsPool.cpm_bid, type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    cpv_bid = ViewColumn(__id.increment_as_string(), display_name='Max CPV',
                         primary_value=GoogleMetadataColumnsPool.cpv_bid, type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    effective_target_roas = ViewColumn(__id.increment_as_string(), display_name='Effective target roas',
                                       primary_value=GoogleMetadataColumnsPool.effective_target_roas,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    effective_target_roas_source = ViewColumn(__id.increment_as_string(), display_name='Effective target roas source',
                                              primary_value=GoogleMetadataColumnsPool.effective_target_roas_source,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    enhanced_cpc_enabled = ViewColumn(__id.increment_as_string(), display_name='Enhanced cpc enabled',
                                      primary_value=GoogleMetadataColumnsPool.enhanced_cpc_enabled,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    final_url_suffix = ViewColumn(__id.increment_as_string(), display_name='Final url suffix',
                                  primary_value=GoogleMetadataColumnsPool.final_url_suffix,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    target_cpa = ViewColumn(__id.increment_as_string(), display_name='Target cpa',
                            primary_value=GoogleMetadataColumnsPool.target_cpa, type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    target_cpa_bid_source = ViewColumn(__id.increment_as_string(), display_name='Target cpa bid source',
                                       primary_value=GoogleMetadataColumnsPool.target_cpa_bid_source,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    tracking_url_template = ViewColumn(__id.increment_as_string(), display_name='Tracking url template',
                                       primary_value=GoogleMetadataColumnsPool.tracking_url_template,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    url_custom_parameters = ViewColumn(__id.increment_as_string(), display_name='Url custom parameters',
                                       primary_value=GoogleMetadataColumnsPool.url_custom_parameters,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    advertising_channel_sub_type = ViewColumn(__id.increment_as_string(), display_name='Advertising channel sub type',
                                              primary_value=GoogleMetadataColumnsPool.advertising_channel_sub_type,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    advertising_channel_type = ViewColumn(__id.increment_as_string(), display_name='Advertising channel type',
                                          primary_value=GoogleMetadataColumnsPool.advertising_channel_type,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    amount = ViewColumn(__id.increment_as_string(), display_name='Budget',
                        primary_value=GoogleMetadataColumnsPool.amount, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    budget_id = ViewColumn(__id.increment_as_string(), display_name='Budget id',
                           primary_value=GoogleMetadataColumnsPool.budget_id, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    campaign_desktop_bid_modifier = ViewColumn(__id.increment_as_string(),
                                               display_name='Campaign desktop bid modifier',
                                               primary_value=GoogleMetadataColumnsPool.campaign_desktop_bid_modifier,
                                               type_id=ViewColumnType.text.id,
                                               category_id=ViewColumnCategory.common.id, actions=[])

    campaign_group_id = ViewColumn(__id.increment_as_string(), display_name='Campaign group id',
                                   primary_value=GoogleMetadataColumnsPool.campaign_group_id,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    campaign_mobile_bid_modifier = ViewColumn(__id.increment_as_string(), display_name='Campaign mobile bid modifier',
                                              primary_value=GoogleMetadataColumnsPool.campaign_mobile_bid_modifier,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    campaign_tablet_bid_modifier = ViewColumn(__id.increment_as_string(), display_name='Campaign tablet bid modifier',
                                              primary_value=GoogleMetadataColumnsPool.campaign_tablet_bid_modifier,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    campaign_trial_type = ViewColumn(__id.increment_as_string(), display_name='Campaign trial type',
                                     primary_value=GoogleMetadataColumnsPool.campaign_trial_type,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    end_date = ViewColumn(__id.increment_as_string(), display_name='End date',
                          primary_value=GoogleMetadataColumnsPool.end_date, type_id=ViewColumnType.text.id,
                          category_id=ViewColumnCategory.common.id, actions=[])

    has_recommended_budget = ViewColumn(__id.increment_as_string(), display_name='Has recommended budget',
                                        primary_value=GoogleMetadataColumnsPool.has_recommended_budget,
                                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                        actions=[])

    is_budget_explicitly_shared = ViewColumn(__id.increment_as_string(), display_name='Is budget explicitly shared',
                                             primary_value=GoogleMetadataColumnsPool.is_budget_explicitly_shared,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    maximize_conversion_value_target_roas = ViewColumn(__id.increment_as_string(),
                                                       display_name='Maximize conversion value target roas',
                                                       primary_value=GoogleMetadataColumnsPool.maximize_conversion_value_target_roas,
                                                       type_id=ViewColumnType.text.id,
                                                       category_id=ViewColumnCategory.common.id, actions=[])

    period = ViewColumn(__id.increment_as_string(), display_name='Period',
                        primary_value=GoogleMetadataColumnsPool.period, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    recommended_budget_amount = ViewColumn(__id.increment_as_string(), display_name='Recommended budget amount',
                                           primary_value=GoogleMetadataColumnsPool.recommended_budget_amount,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[])

    serving_status = ViewColumn(__id.increment_as_string(), display_name='Serving status',
                                primary_value=GoogleMetadataColumnsPool.serving_status, type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    start_date = ViewColumn(__id.increment_as_string(), display_name='Start date',
                            primary_value=GoogleMetadataColumnsPool.start_date, type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    total_amount = ViewColumn(__id.increment_as_string(), display_name='Total amount',
                              primary_value=GoogleMetadataColumnsPool.total_amount, type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    approval_status = ViewColumn(__id.increment_as_string(), display_name='Policy Details',
                                 primary_value=GoogleMetadataColumnsPool.approval_status,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    cpc_bid_source = ViewColumn(__id.increment_as_string(), display_name='Cpc bid source',
                                primary_value=GoogleMetadataColumnsPool.cpc_bid_source, type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    creative_quality_score = ViewColumn(__id.increment_as_string(), display_name='Creative quality score',
                                        primary_value=GoogleMetadataColumnsPool.creative_quality_score,
                                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                        actions=[])

    criteria = ViewColumn(__id.increment_as_string(), display_name='Criteria',
                          primary_value=GoogleMetadataColumnsPool.criteria, type_id=ViewColumnType.text.id,
                          category_id=ViewColumnCategory.common.id, actions=[])

    gender = ViewColumn(__id.increment_as_string(), display_name='Gender',
                        primary_value=GoogleMetadataColumnsPool.gender, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    age_range = ViewColumn(__id.increment_as_string(), display_name='Age range',
                           primary_value=GoogleMetadataColumnsPool.age_range, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    keywords = ViewColumn(__id.increment_as_string(), display_name='Keyword',
                          primary_value=GoogleMetadataColumnsPool.keywords, type_id=ViewColumnType.text.id,
                          category_id=ViewColumnCategory.common.id, actions=[])

    criteria_destination_url = ViewColumn(__id.increment_as_string(), display_name='Criteria destination url',
                                          primary_value=GoogleMetadataColumnsPool.criteria_destination_url,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    estimated_add_clicks_at_first_position_cpc = ViewColumn(__id.increment_as_string(),
                                                            display_name='Estimated add clicks at first position cpc',
                                                            primary_value=GoogleMetadataColumnsPool.estimated_add_clicks_at_first_position_cpc,
                                                            type_id=ViewColumnType.text.id,
                                                            category_id=ViewColumnCategory.common.id, actions=[])

    estimated_add_cost_at_first_position_cpc = ViewColumn(__id.increment_as_string(),
                                                          display_name='Estimated add cost at first position cpc',
                                                          primary_value=GoogleMetadataColumnsPool.estimated_add_cost_at_first_position_cpc,
                                                          type_id=ViewColumnType.text.id,
                                                          category_id=ViewColumnCategory.common.id, actions=[])

    final_app_urls = ViewColumn(__id.increment_as_string(), display_name='Final app urls',
                                primary_value=GoogleMetadataColumnsPool.final_app_urls, type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    final_mobile_urls = ViewColumn(__id.increment_as_string(), display_name='Final mobile urls',
                                   primary_value=GoogleMetadataColumnsPool.final_mobile_urls,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    final_urls = ViewColumn(__id.increment_as_string(), display_name='Final URL',
                            primary_value=GoogleMetadataColumnsPool.final_urls,
                            type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    first_page_cpc = ViewColumn(__id.increment_as_string(), display_name='First page cpc',
                                primary_value=GoogleMetadataColumnsPool.first_page_cpc, type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    first_position_cpc = ViewColumn(__id.increment_as_string(), display_name='First position cpc',
                                    primary_value=GoogleMetadataColumnsPool.first_position_cpc,
                                    type_id=ViewColumnType.text.id,
                                    category_id=ViewColumnCategory.common.id, actions=[])

    has_quality_score = ViewColumn(__id.increment_as_string(), display_name='Has quality score',
                                   primary_value=GoogleMetadataColumnsPool.has_quality_score,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    keyword_match_type = ViewColumn(__id.increment_as_string(), display_name='Keyword match type',
                                    primary_value=GoogleMetadataColumnsPool.keyword_match_type,
                                    type_id=ViewColumnType.text.id,
                                    category_id=ViewColumnCategory.common.id, actions=[])

    post_click_quality_score = ViewColumn(__id.increment_as_string(), display_name='Post click quality score',
                                          primary_value=GoogleMetadataColumnsPool.post_click_quality_score,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    quality_score = ViewColumn(__id.increment_as_string(), display_name='Quality score',
                               primary_value=GoogleMetadataColumnsPool.quality_score, type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    search_predicted_ctr = ViewColumn(__id.increment_as_string(), display_name='Search predicted ctr',
                                      primary_value=GoogleMetadataColumnsPool.search_predicted_ctr,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    system_serving_status = ViewColumn(__id.increment_as_string(), display_name='System serving status',
                                       primary_value=GoogleMetadataColumnsPool.system_serving_status,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    top_of_page_cpc = ViewColumn(__id.increment_as_string(), display_name='Top of page cpc',
                                 primary_value=GoogleMetadataColumnsPool.top_of_page_cpc,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    vertical_id = ViewColumn(__id.increment_as_string(), display_name='Vertical id',
                             primary_value=GoogleMetadataColumnsPool.vertical_id, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    city_name = ViewColumn(__id.increment_as_string(), display_name='City name',
                           primary_value=GoogleMetadataColumnsPool.city_name, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    country_name = ViewColumn(__id.increment_as_string(), display_name='Country name',
                              primary_value=GoogleMetadataColumnsPool.country_name, type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    is_targeting_location = ViewColumn(__id.increment_as_string(), display_name='Is targeting location',
                                       primary_value=GoogleMetadataColumnsPool.is_targeting_location,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    metro_criteria_id = ViewColumn(__id.increment_as_string(), display_name='Metro criteria id',
                                   primary_value=GoogleMetadataColumnsPool.metro_criteria_id,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    most_specific_criteria_id = ViewColumn(__id.increment_as_string(), display_name='Most specific criteria id',
                                           primary_value=GoogleMetadataColumnsPool.most_specific_criteria_id,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[])

    region_name = ViewColumn(__id.increment_as_string(), display_name='Region name',
                             primary_value=GoogleMetadataColumnsPool.region_name, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    base_campaign_id = ViewColumn(__id.increment_as_string(), display_name='Base campaign id',
                                  primary_value=GoogleMetadataColumnsPool.base_campaign_id,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    bid_modifier = ViewColumn(__id.increment_as_string(), display_name='Bid Adjust',
                              primary_value=GoogleMetadataColumnsPool.bid_modifier,
                              type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    cpm_bid_source = ViewColumn(__id.increment_as_string(), display_name='Cpm bid source',
                                primary_value=GoogleMetadataColumnsPool.cpm_bid_source, type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    is_restrict = ViewColumn(__id.increment_as_string(), display_name='Is restrict',
                             primary_value=GoogleMetadataColumnsPool.is_restrict, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    ad_network_type_1 = ViewColumn(__id.increment_as_string(), display_name='Ad network type 1',
                                   primary_value=GoogleMetadataColumnsPool.ad_network_type_1,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    ad_network_type_2 = ViewColumn(__id.increment_as_string(), display_name='Ad network type 2',
                                   primary_value=GoogleMetadataColumnsPool.ad_network_type_2,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    click_type = ViewColumn(__id.increment_as_string(), display_name='Click type',
                            primary_value=GoogleMetadataColumnsPool.click_type, type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    conversion_adjustment_lag_bucket = ViewColumn(__id.increment_as_string(),
                                                  display_name='Conversion adjustment lag bucket',
                                                  primary_value=GoogleMetadataColumnsPool.conversion_adjustment_lag_bucket,
                                                  type_id=ViewColumnType.text.id,
                                                  category_id=ViewColumnCategory.common.id, actions=[])

    conversion_lag_bucket = ViewColumn(__id.increment_as_string(), display_name='Conversion lag bucket',
                                       primary_value=GoogleMetadataColumnsPool.conversion_lag_bucket,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    conversion_tracker_id = ViewColumn(__id.increment_as_string(), display_name='Conversion tracker id',
                                       primary_value=GoogleMetadataColumnsPool.conversion_tracker_id,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    conversion_type_name = ViewColumn(__id.increment_as_string(), display_name='Conversion type name',
                                      primary_value=GoogleMetadataColumnsPool.conversion_type_name,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    criterion_id = ViewColumn(__id.increment_as_string(), display_name='Criterion id',
                              primary_value=GoogleMetadataColumnsPool.criterion_id, type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    criterion_type = ViewColumn(__id.increment_as_string(), display_name='Criterion type',
                                primary_value=GoogleMetadataColumnsPool.criterion_type, type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    date = ViewColumn(__id.increment_as_string(), display_name='Date', primary_value=GoogleMetadataColumnsPool.date,
                      type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                      actions=[])

    day_of_week = ViewColumn(__id.increment_as_string(), display_name='Day of week',
                             primary_value=GoogleMetadataColumnsPool.day_of_week, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    device = ViewColumn(__id.increment_as_string(), display_name='Device',
                        primary_value=GoogleMetadataColumnsPool.device, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    external_conversion_source = ViewColumn(__id.increment_as_string(), display_name='External conversion source',
                                            primary_value=GoogleMetadataColumnsPool.external_conversion_source,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[])

    month = ViewColumn(__id.increment_as_string(), display_name='Month', primary_value=GoogleMetadataColumnsPool.month,
                       type_id=ViewColumnType.text.id,
                       category_id=ViewColumnCategory.common.id, actions=[])

    month_of_year = ViewColumn(__id.increment_as_string(), display_name='Month of year',
                               primary_value=GoogleMetadataColumnsPool.month_of_year, type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    quarter = ViewColumn(__id.increment_as_string(), display_name='Quarter',
                         primary_value=GoogleMetadataColumnsPool.quarter, type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    slot = ViewColumn(__id.increment_as_string(), display_name='Slot', primary_value=GoogleMetadataColumnsPool.slot,
                      type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                      actions=[])

    week = ViewColumn(__id.increment_as_string(), display_name='Week', primary_value=GoogleMetadataColumnsPool.week,
                      type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                      actions=[])

    year = ViewColumn(__id.increment_as_string(), display_name='Year', primary_value=GoogleMetadataColumnsPool.year,
                      type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                      actions=[])

    hour_of_day = ViewColumn(__id.increment_as_string(), display_name='Hour of day',
                             primary_value=GoogleMetadataColumnsPool.hour_of_day, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    conversion_attribution_event_type = ViewColumn(__id.increment_as_string(),
                                                   display_name='Conversion attribution event type',
                                                   primary_value=GoogleMetadataColumnsPool.conversion_attribution_event_type,
                                                   type_id=ViewColumnType.text.id,
                                                   category_id=ViewColumnCategory.common.id, actions=[])

    ad_format = ViewColumn(__id.increment_as_string(), display_name='Ad format',
                           primary_value=GoogleMetadataColumnsPool.ad_format, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    location_type = ViewColumn(__id.increment_as_string(), display_name='Location type',
                               primary_value=GoogleMetadataColumnsPool.location_type, type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    conversion_category_name = ViewColumn(__id.increment_as_string(), display_name='Conversion category name',
                                          primary_value=GoogleMetadataColumnsPool.conversion_category_name,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    ad_group_id_segment = ViewColumn(__id.increment_as_string(), display_name='Ad group id segment',
                                     primary_value=GoogleMetadataColumnsPool.ad_group_id_segment,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    ad_group_name_segment = ViewColumn(__id.increment_as_string(), display_name='Ad group name segment',
                                       primary_value=GoogleMetadataColumnsPool.ad_group_name_segment,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    ad_group_status_segment = ViewColumn(__id.increment_as_string(), display_name='Ad group status segment',
                                         primary_value=GoogleMetadataColumnsPool.ad_group_status_segment,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    absolute_top_impression_percentage = ViewColumn(__id.increment_as_string(),
                                                    display_name='Absolute top impression percentage',
                                                    primary_value=GoogleMetadataColumnsPool.absolute_top_impression_percentage,
                                                    type_id=ViewColumnType.text.id,
                                                    category_id=ViewColumnCategory.common.id, actions=[])

    active_view_cpm = ViewColumn(__id.increment_as_string(), display_name='Active view cpm',
                                 primary_value=GoogleMetadataColumnsPool.active_view_cpm,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    active_view_ctr = ViewColumn(__id.increment_as_string(), display_name='Active view ctr',
                                 primary_value=GoogleMetadataColumnsPool.active_view_ctr,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    active_view_impressions = ViewColumn(__id.increment_as_string(), display_name='Active view impressions',
                                         primary_value=GoogleMetadataColumnsPool.active_view_impressions,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    active_view_measurability = ViewColumn(__id.increment_as_string(), display_name='Active view measurability',
                                           primary_value=GoogleMetadataColumnsPool.active_view_measurability,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[])

    active_view_measurable_cost = ViewColumn(__id.increment_as_string(), display_name='Active view measurable cost',
                                             primary_value=GoogleMetadataColumnsPool.active_view_measurable_cost,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    active_view_measurable_impressions = ViewColumn(__id.increment_as_string(),
                                                    display_name='Active view measurable impressions',
                                                    primary_value=GoogleMetadataColumnsPool.active_view_measurable_impressions,
                                                    type_id=ViewColumnType.text.id,
                                                    category_id=ViewColumnCategory.common.id, actions=[])

    active_view_viewability = ViewColumn(__id.increment_as_string(), display_name='Active view viewability',
                                         primary_value=GoogleMetadataColumnsPool.active_view_viewability,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    all_conversion_rate = ViewColumn(__id.increment_as_string(), display_name='All conversion rate',
                                     primary_value=GoogleMetadataColumnsPool.all_conversion_rate,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    all_conversions = ViewColumn(__id.increment_as_string(), display_name='All conversions',
                                 primary_value=GoogleMetadataColumnsPool.all_conversions,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    all_conversion_value = ViewColumn(__id.increment_as_string(), display_name='All conversion value',
                                      primary_value=GoogleMetadataColumnsPool.all_conversion_value,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    average_cost = ViewColumn(__id.increment_as_string(), display_name='Average cost',
                              primary_value=GoogleMetadataColumnsPool.average_cost, type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    average_cpc = ViewColumn(__id.increment_as_string(), display_name='Cpc',
                             primary_value=GoogleMetadataColumnsPool.average_cpc, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    average_cpe = ViewColumn(__id.increment_as_string(), display_name='Average cpe',
                             primary_value=GoogleMetadataColumnsPool.average_cpe, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    average_cpm = ViewColumn(__id.increment_as_string(), display_name='Cpm',
                             primary_value=GoogleMetadataColumnsPool.average_cpm, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    average_cpv = ViewColumn(__id.increment_as_string(), display_name='Average cpv',
                             primary_value=GoogleMetadataColumnsPool.average_cpv, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    average_pageviews = ViewColumn(__id.increment_as_string(), display_name='Average pageviews',
                                   primary_value=GoogleMetadataColumnsPool.average_pageviews,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    average_position = ViewColumn(__id.increment_as_string(), display_name='Average position',
                                  primary_value=GoogleMetadataColumnsPool.average_position,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    average_time_on_site = ViewColumn(__id.increment_as_string(), display_name='Average time on site',
                                      primary_value=GoogleMetadataColumnsPool.average_time_on_site,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    bounce_rate = ViewColumn(__id.increment_as_string(), display_name='Bounce rate',
                             primary_value=GoogleMetadataColumnsPool.bounce_rate, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    click_assisted_conversions = ViewColumn(__id.increment_as_string(), display_name='Click assisted conversions',
                                            primary_value=GoogleMetadataColumnsPool.click_assisted_conversions,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[])

    click_assisted_conversions_over_last_click_conversions = ViewColumn(__id.increment_as_string(),
                                                                        display_name='Click assisted conversions over last click conversions',
                                                                        primary_value=GoogleMetadataColumnsPool.click_assisted_conversions_over_last_click_conversions,
                                                                        type_id=ViewColumnType.text.id,
                                                                        category_id=ViewColumnCategory.common.id,
                                                                        actions=[])

    click_assisted_conversion_value = ViewColumn(__id.increment_as_string(),
                                                 display_name='Click assisted conversion value',
                                                 primary_value=GoogleMetadataColumnsPool.click_assisted_conversion_value,
                                                 type_id=ViewColumnType.text.id,
                                                 category_id=ViewColumnCategory.common.id, actions=[])

    clicks = ViewColumn(__id.increment_as_string(), display_name='Clicks',
                        primary_value=GoogleMetadataColumnsPool.clicks, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    conversion_rate = ViewColumn(__id.increment_as_string(), display_name='Conversion rate',
                                 primary_value=GoogleMetadataColumnsPool.conversion_rate,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    conversions = ViewColumn(__id.increment_as_string(), display_name='Conversions',
                             primary_value=GoogleMetadataColumnsPool.conversions, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    conversion_value = ViewColumn(__id.increment_as_string(), display_name='Conversion value',
                                  primary_value=GoogleMetadataColumnsPool.conversion_value,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    cost = ViewColumn(__id.increment_as_string(), display_name='Cost', primary_value=GoogleMetadataColumnsPool.cost,
                      type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                      actions=[])

    cost_per_all_conversion = ViewColumn(__id.increment_as_string(), display_name='Cost per all conversion',
                                         primary_value=GoogleMetadataColumnsPool.cost_per_all_conversion,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    cost_per_conversion = ViewColumn(__id.increment_as_string(), display_name='Cost per conversion',
                                     primary_value=GoogleMetadataColumnsPool.cost_per_conversion,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    cost_per_current_model_attributed_conversion = ViewColumn(__id.increment_as_string(),
                                                              display_name='Cost per current model attributed conversion',
                                                              primary_value=GoogleMetadataColumnsPool.cost_per_current_model_attributed_conversion,
                                                              type_id=ViewColumnType.text.id,
                                                              category_id=ViewColumnCategory.common.id, actions=[])

    cross_device_conversions = ViewColumn(__id.increment_as_string(), display_name='Cross device conversions',
                                          primary_value=GoogleMetadataColumnsPool.cross_device_conversions,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    ctr = ViewColumn(__id.increment_as_string(), display_name='Ctr', primary_value=GoogleMetadataColumnsPool.ctr,
                     type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                     actions=[])

    current_model_attributed_conversions = ViewColumn(__id.increment_as_string(),
                                                      display_name='Current model attributed conversions',
                                                      primary_value=GoogleMetadataColumnsPool.current_model_attributed_conversions,
                                                      type_id=ViewColumnType.text.id,
                                                      category_id=ViewColumnCategory.common.id, actions=[])

    current_model_attributed_conversion_value = ViewColumn(__id.increment_as_string(),
                                                           display_name='Current model attributed conversion value',
                                                           primary_value=GoogleMetadataColumnsPool.current_model_attributed_conversion_value,
                                                           type_id=ViewColumnType.text.id,
                                                           category_id=ViewColumnCategory.common.id, actions=[])

    engagement_rate = ViewColumn(__id.increment_as_string(), display_name='Engagement rate',
                                 primary_value=GoogleMetadataColumnsPool.engagement_rate,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    engagements = ViewColumn(__id.increment_as_string(), display_name='Engagements',
                             primary_value=GoogleMetadataColumnsPool.engagements, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    gmail_forwards = ViewColumn(__id.increment_as_string(), display_name='Gmail forwards',
                                primary_value=GoogleMetadataColumnsPool.gmail_forwards, type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    gmail_saves = ViewColumn(__id.increment_as_string(), display_name='Gmail saves',
                             primary_value=GoogleMetadataColumnsPool.gmail_saves, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    gmail_secondary_clicks = ViewColumn(__id.increment_as_string(), display_name='Gmail secondary clicks',
                                        primary_value=GoogleMetadataColumnsPool.gmail_secondary_clicks,
                                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                        actions=[])

    impression_assisted_conversions = ViewColumn(__id.increment_as_string(),
                                                 display_name='Impression assisted conversions',
                                                 primary_value=GoogleMetadataColumnsPool.impression_assisted_conversions,
                                                 type_id=ViewColumnType.text.id,
                                                 category_id=ViewColumnCategory.common.id, actions=[])

    impression_assisted_conversions_over_last_click_conversions = ViewColumn(__id.increment_as_string(),
                                                                             display_name='Impression assisted conversions over last click conversions',
                                                                             primary_value=GoogleMetadataColumnsPool.impression_assisted_conversions_over_last_click_conversions,
                                                                             type_id=ViewColumnType.text.id,
                                                                             category_id=ViewColumnCategory.common.id,
                                                                             actions=[])

    impression_assisted_conversion_value = ViewColumn(__id.increment_as_string(),
                                                      display_name='Impression assisted conversion value',
                                                      primary_value=GoogleMetadataColumnsPool.impression_assisted_conversion_value,
                                                      type_id=ViewColumnType.text.id,
                                                      category_id=ViewColumnCategory.common.id, actions=[])

    impressions = ViewColumn(__id.increment_as_string(), display_name='Impressions',
                             primary_value=GoogleMetadataColumnsPool.impressions, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    interaction_rate = ViewColumn(__id.increment_as_string(), display_name='Interaction rate',
                                  primary_value=GoogleMetadataColumnsPool.interaction_rate,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    interactions = ViewColumn(__id.increment_as_string(), display_name='Interactions',
                              primary_value=GoogleMetadataColumnsPool.interactions, type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    interaction_types = ViewColumn(__id.increment_as_string(), display_name='Interaction types',
                                   primary_value=GoogleMetadataColumnsPool.interaction_types,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    percent_new_visitors = ViewColumn(__id.increment_as_string(), display_name='Percent new visitors',
                                      primary_value=GoogleMetadataColumnsPool.percent_new_visitors,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    top_impression_percentage = ViewColumn(__id.increment_as_string(), display_name='Top impression percentage',
                                           primary_value=GoogleMetadataColumnsPool.top_impression_percentage,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[])

    value_per_all_conversion = ViewColumn(__id.increment_as_string(), display_name='Value per all conversion',
                                          primary_value=GoogleMetadataColumnsPool.value_per_all_conversion,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    value_per_conversion = ViewColumn(__id.increment_as_string(), display_name='Value per conversion',
                                      primary_value=GoogleMetadataColumnsPool.value_per_conversion,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    value_per_current_model_attributed_conversion = ViewColumn(__id.increment_as_string(),
                                                               display_name='Value per current model attributed conversion',
                                                               primary_value=GoogleMetadataColumnsPool.value_per_current_model_attributed_conversion,
                                                               type_id=ViewColumnType.text.id,
                                                               category_id=ViewColumnCategory.common.id, actions=[])

    video_quartile_100_rate = ViewColumn(__id.increment_as_string(), display_name='Video quartile 100 rate',
                                         primary_value=GoogleMetadataColumnsPool.video_quartile_100_rate,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    video_quartile_25_rate = ViewColumn(__id.increment_as_string(), display_name='Video quartile 25 rate',
                                        primary_value=GoogleMetadataColumnsPool.video_quartile_25_rate,
                                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                        actions=[])

    video_quartile_50_rate = ViewColumn(__id.increment_as_string(), display_name='Video quartile 50 rate',
                                        primary_value=GoogleMetadataColumnsPool.video_quartile_50_rate,
                                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                        actions=[])

    video_quartile_75_rate = ViewColumn(__id.increment_as_string(), display_name='Video quartile 75 rate',
                                        primary_value=GoogleMetadataColumnsPool.video_quartile_75_rate,
                                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                        actions=[])

    video_view_rate = ViewColumn(__id.increment_as_string(), display_name='Video view rate',
                                 primary_value=GoogleMetadataColumnsPool.video_view_rate,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    video_views = ViewColumn(__id.increment_as_string(), display_name='Video views',
                             primary_value=GoogleMetadataColumnsPool.video_views, type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    view_through_conversions = ViewColumn(__id.increment_as_string(), display_name='View through conversions',
                                          primary_value=GoogleMetadataColumnsPool.view_through_conversions,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    content_impression_share = ViewColumn(__id.increment_as_string(), display_name='Content impression share',
                                          primary_value=GoogleMetadataColumnsPool.content_impression_share,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    content_rank_lost_impression_share = ViewColumn(__id.increment_as_string(),
                                                    display_name='Content rank lost impression share',
                                                    primary_value=GoogleMetadataColumnsPool.content_rank_lost_impression_share,
                                                    type_id=ViewColumnType.text.id,
                                                    category_id=ViewColumnCategory.common.id, actions=[])

    num_offline_impressions = ViewColumn(__id.increment_as_string(), display_name='Num offline impressions',
                                         primary_value=GoogleMetadataColumnsPool.num_offline_impressions,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    num_offline_interactions = ViewColumn(__id.increment_as_string(), display_name='Num offline interactions',
                                          primary_value=GoogleMetadataColumnsPool.num_offline_interactions,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    offline_interaction_rate = ViewColumn(__id.increment_as_string(), display_name='Offline interaction rate',
                                          primary_value=GoogleMetadataColumnsPool.offline_interaction_rate,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    relative_ctr = ViewColumn(__id.increment_as_string(), display_name='Relative ctr',
                              primary_value=GoogleMetadataColumnsPool.relative_ctr, type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    search_absolute_top_impression_share = ViewColumn(__id.increment_as_string(),
                                                      display_name='Search absolute top impression share',
                                                      primary_value=GoogleMetadataColumnsPool.search_absolute_top_impression_share,
                                                      type_id=ViewColumnType.text.id,
                                                      category_id=ViewColumnCategory.common.id, actions=[])

    search_budget_lost_absolute_top_impression_share = ViewColumn(__id.increment_as_string(),
                                                                  display_name='Search budget lost absolute top impression share',
                                                                  primary_value=GoogleMetadataColumnsPool.search_budget_lost_absolute_top_impression_share,
                                                                  type_id=ViewColumnType.text.id,
                                                                  category_id=ViewColumnCategory.common.id, actions=[])

    search_budget_lost_top_impression_share = ViewColumn(__id.increment_as_string(),
                                                         display_name='Search budget lost top impression share',
                                                         primary_value=GoogleMetadataColumnsPool.search_budget_lost_top_impression_share,
                                                         type_id=ViewColumnType.text.id,
                                                         category_id=ViewColumnCategory.common.id, actions=[])

    search_exact_match_impression_share = ViewColumn(__id.increment_as_string(),
                                                     display_name='Search exact match impression share',
                                                     primary_value=GoogleMetadataColumnsPool.search_exact_match_impression_share,
                                                     type_id=ViewColumnType.text.id,
                                                     category_id=ViewColumnCategory.common.id, actions=[])

    search_impression_share = ViewColumn(__id.increment_as_string(), display_name='Search impression share',
                                         primary_value=GoogleMetadataColumnsPool.search_impression_share,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    search_rank_lost_absolute_top_impression_share = ViewColumn(__id.increment_as_string(),
                                                                display_name='Search rank lost absolute top impression share',
                                                                primary_value=GoogleMetadataColumnsPool.search_rank_lost_absolute_top_impression_share,
                                                                type_id=ViewColumnType.text.id,
                                                                category_id=ViewColumnCategory.common.id, actions=[])

    search_rank_lost_impression_share = ViewColumn(__id.increment_as_string(),
                                                   display_name='Search rank lost impression share',
                                                   primary_value=GoogleMetadataColumnsPool.search_rank_lost_impression_share,
                                                   type_id=ViewColumnType.text.id,
                                                   category_id=ViewColumnCategory.common.id, actions=[])

    search_rank_lost_top_impression_share = ViewColumn(__id.increment_as_string(),
                                                       display_name='Search rank lost top impression share',
                                                       primary_value=GoogleMetadataColumnsPool.search_rank_lost_top_impression_share,
                                                       type_id=ViewColumnType.text.id,
                                                       category_id=ViewColumnCategory.common.id, actions=[])

    search_top_impression_share = ViewColumn(__id.increment_as_string(), display_name='Search top impression share',
                                             primary_value=GoogleMetadataColumnsPool.search_top_impression_share,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    average_frequency = ViewColumn(__id.increment_as_string(), display_name='Average frequency',
                                   primary_value=GoogleMetadataColumnsPool.average_frequency,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    content_budget_lost_impression_share = ViewColumn(__id.increment_as_string(),
                                                      display_name='Content budget lost impression share',
                                                      primary_value=GoogleMetadataColumnsPool.content_budget_lost_impression_share,
                                                      type_id=ViewColumnType.text.id,
                                                      category_id=ViewColumnCategory.common.id, actions=[])

    impression_reach = ViewColumn(__id.increment_as_string(), display_name='Impression reach',
                                  primary_value=GoogleMetadataColumnsPool.impression_reach,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    invalid_click_rate = ViewColumn(__id.increment_as_string(), display_name='Invalid click rate',
                                    primary_value=GoogleMetadataColumnsPool.invalid_click_rate,
                                    type_id=ViewColumnType.text.id,
                                    category_id=ViewColumnCategory.common.id, actions=[])

    invalid_clicks = ViewColumn(__id.increment_as_string(), display_name='Invalid clicks',
                                primary_value=GoogleMetadataColumnsPool.invalid_clicks, type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    search_budget_lost_impression_share = ViewColumn(__id.increment_as_string(),
                                                     display_name='Search budget lost impression share',
                                                     primary_value=GoogleMetadataColumnsPool.search_budget_lost_impression_share,
                                                     type_id=ViewColumnType.text.id,
                                                     category_id=ViewColumnCategory.common.id, actions=[])

    search_click_share = ViewColumn(__id.increment_as_string(), display_name='Search click share',
                                    primary_value=GoogleMetadataColumnsPool.search_click_share,
                                    type_id=ViewColumnType.text.id,
                                    category_id=ViewColumnCategory.common.id, actions=[])

    historical_creative_quality_score = ViewColumn(__id.increment_as_string(),
                                                   display_name='Historical creative quality score',
                                                   primary_value=GoogleMetadataColumnsPool.historical_creative_quality_score,
                                                   type_id=ViewColumnType.text.id,
                                                   category_id=ViewColumnCategory.common.id, actions=[])

    historical_landing_page_quality_score = ViewColumn(__id.increment_as_string(),
                                                       display_name='Historical landing page quality score',
                                                       primary_value=GoogleMetadataColumnsPool.historical_landing_page_quality_score,
                                                       type_id=ViewColumnType.text.id,
                                                       category_id=ViewColumnCategory.common.id, actions=[])

    historical_quality_score = ViewColumn(__id.increment_as_string(), display_name='Historical quality score',
                                          primary_value=GoogleMetadataColumnsPool.historical_quality_score,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    historical_search_predicted_ctr = ViewColumn(__id.increment_as_string(),
                                                 display_name='Historical search predicted ctr',
                                                 primary_value=GoogleMetadataColumnsPool.historical_search_predicted_ctr,
                                                 type_id=ViewColumnType.text.id,
                                                 category_id=ViewColumnCategory.common.id, actions=[])
