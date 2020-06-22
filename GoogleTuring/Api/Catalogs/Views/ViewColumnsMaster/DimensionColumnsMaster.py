from Core.Metadata.Columns.ViewColumns.ViewColumn import ViewColumn
from Core.Tools.Misc.Autoincrement import Autoincrement
from GoogleTuring.Api.Catalogs.Columns.GoogleAttributeMetadataColumnsPool import GoogleAttributeMetadataColumnsPool
from GoogleTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnCategory import ViewColumnCategory
from GoogleTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnType import ViewColumnType


class DimensionColumnsMaster:
    __id = Autoincrement(0)
    accent_color = ViewColumn(__id.increment_as_string(), display_name='Accent color',
                              primary_value=GoogleAttributeMetadataColumnsPool.accent_color,
                              type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    account_currency_code = ViewColumn(__id.increment_as_string(), display_name='Account currency code',
                                       primary_value=GoogleAttributeMetadataColumnsPool.account_currency_code,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    account_time_zone = ViewColumn(__id.increment_as_string(), display_name='Account time zone',
                                   primary_value=GoogleAttributeMetadataColumnsPool.account_time_zone,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    ad_group_status = ViewColumn(__id.increment_as_string(), display_name='Status',
                                 primary_value=GoogleAttributeMetadataColumnsPool.ad_group_status,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    # enable_pause_ad_group = ViewColumn(__id.increment_as_string(), display_name='Enable/Pause',
    #                                    primary_value=GoogleAttributeMetadataColumnsPool.ad_group_status,
    #                                    type_id=ViewColumnType.text.id,
    #                                    category_id=ViewColumnCategory.common.id, actions=[])

    ad_strength_info = ViewColumn(__id.increment_as_string(), display_name='Ad strength info',
                                  primary_value=GoogleAttributeMetadataColumnsPool.ad_strength_info,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    ad_type = ViewColumn(__id.increment_as_string(), display_name='Ad type',
                         primary_value=GoogleAttributeMetadataColumnsPool.ad_type, type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    allow_flexible_color = ViewColumn(__id.increment_as_string(), display_name='Allow flexible color',
                                      primary_value=GoogleAttributeMetadataColumnsPool.allow_flexible_color,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    automated = ViewColumn(__id.increment_as_string(), display_name='Automated',
                           primary_value=GoogleAttributeMetadataColumnsPool.automated, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    base_ad_group_id = ViewColumn(__id.increment_as_string(), display_name='Base ad group id',
                                  primary_value=GoogleAttributeMetadataColumnsPool.base_ad_group_id,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    base_campaignId = ViewColumn(__id.increment_as_string(), display_name='Base campaign id',
                                 primary_value=GoogleAttributeMetadataColumnsPool.base_campaignId,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    business_name = ViewColumn(__id.increment_as_string(), display_name='Business name',
                               primary_value=GoogleAttributeMetadataColumnsPool.business_name,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    call_only_phone_number = ViewColumn(__id.increment_as_string(), display_name='Call only phone number',
                                        primary_value=GoogleAttributeMetadataColumnsPool.call_only_phone_number,
                                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                        actions=[])

    call_to_action_text = ViewColumn(__id.increment_as_string(), display_name='Call to action text',
                                     primary_value=GoogleAttributeMetadataColumnsPool.call_to_action_text,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    campaign_id = ViewColumn(__id.increment_as_string(), display_name='Campaign id',
                             primary_value=GoogleAttributeMetadataColumnsPool.campaign_id,
                             type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    campaign_name = ViewColumn(__id.increment_as_string(), display_name='Campaign',
                               primary_value=GoogleAttributeMetadataColumnsPool.campaign_name,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    campaign_status = ViewColumn(__id.increment_as_string(), display_name='Status',
                                 primary_value=GoogleAttributeMetadataColumnsPool.campaign_status,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    # enable_pause_campaign = ViewColumn(__id.increment_as_string(), display_name='Enable/Pause',
    #                                    primary_value=GoogleAttributeMetadataColumnsPool.campaign_status,
    #                                    type_id=ViewColumnType.text.id,
    #                                    category_id=ViewColumnCategory.common.id, actions=[])

    combined_approval_status = ViewColumn(__id.increment_as_string(), display_name='Combined approval status',
                                          primary_value=GoogleAttributeMetadataColumnsPool.combined_approval_status,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    conversion_adjustment = ViewColumn(__id.increment_as_string(), display_name='Conversion adjustment',
                                       primary_value=GoogleAttributeMetadataColumnsPool.conversion_adjustment,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    creative_destination_url = ViewColumn(__id.increment_as_string(), display_name='Creative destination url',
                                          primary_value=GoogleAttributeMetadataColumnsPool.creative_destination_url,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    creative_final_app_urls = ViewColumn(__id.increment_as_string(), display_name='Creative final app urls',
                                         primary_value=GoogleAttributeMetadataColumnsPool.creative_final_app_urls,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    creative_final_mobile_urls = ViewColumn(__id.increment_as_string(), display_name='Creative final mobile urls',
                                            primary_value=GoogleAttributeMetadataColumnsPool.creative_final_mobile_urls,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[])

    creative_final_urls = ViewColumn(__id.increment_as_string(), display_name='Creative final urls',
                                     primary_value=GoogleAttributeMetadataColumnsPool.creative_final_urls,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    creative_final_url_suffix = ViewColumn(__id.increment_as_string(), display_name='Creative final url suffix',
                                           primary_value=GoogleAttributeMetadataColumnsPool.creative_final_url_suffix,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[])

    creative_tracking_url_template = ViewColumn(__id.increment_as_string(),
                                                display_name='Creative tracking url template',
                                                primary_value=GoogleAttributeMetadataColumnsPool.creative_tracking_url_template,
                                                type_id=ViewColumnType.text.id,
                                                category_id=ViewColumnCategory.common.id, actions=[])

    creative_url_custom_parameters = ViewColumn(__id.increment_as_string(),
                                                display_name='Creative url custom parameters',
                                                primary_value=GoogleAttributeMetadataColumnsPool.creative_url_custom_parameters,
                                                type_id=ViewColumnType.text.id,
                                                category_id=ViewColumnCategory.common.id, actions=[])

    customer_descriptive_name = ViewColumn(__id.increment_as_string(), display_name='Customer descriptive name',
                                           primary_value=GoogleAttributeMetadataColumnsPool.customer_descriptive_name,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[])

    description = ViewColumn(__id.increment_as_string(), display_name='Description',
                             primary_value=GoogleAttributeMetadataColumnsPool.description,
                             type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    description_1 = ViewColumn(__id.increment_as_string(), display_name='Description 1',
                               primary_value=GoogleAttributeMetadataColumnsPool.description_1,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    description_2 = ViewColumn(__id.increment_as_string(), display_name='Description 2',
                               primary_value=GoogleAttributeMetadataColumnsPool.description_2,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    device_preference = ViewColumn(__id.increment_as_string(), display_name='Device preference',
                                   primary_value=GoogleAttributeMetadataColumnsPool.device_preference,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    display_url = ViewColumn(__id.increment_as_string(), display_name='Display url',
                             primary_value=GoogleAttributeMetadataColumnsPool.display_url,
                             type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    enhanced_display_creative_landscape_logo_image_media_id = ViewColumn(__id.increment_as_string(),
                                                                         display_name='Enhanced display creative landscape logo image media id',
                                                                         primary_value=GoogleAttributeMetadataColumnsPool.enhanced_display_creative_landscape_logo_image_media_id,
                                                                         type_id=ViewColumnType.text.id,
                                                                         category_id=ViewColumnCategory.common.id,
                                                                         actions=[])

    enhanced_display_creative_logo_image_media_id = ViewColumn(__id.increment_as_string(),
                                                               display_name='Enhanced display creative logo image media id',
                                                               primary_value=GoogleAttributeMetadataColumnsPool.enhanced_display_creative_logo_image_media_id,
                                                               type_id=ViewColumnType.text.id,
                                                               category_id=ViewColumnCategory.common.id, actions=[])

    enhanced_display_creative_marketing_image_media_id = ViewColumn(__id.increment_as_string(),
                                                                    display_name='Enhanced display creative marketing image media id',
                                                                    primary_value=GoogleAttributeMetadataColumnsPool.enhanced_display_creative_marketing_image_media_id,
                                                                    type_id=ViewColumnType.text.id,
                                                                    category_id=ViewColumnCategory.common.id,
                                                                    actions=[])

    enhanced_display_creative_marketing_image_square_media_id = ViewColumn(__id.increment_as_string(),
                                                                           display_name='Enhanced display creative marketing image square media id',
                                                                           primary_value=GoogleAttributeMetadataColumnsPool.enhanced_display_creative_marketing_image_square_media_id,
                                                                           type_id=ViewColumnType.text.id,
                                                                           category_id=ViewColumnCategory.common.id,
                                                                           actions=[])

    expanded_dynamic_search_creative_description_2 = ViewColumn(__id.increment_as_string(),
                                                                display_name='Expanded dynamic search creative description 2',
                                                                primary_value=GoogleAttributeMetadataColumnsPool.expanded_dynamic_search_creative_description_2,
                                                                type_id=ViewColumnType.text.id,
                                                                category_id=ViewColumnCategory.common.id, actions=[])

    expanded_text_ad_description_2 = ViewColumn(__id.increment_as_string(),
                                                display_name='Expanded text ad description 2',
                                                primary_value=GoogleAttributeMetadataColumnsPool.expanded_text_ad_description_2,
                                                type_id=ViewColumnType.text.id,
                                                category_id=ViewColumnCategory.common.id, actions=[])

    expanded_text_ad_headline_part_3 = ViewColumn(__id.increment_as_string(),
                                                  display_name='Expanded text ad headline part 3',
                                                  primary_value=GoogleAttributeMetadataColumnsPool.expanded_text_ad_headline_part_3,
                                                  type_id=ViewColumnType.text.id,
                                                  category_id=ViewColumnCategory.common.id, actions=[])

    external_customer_id = ViewColumn(__id.increment_as_string(), display_name='External customer id',
                                      primary_value=GoogleAttributeMetadataColumnsPool.external_customer_id,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    format_setting = ViewColumn(__id.increment_as_string(), display_name='Format setting',
                                primary_value=GoogleAttributeMetadataColumnsPool.format_setting,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    gmail_creative_header_image_media_id = ViewColumn(__id.increment_as_string(),
                                                      display_name='Gmail creative header image media id',
                                                      primary_value=GoogleAttributeMetadataColumnsPool.gmail_creative_header_image_media_id,
                                                      type_id=ViewColumnType.text.id,
                                                      category_id=ViewColumnCategory.common.id, actions=[])

    gmail_creative_logo_image_media_id = ViewColumn(__id.increment_as_string(),
                                                    display_name='Gmail creative logo image media id',
                                                    primary_value=GoogleAttributeMetadataColumnsPool.gmail_creative_logo_image_media_id,
                                                    type_id=ViewColumnType.text.id,
                                                    category_id=ViewColumnCategory.common.id, actions=[])

    gmail_creative_marketing_image_media_id = ViewColumn(__id.increment_as_string(),
                                                         display_name='Gmail creative marketing image media id',
                                                         primary_value=GoogleAttributeMetadataColumnsPool.gmail_creative_marketing_image_media_id,
                                                         type_id=ViewColumnType.text.id,
                                                         category_id=ViewColumnCategory.common.id, actions=[])

    gmail_teaser_business_name = ViewColumn(__id.increment_as_string(), display_name='Gmail teaser business name',
                                            primary_value=GoogleAttributeMetadataColumnsPool.gmail_teaser_business_name,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[])

    gmail_teaser_description = ViewColumn(__id.increment_as_string(), display_name='Gmail teaser description',
                                          primary_value=GoogleAttributeMetadataColumnsPool.gmail_teaser_description,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    gmail_teaser_headline = ViewColumn(__id.increment_as_string(), display_name='Gmail teaser headline',
                                       primary_value=GoogleAttributeMetadataColumnsPool.gmail_teaser_headline,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    headline = ViewColumn(__id.increment_as_string(), display_name='Headline',
                          primary_value=GoogleAttributeMetadataColumnsPool.headline, type_id=ViewColumnType.text.id,
                          category_id=ViewColumnCategory.common.id, actions=[])

    headline_part_1 = ViewColumn(__id.increment_as_string(), display_name='Headline part 1',
                                 primary_value=GoogleAttributeMetadataColumnsPool.headline_part_1,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    headline_part_2 = ViewColumn(__id.increment_as_string(), display_name='Headline part 2',
                                 primary_value=GoogleAttributeMetadataColumnsPool.headline_part_2,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    id = ViewColumn(__id.increment_as_string(), display_name='Id', primary_value=GoogleAttributeMetadataColumnsPool.id,
                    type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                    actions=[])

    ad_id = ViewColumn(__id.increment_as_string(), display_name='Ad id',
                       primary_value=GoogleAttributeMetadataColumnsPool.ad_id,
                       type_id=ViewColumnType.text.id,
                       category_id=ViewColumnCategory.common.id, actions=[])

    image_ad_url = ViewColumn(__id.increment_as_string(), display_name='Image ad url',
                              primary_value=GoogleAttributeMetadataColumnsPool.image_ad_url,
                              type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    image_creative_image_height = ViewColumn(__id.increment_as_string(), display_name='Image creative image height',
                                             primary_value=GoogleAttributeMetadataColumnsPool.image_creative_image_height,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    image_creative_image_width = ViewColumn(__id.increment_as_string(), display_name='Image creative image width',
                                            primary_value=GoogleAttributeMetadataColumnsPool.image_creative_image_width,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[])

    image_creative_mime_type = ViewColumn(__id.increment_as_string(), display_name='Image creative mime type',
                                          primary_value=GoogleAttributeMetadataColumnsPool.image_creative_mime_type,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    image_creative_name = ViewColumn(__id.increment_as_string(), display_name='Image creative name',
                                     primary_value=GoogleAttributeMetadataColumnsPool.image_creative_name,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    is_negative = ViewColumn(__id.increment_as_string(), display_name='Is negative',
                             primary_value=GoogleAttributeMetadataColumnsPool.is_negative,
                             type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    label_ids = ViewColumn(__id.increment_as_string(), display_name='Label ids',
                           primary_value=GoogleAttributeMetadataColumnsPool.label_ids, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    labels = ViewColumn(__id.increment_as_string(), display_name='Labels',
                        primary_value=GoogleAttributeMetadataColumnsPool.labels, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    long_headline = ViewColumn(__id.increment_as_string(), display_name='Long headline',
                               primary_value=GoogleAttributeMetadataColumnsPool.long_headline,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    main_color = ViewColumn(__id.increment_as_string(), display_name='Main color',
                            primary_value=GoogleAttributeMetadataColumnsPool.main_color,
                            type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    marketing_image_call_to_action_text = ViewColumn(__id.increment_as_string(),
                                                     display_name='Marketing image call to action text',
                                                     primary_value=GoogleAttributeMetadataColumnsPool.marketing_image_call_to_action_text,
                                                     type_id=ViewColumnType.text.id,
                                                     category_id=ViewColumnCategory.common.id, actions=[])

    marketing_image_call_to_action_text_color = ViewColumn(__id.increment_as_string(),
                                                           display_name='Marketing image call to action text color',
                                                           primary_value=GoogleAttributeMetadataColumnsPool.marketing_image_call_to_action_text_color,
                                                           type_id=ViewColumnType.text.id,
                                                           category_id=ViewColumnCategory.common.id, actions=[])

    marketing_image_description = ViewColumn(__id.increment_as_string(), display_name='Marketing image description',
                                             primary_value=GoogleAttributeMetadataColumnsPool.marketing_image_description,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    marketing_image_headline = ViewColumn(__id.increment_as_string(), display_name='Marketing image headline',
                                          primary_value=GoogleAttributeMetadataColumnsPool.marketing_image_headline,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    multi_asset_responsive_display_ad_accent_color = ViewColumn(__id.increment_as_string(),
                                                                display_name='Multi asset responsive display ad accent color',
                                                                primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_accent_color,
                                                                type_id=ViewColumnType.text.id,
                                                                category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_allow_flexible_color = ViewColumn(__id.increment_as_string(),
                                                                        display_name='Multi asset responsive display ad allow flexible color',
                                                                        primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_allow_flexible_color,
                                                                        type_id=ViewColumnType.text.id,
                                                                        category_id=ViewColumnCategory.common.id,
                                                                        actions=[])

    multi_asset_responsive_display_ad_business_name = ViewColumn(__id.increment_as_string(),
                                                                 display_name='Multi asset responsive display ad business name',
                                                                 primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_business_name,
                                                                 type_id=ViewColumnType.text.id,
                                                                 category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_call_to_action_text = ViewColumn(__id.increment_as_string(),
                                                                       display_name='Multi asset responsive display ad call to action text',
                                                                       primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_call_to_action_text,
                                                                       type_id=ViewColumnType.text.id,
                                                                       category_id=ViewColumnCategory.common.id,
                                                                       actions=[])

    multi_asset_responsive_display_ad_descriptions = ViewColumn(__id.increment_as_string(),
                                                                display_name='Multi asset responsive display ad descriptions',
                                                                primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_descriptions,
                                                                type_id=ViewColumnType.text.id,
                                                                category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_dynamic_settings_price_prefix = ViewColumn(__id.increment_as_string(),
                                                                                 display_name='Multi asset responsive display ad dynamic settings price prefix',
                                                                                 primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_dynamic_settings_price_prefix,
                                                                                 type_id=ViewColumnType.text.id,
                                                                                 category_id=ViewColumnCategory.common.id,
                                                                                 actions=[])

    multi_asset_responsive_display_ad_dynamic_settings_promo_text = ViewColumn(__id.increment_as_string(),
                                                                               display_name='Multi asset responsive display ad dynamic settings promo text',
                                                                               primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_dynamic_settings_promo_text,
                                                                               type_id=ViewColumnType.text.id,
                                                                               category_id=ViewColumnCategory.common.id,
                                                                               actions=[])

    multi_asset_responsive_display_ad_format_setting = ViewColumn(__id.increment_as_string(),
                                                                  display_name='Multi asset responsive display ad format setting',
                                                                  primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_format_setting,
                                                                  type_id=ViewColumnType.text.id,
                                                                  category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_headlines = ViewColumn(__id.increment_as_string(),
                                                             display_name='Multi asset responsive display ad headlines',
                                                             primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_headlines,
                                                             type_id=ViewColumnType.text.id,
                                                             category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_landscape_logo_images = ViewColumn(__id.increment_as_string(),
                                                                         display_name='Multi asset responsive display ad landscape logo images',
                                                                         primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_landscape_logo_images,
                                                                         type_id=ViewColumnType.text.id,
                                                                         category_id=ViewColumnCategory.common.id,
                                                                         actions=[])

    multi_asset_responsive_display_ad_logo_images = ViewColumn(__id.increment_as_string(),
                                                               display_name='Multi asset responsive display ad logo images',
                                                               primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_logo_images,
                                                               type_id=ViewColumnType.text.id,
                                                               category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_long_headline = ViewColumn(__id.increment_as_string(),
                                                                 display_name='Multi asset responsive display ad long headline',
                                                                 primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_long_headline,
                                                                 type_id=ViewColumnType.text.id,
                                                                 category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_main_color = ViewColumn(__id.increment_as_string(),
                                                              display_name='Multi asset responsive display ad main color',
                                                              primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_main_color,
                                                              type_id=ViewColumnType.text.id,
                                                              category_id=ViewColumnCategory.common.id, actions=[])

    multi_asset_responsive_display_ad_marketing_images = ViewColumn(__id.increment_as_string(),
                                                                    display_name='Multi asset responsive display ad marketing images',
                                                                    primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_marketing_images,
                                                                    type_id=ViewColumnType.text.id,
                                                                    category_id=ViewColumnCategory.common.id,
                                                                    actions=[])

    multi_asset_responsive_display_ad_square_marketing_images = ViewColumn(__id.increment_as_string(),
                                                                           display_name='Multi asset responsive display ad square marketing images',
                                                                           primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_square_marketing_images,
                                                                           type_id=ViewColumnType.text.id,
                                                                           category_id=ViewColumnCategory.common.id,
                                                                           actions=[])

    multi_asset_responsive_display_ad_you_tube_videos = ViewColumn(__id.increment_as_string(),
                                                                   display_name='Multi asset responsive display ad you tube videos',
                                                                   primary_value=GoogleAttributeMetadataColumnsPool.multi_asset_responsive_display_ad_you_tube_videos,
                                                                   type_id=ViewColumnType.text.id,
                                                                   category_id=ViewColumnCategory.common.id,
                                                                   actions=[])

    path_1 = ViewColumn(__id.increment_as_string(), display_name='Path 1',
                        primary_value=GoogleAttributeMetadataColumnsPool.path_1, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    path_2 = ViewColumn(__id.increment_as_string(), display_name='Path 2',
                        primary_value=GoogleAttributeMetadataColumnsPool.path_2, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    policy_summary = ViewColumn(__id.increment_as_string(), display_name='Policy summary',
                                primary_value=GoogleAttributeMetadataColumnsPool.policy_summary,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    price_prefix = ViewColumn(__id.increment_as_string(), display_name='Price prefix',
                              primary_value=GoogleAttributeMetadataColumnsPool.price_prefix,
                              type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    promo_text = ViewColumn(__id.increment_as_string(), display_name='Promo text',
                            primary_value=GoogleAttributeMetadataColumnsPool.promo_text,
                            type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    responsive_search_ad_descriptions = ViewColumn(__id.increment_as_string(),
                                                   display_name='Responsive search ad descriptions',
                                                   primary_value=GoogleAttributeMetadataColumnsPool.responsive_search_ad_descriptions,
                                                   type_id=ViewColumnType.text.id,
                                                   category_id=ViewColumnCategory.common.id, actions=[])

    responsive_search_ad_headlines = ViewColumn(__id.increment_as_string(),
                                                display_name='Responsive search ad headlines',
                                                primary_value=GoogleAttributeMetadataColumnsPool.responsive_search_ad_headlines,
                                                type_id=ViewColumnType.text.id,
                                                category_id=ViewColumnCategory.common.id, actions=[])

    responsive_search_ad_path_1 = ViewColumn(__id.increment_as_string(), display_name='Responsive search ad path 1',
                                             primary_value=GoogleAttributeMetadataColumnsPool.responsive_search_ad_path_1,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    responsive_search_ad_path_2 = ViewColumn(__id.increment_as_string(), display_name='Responsive search ad path 2',
                                             primary_value=GoogleAttributeMetadataColumnsPool.responsive_search_ad_path_2,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    short_headline = ViewColumn(__id.increment_as_string(), display_name='Short headline',
                                primary_value=GoogleAttributeMetadataColumnsPool.short_headline,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    status = ViewColumn(__id.increment_as_string(), display_name='Status',
                        primary_value=GoogleAttributeMetadataColumnsPool.status, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    # enable_pause_keyword = ViewColumn(__id.increment_as_string(), display_name='Enable/Pause',
    #                                   primary_value=GoogleAttributeMetadataColumnsPool.status,
    #                                   type_id=ViewColumnType.text.id,
    #                                   category_id=ViewColumnCategory.common.id, actions=[])

    # enable_pause_ad = ViewColumn(__id.increment_as_string(), display_name='Enable/Pause',
    #                              primary_value=GoogleAttributeMetadataColumnsPool.status,
    #                              type_id=ViewColumnType.text.id,
    #                              category_id=ViewColumnCategory.common.id, actions=[])

    system_managed_entity_source = ViewColumn(__id.increment_as_string(), display_name='System managed entity source',
                                              primary_value=GoogleAttributeMetadataColumnsPool.system_managed_entity_source,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    universal_app_ad_descriptions = ViewColumn(__id.increment_as_string(),
                                               display_name='Universal app ad descriptions',
                                               primary_value=GoogleAttributeMetadataColumnsPool.universal_app_ad_descriptions,
                                               type_id=ViewColumnType.text.id,
                                               category_id=ViewColumnCategory.common.id, actions=[])

    universal_app_ad_headlines = ViewColumn(__id.increment_as_string(), display_name='Universal app ad headlines',
                                            primary_value=GoogleAttributeMetadataColumnsPool.universal_app_ad_headlines,
                                            type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                            actions=[])

    universal_app_ad_html_5_media_bundles = ViewColumn(__id.increment_as_string(),
                                                       display_name='Universal app ad html 5 media bundles',
                                                       primary_value=GoogleAttributeMetadataColumnsPool.universal_app_ad_html_5_media_bundles,
                                                       type_id=ViewColumnType.text.id,
                                                       category_id=ViewColumnCategory.common.id, actions=[])

    universal_app_ad_images = ViewColumn(__id.increment_as_string(), display_name='Universal app ad images',
                                         primary_value=GoogleAttributeMetadataColumnsPool.universal_app_ad_images,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    universal_app_ad_mandatory_ad_text = ViewColumn(__id.increment_as_string(),
                                                    display_name='Universal app ad mandatory ad text',
                                                    primary_value=GoogleAttributeMetadataColumnsPool.universal_app_ad_mandatory_ad_text,
                                                    type_id=ViewColumnType.text.id,
                                                    category_id=ViewColumnCategory.common.id, actions=[])

    universal_app_ad_you_tube_videos = ViewColumn(__id.increment_as_string(),
                                                  display_name='Universal app ad you tube videos',
                                                  primary_value=GoogleAttributeMetadataColumnsPool.universal_app_ad_you_tube_videos,
                                                  type_id=ViewColumnType.text.id,
                                                  category_id=ViewColumnCategory.common.id, actions=[])

    account_descriptive_name = ViewColumn(__id.increment_as_string(), display_name='Account descriptive name',
                                          primary_value=GoogleAttributeMetadataColumnsPool.account_descriptive_name,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    ad_group_desktop_bid_modifier = ViewColumn(__id.increment_as_string(),
                                               display_name='Ad group desktop bid modifier',
                                               primary_value=GoogleAttributeMetadataColumnsPool.ad_group_desktop_bid_modifier,
                                               type_id=ViewColumnType.text.id,
                                               category_id=ViewColumnCategory.common.id, actions=[])

    ad_group_id = ViewColumn(__id.increment_as_string(), display_name='Ad group id',
                             primary_value=GoogleAttributeMetadataColumnsPool.ad_group_id,
                             type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    ad_group_mobile_bid_modifier = ViewColumn(__id.increment_as_string(), display_name='Ad group mobile bid modifier',
                                              primary_value=GoogleAttributeMetadataColumnsPool.ad_group_mobile_bid_modifier,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    ad_group_name = ViewColumn(__id.increment_as_string(), display_name='Ad group',
                               primary_value=GoogleAttributeMetadataColumnsPool.ad_group_name,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    ad_group_tablet_bid_modifier = ViewColumn(__id.increment_as_string(), display_name='Ad group tablet bid modifier',
                                              primary_value=GoogleAttributeMetadataColumnsPool.ad_group_tablet_bid_modifier,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    ad_group_type = ViewColumn(__id.increment_as_string(), display_name='Ad group type',
                               primary_value=GoogleAttributeMetadataColumnsPool.ad_group_type,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    ad_rotation_mode = ViewColumn(__id.increment_as_string(), display_name='Ad rotation mode',
                                  primary_value=GoogleAttributeMetadataColumnsPool.ad_rotation_mode,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    bidding_strategy_id = ViewColumn(__id.increment_as_string(), display_name='Bidding strategy id',
                                     primary_value=GoogleAttributeMetadataColumnsPool.bidding_strategy_id,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    bidding_strategy_name = ViewColumn(__id.increment_as_string(), display_name='Bidding strategy name',
                                       primary_value=GoogleAttributeMetadataColumnsPool.bidding_strategy_name,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    bidding_strategy_source = ViewColumn(__id.increment_as_string(), display_name='Bidding strategy source',
                                         primary_value=GoogleAttributeMetadataColumnsPool.bidding_strategy_source,
                                         type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                         actions=[])

    bidding_strategy_type = ViewColumn(__id.increment_as_string(), display_name='Bidding strategy type',
                                       primary_value=GoogleAttributeMetadataColumnsPool.bidding_strategy_type,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    content_bid_criterion_type_group = ViewColumn(__id.increment_as_string(),
                                                  display_name='Content bid criterion type group',
                                                  primary_value=GoogleAttributeMetadataColumnsPool.content_bid_criterion_type_group,
                                                  type_id=ViewColumnType.text.id,
                                                  category_id=ViewColumnCategory.common.id, actions=[])

    cpc_bid = ViewColumn(__id.increment_as_string(), display_name='Default max. CPC',
                         primary_value=GoogleAttributeMetadataColumnsPool.cpc_bid,
                         type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    max_cpc = ViewColumn(__id.increment_as_string(), display_name='Max. CPC',
                         primary_value=GoogleAttributeMetadataColumnsPool.cpc_bid, type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    cpm_bid = ViewColumn(__id.increment_as_string(), display_name='Cpm bid',
                         primary_value=GoogleAttributeMetadataColumnsPool.cpm_bid, type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    cpv_bid = ViewColumn(__id.increment_as_string(), display_name='Max CPV',
                         primary_value=GoogleAttributeMetadataColumnsPool.cpv_bid, type_id=ViewColumnType.text.id,
                         category_id=ViewColumnCategory.common.id, actions=[])

    effective_target_roas = ViewColumn(__id.increment_as_string(), display_name='Effective target roas',
                                       primary_value=GoogleAttributeMetadataColumnsPool.effective_target_roas,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    effective_target_roas_source = ViewColumn(__id.increment_as_string(), display_name='Effective target roas source',
                                              primary_value=GoogleAttributeMetadataColumnsPool.effective_target_roas_source,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    enhanced_cpc_enabled = ViewColumn(__id.increment_as_string(), display_name='Enhanced cpc enabled',
                                      primary_value=GoogleAttributeMetadataColumnsPool.enhanced_cpc_enabled,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    final_url_suffix = ViewColumn(__id.increment_as_string(), display_name='Final url suffix',
                                  primary_value=GoogleAttributeMetadataColumnsPool.final_url_suffix,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    target_cpa = ViewColumn(__id.increment_as_string(), display_name='Target cpa',
                            primary_value=GoogleAttributeMetadataColumnsPool.target_cpa,
                            type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    target_cpa_bid_source = ViewColumn(__id.increment_as_string(), display_name='Target cpa bid source',
                                       primary_value=GoogleAttributeMetadataColumnsPool.target_cpa_bid_source,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    tracking_url_template = ViewColumn(__id.increment_as_string(), display_name='Tracking url template',
                                       primary_value=GoogleAttributeMetadataColumnsPool.tracking_url_template,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    url_custom_parameters = ViewColumn(__id.increment_as_string(), display_name='Url custom parameters',
                                       primary_value=GoogleAttributeMetadataColumnsPool.url_custom_parameters,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    advertising_channel_sub_type = ViewColumn(__id.increment_as_string(), display_name='Advertising channel sub type',
                                              primary_value=GoogleAttributeMetadataColumnsPool.advertising_channel_sub_type,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    advertising_channel_type = ViewColumn(__id.increment_as_string(), display_name='Advertising channel type',
                                          primary_value=GoogleAttributeMetadataColumnsPool.advertising_channel_type,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    amount = ViewColumn(__id.increment_as_string(), display_name='Budget',
                        primary_value=GoogleAttributeMetadataColumnsPool.amount, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    budget_id = ViewColumn(__id.increment_as_string(), display_name='Budget id',
                           primary_value=GoogleAttributeMetadataColumnsPool.budget_id, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    campaign_desktop_bid_modifier = ViewColumn(__id.increment_as_string(),
                                               display_name='Campaign desktop bid modifier',
                                               primary_value=GoogleAttributeMetadataColumnsPool.campaign_desktop_bid_modifier,
                                               type_id=ViewColumnType.text.id,
                                               category_id=ViewColumnCategory.common.id, actions=[])

    campaign_group_id = ViewColumn(__id.increment_as_string(), display_name='Campaign group id',
                                   primary_value=GoogleAttributeMetadataColumnsPool.campaign_group_id,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    campaign_mobile_bid_modifier = ViewColumn(__id.increment_as_string(), display_name='Campaign mobile bid modifier',
                                              primary_value=GoogleAttributeMetadataColumnsPool.campaign_mobile_bid_modifier,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    campaign_tablet_bid_modifier = ViewColumn(__id.increment_as_string(), display_name='Campaign tablet bid modifier',
                                              primary_value=GoogleAttributeMetadataColumnsPool.campaign_tablet_bid_modifier,
                                              type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                              actions=[])

    campaign_trial_type = ViewColumn(__id.increment_as_string(), display_name='Campaign trial type',
                                     primary_value=GoogleAttributeMetadataColumnsPool.campaign_trial_type,
                                     type_id=ViewColumnType.text.id,
                                     category_id=ViewColumnCategory.common.id, actions=[])

    end_date = ViewColumn(__id.increment_as_string(), display_name='End date',
                          primary_value=GoogleAttributeMetadataColumnsPool.end_date, type_id=ViewColumnType.text.id,
                          category_id=ViewColumnCategory.common.id, actions=[])

    has_recommended_budget = ViewColumn(__id.increment_as_string(), display_name='Has recommended budget',
                                        primary_value=GoogleAttributeMetadataColumnsPool.has_recommended_budget,
                                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                        actions=[])

    is_budget_explicitly_shared = ViewColumn(__id.increment_as_string(), display_name='Is budget explicitly shared',
                                             primary_value=GoogleAttributeMetadataColumnsPool.is_budget_explicitly_shared,
                                             type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                             actions=[])

    maximize_conversion_value_target_roas = ViewColumn(__id.increment_as_string(),
                                                       display_name='Maximize conversion value target roas',
                                                       primary_value=GoogleAttributeMetadataColumnsPool.maximize_conversion_value_target_roas,
                                                       type_id=ViewColumnType.text.id,
                                                       category_id=ViewColumnCategory.common.id, actions=[])

    period = ViewColumn(__id.increment_as_string(), display_name='Period',
                        primary_value=GoogleAttributeMetadataColumnsPool.period, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    recommended_budget_amount = ViewColumn(__id.increment_as_string(), display_name='Recommended budget amount',
                                           primary_value=GoogleAttributeMetadataColumnsPool.recommended_budget_amount,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[])

    serving_status = ViewColumn(__id.increment_as_string(), display_name='Serving status',
                                primary_value=GoogleAttributeMetadataColumnsPool.serving_status,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    start_date = ViewColumn(__id.increment_as_string(), display_name='Start date',
                            primary_value=GoogleAttributeMetadataColumnsPool.start_date,
                            type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    total_amount = ViewColumn(__id.increment_as_string(), display_name='Total amount',
                              primary_value=GoogleAttributeMetadataColumnsPool.total_amount,
                              type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    approval_status = ViewColumn(__id.increment_as_string(), display_name='Policy Details',
                                 primary_value=GoogleAttributeMetadataColumnsPool.approval_status,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    cpc_bid_source = ViewColumn(__id.increment_as_string(), display_name='Cpc bid source',
                                primary_value=GoogleAttributeMetadataColumnsPool.cpc_bid_source,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    creative_quality_score = ViewColumn(__id.increment_as_string(), display_name='Creative quality score',
                                        primary_value=GoogleAttributeMetadataColumnsPool.creative_quality_score,
                                        type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                        actions=[])

    criteria = ViewColumn(__id.increment_as_string(), display_name='Criteria',
                          primary_value=GoogleAttributeMetadataColumnsPool.criteria, type_id=ViewColumnType.text.id,
                          category_id=ViewColumnCategory.common.id, actions=[])

    gender = ViewColumn(__id.increment_as_string(), display_name='Gender',
                        primary_value=GoogleAttributeMetadataColumnsPool.gender, type_id=ViewColumnType.text.id,
                        category_id=ViewColumnCategory.common.id, actions=[])

    age_range = ViewColumn(__id.increment_as_string(), display_name='Age range',
                           primary_value=GoogleAttributeMetadataColumnsPool.age_range, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    keywords = ViewColumn(__id.increment_as_string(), display_name='Keyword',
                          primary_value=GoogleAttributeMetadataColumnsPool.keywords, type_id=ViewColumnType.text.id,
                          category_id=ViewColumnCategory.common.id, actions=[])

    criteria_destination_url = ViewColumn(__id.increment_as_string(), display_name='Criteria destination url',
                                          primary_value=GoogleAttributeMetadataColumnsPool.criteria_destination_url,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    estimated_add_clicks_at_first_position_cpc = ViewColumn(__id.increment_as_string(),
                                                            display_name='Estimated add clicks at first position cpc',
                                                            primary_value=GoogleAttributeMetadataColumnsPool.estimated_add_clicks_at_first_position_cpc,
                                                            type_id=ViewColumnType.text.id,
                                                            category_id=ViewColumnCategory.common.id, actions=[])

    estimated_add_cost_at_first_position_cpc = ViewColumn(__id.increment_as_string(),
                                                          display_name='Estimated add cost at first position cpc',
                                                          primary_value=GoogleAttributeMetadataColumnsPool.estimated_add_cost_at_first_position_cpc,
                                                          type_id=ViewColumnType.text.id,
                                                          category_id=ViewColumnCategory.common.id, actions=[])

    final_app_urls = ViewColumn(__id.increment_as_string(), display_name='Final app urls',
                                primary_value=GoogleAttributeMetadataColumnsPool.final_app_urls,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    final_mobile_urls = ViewColumn(__id.increment_as_string(), display_name='Final mobile urls',
                                   primary_value=GoogleAttributeMetadataColumnsPool.final_mobile_urls,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    final_urls = ViewColumn(__id.increment_as_string(), display_name='Final URL',
                            primary_value=GoogleAttributeMetadataColumnsPool.final_urls,
                            type_id=ViewColumnType.text.id,
                            category_id=ViewColumnCategory.common.id, actions=[])

    first_page_cpc = ViewColumn(__id.increment_as_string(), display_name='First page cpc',
                                primary_value=GoogleAttributeMetadataColumnsPool.first_page_cpc,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    first_position_cpc = ViewColumn(__id.increment_as_string(), display_name='First position cpc',
                                    primary_value=GoogleAttributeMetadataColumnsPool.first_position_cpc,
                                    type_id=ViewColumnType.text.id,
                                    category_id=ViewColumnCategory.common.id, actions=[])

    has_quality_score = ViewColumn(__id.increment_as_string(), display_name='Has quality score',
                                   primary_value=GoogleAttributeMetadataColumnsPool.has_quality_score,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    keyword_match_type = ViewColumn(__id.increment_as_string(), display_name='Keyword match type',
                                    primary_value=GoogleAttributeMetadataColumnsPool.keyword_match_type,
                                    type_id=ViewColumnType.text.id,
                                    category_id=ViewColumnCategory.common.id, actions=[])

    post_click_quality_score = ViewColumn(__id.increment_as_string(), display_name='Post click quality score',
                                          primary_value=GoogleAttributeMetadataColumnsPool.post_click_quality_score,
                                          type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                          actions=[])

    quality_score = ViewColumn(__id.increment_as_string(), display_name='Quality score',
                               primary_value=GoogleAttributeMetadataColumnsPool.quality_score,
                               type_id=ViewColumnType.text.id,
                               category_id=ViewColumnCategory.common.id, actions=[])

    search_predicted_ctr = ViewColumn(__id.increment_as_string(), display_name='Search predicted ctr',
                                      primary_value=GoogleAttributeMetadataColumnsPool.search_predicted_ctr,
                                      type_id=ViewColumnType.text.id,
                                      category_id=ViewColumnCategory.common.id, actions=[])

    system_serving_status = ViewColumn(__id.increment_as_string(), display_name='System serving status',
                                       primary_value=GoogleAttributeMetadataColumnsPool.system_serving_status,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    top_of_page_cpc = ViewColumn(__id.increment_as_string(), display_name='Top of page cpc',
                                 primary_value=GoogleAttributeMetadataColumnsPool.top_of_page_cpc,
                                 type_id=ViewColumnType.text.id,
                                 category_id=ViewColumnCategory.common.id, actions=[])

    vertical_id = ViewColumn(__id.increment_as_string(), display_name='Vertical id',
                             primary_value=GoogleAttributeMetadataColumnsPool.vertical_id,
                             type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    city_name = ViewColumn(__id.increment_as_string(), display_name='City name',
                           primary_value=GoogleAttributeMetadataColumnsPool.city_name, type_id=ViewColumnType.text.id,
                           category_id=ViewColumnCategory.common.id, actions=[])

    country_name = ViewColumn(__id.increment_as_string(), display_name='Country name',
                              primary_value=GoogleAttributeMetadataColumnsPool.country_name,
                              type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    is_targeting_location = ViewColumn(__id.increment_as_string(), display_name='Is targeting location',
                                       primary_value=GoogleAttributeMetadataColumnsPool.is_targeting_location,
                                       type_id=ViewColumnType.text.id,
                                       category_id=ViewColumnCategory.common.id, actions=[])

    metro_criteria_id = ViewColumn(__id.increment_as_string(), display_name='Metro criteria id',
                                   primary_value=GoogleAttributeMetadataColumnsPool.metro_criteria_id,
                                   type_id=ViewColumnType.text.id,
                                   category_id=ViewColumnCategory.common.id, actions=[])

    most_specific_criteria_id = ViewColumn(__id.increment_as_string(), display_name='Most specific criteria id',
                                           primary_value=GoogleAttributeMetadataColumnsPool.most_specific_criteria_id,
                                           type_id=ViewColumnType.text.id, category_id=ViewColumnCategory.common.id,
                                           actions=[])

    region_name = ViewColumn(__id.increment_as_string(), display_name='Region name',
                             primary_value=GoogleAttributeMetadataColumnsPool.region_name,
                             type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])

    base_campaign_id = ViewColumn(__id.increment_as_string(), display_name='Base campaign id',
                                  primary_value=GoogleAttributeMetadataColumnsPool.base_campaign_id,
                                  type_id=ViewColumnType.text.id,
                                  category_id=ViewColumnCategory.common.id, actions=[])

    bid_modifier = ViewColumn(__id.increment_as_string(), display_name='Bid Adjust',
                              primary_value=GoogleAttributeMetadataColumnsPool.bid_modifier,
                              type_id=ViewColumnType.text.id,
                              category_id=ViewColumnCategory.common.id, actions=[])

    cpm_bid_source = ViewColumn(__id.increment_as_string(), display_name='Cpm bid source',
                                primary_value=GoogleAttributeMetadataColumnsPool.cpm_bid_source,
                                type_id=ViewColumnType.text.id,
                                category_id=ViewColumnCategory.common.id, actions=[])

    is_restrict = ViewColumn(__id.increment_as_string(), display_name='Is restrict',
                             primary_value=GoogleAttributeMetadataColumnsPool.is_restrict,
                             type_id=ViewColumnType.text.id,
                             category_id=ViewColumnCategory.common.id, actions=[])
