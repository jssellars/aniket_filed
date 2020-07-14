from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import ActionFieldCondition, \
    ActionFieldConditionOperatorEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.BudgetFieldMapper import BudgetFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.OneToOneFieldMapper import OneToOneFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.StructureFieldMapper import StructureFieldMapper, \
    StructureDetailsTypeEnum
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType
from Core.Web.FacebookGraphAPI.Models.FieldAggregationTypeEnum import FieldAggregationTypeEnum
from Core.Web.FacebookGraphAPI.Models.FieldDataTypeEnum import FieldDataTypeEnum

ad_creative_field_definition = 'adcreatives{account_id, actor_id, applink_treatment, asset_feed_spec, authorization_category,' \
                               'auto_update, body, branded_content_sponsor_page_id, call_to_action_type, categorization_criteria, bundle_folder_id, category_media_source, destination_set_id,' \
                               'effective_authorization_category, effective_instagram_story_id, dynamic_ad_voice, effective_object_story_id, enable_direct_install, id, image_crops,' \
                               'enable_launch_instant_app, image_hash, image_url, instagram_permalink_url, instagram_story_id, instagram_actor_id, interactive_components_spec, link_deep_link_url,' \
                               'link_url, messenger_sponsored_message, link_og_id, name, object_id, object_story_id, object_story_spec, object_store_url, object_type, object_url,' \
                               'platform_customizations, playable_asset_id, place_page_set_id, portrait_customizations, product_set_id, status, template_url, recommender_settings, thumbnail_url,' \
                               'title, url_tags, use_page_actor_override, video_id, template_url_spec}'


class FieldsStructureMetadata:
    name = Field(name="name",
                 facebook_fields=[GraphAPIInsightsFields.name],
                 mapper=OneToOneFieldMapper(),
                 field_type=FieldType.STRUCTURE,
                 data_type_id=FieldDataTypeEnum.TEXT.value,
                 aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    id = Field(name="id",
               facebook_fields=[GraphAPIInsightsFields.structure_id],
               mapper=OneToOneFieldMapper(),
               field_type=FieldType.STRUCTURE,
               data_type_id=FieldDataTypeEnum.TEXT.value,
               aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    buying_type = Field(name="buying_type",
                        facebook_fields=[GraphAPIInsightsFields.buying_type],
                        mapper=OneToOneFieldMapper(),
                        field_type=FieldType.STRUCTURE,
                        data_type_id=FieldDataTypeEnum.TEXT.value,
                        aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    effective_status = Field(name="effective_status",
                             facebook_fields=[GraphAPIInsightsFields.effective_status],
                             mapper=OneToOneFieldMapper(),
                             field_type=FieldType.STRUCTURE,
                             data_type_id=FieldDataTypeEnum.TEXT.value,
                             aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    tags = Field(name="tags",
                 facebook_fields=[GraphAPIInsightsFields.tags],
                 mapper=OneToOneFieldMapper(),
                 field_type=FieldType.STRUCTURE,
                 data_type_id=FieldDataTypeEnum.TEXT.value,
                 aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    created_at = Field(name="created_at",
                       facebook_fields=[GraphAPIInsightsFields.created_time],
                       mapper=OneToOneFieldMapper(),
                       field_type=FieldType.STRUCTURE,
                       data_type_id=FieldDataTypeEnum.DATE.value,
                       aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    last_significant_edit = Field(name="last_significant_edit",
                                  facebook_fields=[GraphAPIInsightsFields.last_significant_edit],
                                  mapper=OneToOneFieldMapper(),
                                  field_type=FieldType.STRUCTURE,
                                  data_type_id=FieldDataTypeEnum.DATE.value,
                                  aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    start_date = Field(name="start_time",
                       facebook_fields=[GraphAPIInsightsFields.start_time],
                       mapper=OneToOneFieldMapper(),
                       field_type=FieldType.STRUCTURE,
                       data_type_id=FieldDataTypeEnum.DATE.value,
                       aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    end_date = Field(name="stop_time",
                     facebook_fields=[GraphAPIInsightsFields.stop_time],
                     mapper=OneToOneFieldMapper(),
                     field_type=FieldType.STRUCTURE,
                     data_type_id=FieldDataTypeEnum.DATE.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    bid_strategy = Field(name="bid_strategy",
                         facebook_fields=[GraphAPIInsightsFields.bid_strategy],
                         mapper=OneToOneFieldMapper(),
                         field_type=FieldType.STRUCTURE,
                         data_type_id=FieldDataTypeEnum.TEXT.value,
                         aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    amount_spent_percentage = Field(name="amount_spent_percentage",
                                    facebook_fields=[GraphAPIInsightsFields.amount_spent_percentage],
                                    mapper=OneToOneFieldMapper(),
                                    field_type=FieldType.STRUCTURE)
    bid_cap = Field(name="bid_cap",
                    facebook_fields=[GraphAPIInsightsFields.bid_cap],
                    mapper=OneToOneFieldMapper(),
                    field_type=FieldType.STRUCTURE)
    budget = Field(name="budget",
                   facebook_fields=[GraphAPIInsightsFields.daily_budget,
                                    GraphAPIInsightsFields.lifetime_budget],
                   mapper=BudgetFieldMapper(facebook_field_names=[GraphAPIInsightsFields.daily_budget,
                                                                  GraphAPIInsightsFields.lifetime_budget]),
                   field_type=FieldType.STRUCTURE)
    daily_min_adset_budget = Field(name="daily_min_adset_budget",
                                   facebook_fields=[GraphAPIInsightsFields.daily_min_spend_target],
                                   mapper=OneToOneFieldMapper(),
                                   field_type=FieldType.STRUCTURE)
    daily_max_adset_budget = Field(name="daily_max_adset_budget",
                                   facebook_fields=[GraphAPIInsightsFields.daily_spend_cap],
                                   mapper=OneToOneFieldMapper(),
                                   field_type=FieldType.STRUCTURE)
    lifetime_min_adset_budget = Field(name="lifetime_min_adset_budget",
                                      facebook_fields=[GraphAPIInsightsFields.lifetime_min_spend_target],
                                      mapper=OneToOneFieldMapper(),
                                      field_type=FieldType.STRUCTURE)
    lifetime_max_adset_budget = Field(name="lifetime_max_adset_budget",
                                      facebook_fields=[GraphAPIInsightsFields.lifetime_spend_cap],
                                      mapper=OneToOneFieldMapper(),
                                      field_type=FieldType.STRUCTURE)
    budget_remaining = Field(name="budget_remaining",
                             facebook_fields=[GraphAPIInsightsFields.budget_remaining],
                             mapper=OneToOneFieldMapper(),
                             field_type=FieldType.STRUCTURE)
    ad_labels = Field(name="ad_labels",
                      facebook_fields=[GraphAPIInsightsFields.adlabels],
                      mapper=OneToOneFieldMapper(),
                      field_type=FieldType.STRUCTURE,
                      data_type_id=FieldDataTypeEnum.TEXT.value,
                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    boosted_object_id = Field(name="boosted_object_id",
                              facebook_fields=[GraphAPIInsightsFields.boosted_object_id],
                              mapper=OneToOneFieldMapper(),
                              field_type=FieldType.STRUCTURE,
                              data_type_id=FieldDataTypeEnum.TEXT.value,
                              aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    brand_lift_studies = Field(name="brand_lift_studies",
                               facebook_fields=[GraphAPIInsightsFields.brand_lift_studies],
                               mapper=OneToOneFieldMapper(),
                               field_type=FieldType.STRUCTURE,
                               data_type_id=FieldDataTypeEnum.TEXT.value,
                               aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    budget_rebalance_flag = Field(name="budget_rebalance_flag",
                                  facebook_fields=[GraphAPIInsightsFields.budget_rebalance_flag],
                                  mapper=OneToOneFieldMapper(),
                                  field_type=FieldType.STRUCTURE,
                                  data_type_id=FieldDataTypeEnum.TEXT.value,
                                  aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    can_create_brand_lift_study = Field(name="can_create_brand_lift_study",
                                        facebook_fields=[GraphAPIInsightsFields.can_create_brand_lift_study],
                                        mapper=OneToOneFieldMapper(),
                                        field_type=FieldType.STRUCTURE,
                                        data_type_id=FieldDataTypeEnum.TEXT.value,
                                        aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    configured_status = Field(name="configured_status",
                              facebook_fields=[GraphAPIInsightsFields.configured_status],
                              mapper=OneToOneFieldMapper(),
                              field_type=FieldType.STRUCTURE,
                              data_type_id=FieldDataTypeEnum.TEXT.value,
                              aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    can_use_spend_cap = Field(name="can_use_spend_cap",
                              facebook_fields=[GraphAPIInsightsFields.can_use_spend_cap],
                              mapper=OneToOneFieldMapper(),
                              field_type=FieldType.STRUCTURE,
                              data_type_id=FieldDataTypeEnum.TEXT.value,
                              aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    daily_budget = Field(name="daily_budget",
                         facebook_fields=[GraphAPIInsightsFields.daily_budget],
                         mapper=OneToOneFieldMapper(),
                         field_type=FieldType.STRUCTURE)
    last_budget_toggling_time = Field(name="last_budget_toggling_time",
                                      facebook_fields=[GraphAPIInsightsFields.last_budget_toggling_time],
                                      mapper=OneToOneFieldMapper(),
                                      field_type=FieldType.STRUCTURE,
                                      data_type_id=FieldDataTypeEnum.DATE.value,
                                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    lifetime_budget = Field(name="lifetime_budget",
                            facebook_fields=[GraphAPIInsightsFields.lifetime_budget],
                            mapper=OneToOneFieldMapper(),
                            field_type=FieldType.STRUCTURE)
    pacing_type = Field(name="pacing_type",
                        facebook_fields=[GraphAPIInsightsFields.pacing_type],
                        mapper=OneToOneFieldMapper(),
                        field_type=FieldType.STRUCTURE,
                        data_type_id=FieldDataTypeEnum.TEXT.value,
                        aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    recommendations = Field(name="recommendations",
                            facebook_fields=[GraphAPIInsightsFields.recommendations],
                            mapper=OneToOneFieldMapper(),
                            field_type=FieldType.STRUCTURE,
                            data_type_id=FieldDataTypeEnum.TEXT.value,
                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    promoted_object = Field(name="promoted_object",
                            facebook_fields=[GraphAPIInsightsFields.promoted_object],
                            mapper=OneToOneFieldMapper(),
                            field_type=FieldType.STRUCTURE,
                            data_type_id=FieldDataTypeEnum.TEXT.value,
                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    source_campaign = Field(name="source_campaign",
                            facebook_fields=[GraphAPIInsightsFields.source_campaign],
                            mapper=OneToOneFieldMapper(),
                            field_type=FieldType.STRUCTURE,
                            data_type_id=FieldDataTypeEnum.TEXT.value,
                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    special_ad_category = Field(name="special_ad_category",
                                facebook_fields=[GraphAPIInsightsFields.special_ad_category],
                                mapper=OneToOneFieldMapper(),
                                field_type=FieldType.STRUCTURE,
                                data_type_id=FieldDataTypeEnum.TEXT.value,
                                aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    source_campaign_id = Field(name="source_campaign_id",
                               facebook_fields=[GraphAPIInsightsFields.source_campaign_id],
                               mapper=OneToOneFieldMapper(),
                               field_type=FieldType.STRUCTURE,
                               data_type_id=FieldDataTypeEnum.TEXT.value,
                               aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    spend_cap = Field(name="spend_cap",
                      facebook_fields=[GraphAPIInsightsFields.spend_cap],
                      mapper=OneToOneFieldMapper(),
                      field_type=FieldType.STRUCTURE)
    top_line_id = Field(name="topline_id",
                        facebook_fields=[GraphAPIInsightsFields.topline_id],
                        mapper=OneToOneFieldMapper(),
                        field_type=FieldType.STRUCTURE,
                        data_type_id=FieldDataTypeEnum.TEXT.value,
                        aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    ad_rules_governed = Field(name="adrules_governed",
                              facebook_fields=[GraphAPIInsightsFields.adrules_governed],
                              mapper=OneToOneFieldMapper(),
                              field_type=FieldType.STRUCTURE,
                              data_type_id=FieldDataTypeEnum.TEXT.value,
                              aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    updated_time = Field(name="updated_time",
                         facebook_fields=[GraphAPIInsightsFields.updated_time],
                         mapper=OneToOneFieldMapper(),
                         field_type=FieldType.STRUCTURE,
                         data_type_id=FieldDataTypeEnum.DATE.value,
                         aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    copies = Field(name="copies",
                   facebook_fields=[GraphAPIInsightsFields.copies],
                   mapper=OneToOneFieldMapper(),
                   field_type=FieldType.STRUCTURE,
                   data_type_id=FieldDataTypeEnum.TEXT.value,
                   aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    adset_schedule = Field(name="adset_schedule",
                           facebook_fields=[GraphAPIInsightsFields.adset_schedule],
                           mapper=OneToOneFieldMapper(),
                           field_type=FieldType.STRUCTURE,
                           data_type_id=FieldDataTypeEnum.TEXT.value,
                           aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    asset_feed_id = Field(name="asset_feed_id",
                          facebook_fields=[GraphAPIInsightsFields.asset_feed_id],
                          mapper=OneToOneFieldMapper(),
                          field_type=FieldType.STRUCTURE,
                          data_type_id=FieldDataTypeEnum.TEXT.value,
                          aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    attribution_spec = Field(name="attribution_spec",
                             facebook_fields=[GraphAPIInsightsFields.attribution_spec],
                             mapper=OneToOneFieldMapper(),
                             field_type=FieldType.STRUCTURE,
                             data_type_id=FieldDataTypeEnum.TEXT.value,
                             aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    bid_adjustments = Field(name="bid_adjustments",
                            facebook_fields=[GraphAPIInsightsFields.bid_adjustments],
                            mapper=OneToOneFieldMapper(),
                            field_type=FieldType.STRUCTURE,
                            data_type_id=FieldDataTypeEnum.TEXT.value,
                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    bid_constraints = Field(name="bid_constraints",
                            facebook_fields=[GraphAPIInsightsFields.bid_constraints],
                            mapper=OneToOneFieldMapper(),
                            field_type=FieldType.STRUCTURE,
                            data_type_id=FieldDataTypeEnum.TEXT.value,
                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    bid_amount = Field(name="bid_amount",
                       facebook_fields=[GraphAPIInsightsFields.bid_amount],
                       mapper=OneToOneFieldMapper(),
                       field_type=FieldType.STRUCTURE)
    bid_info = Field(name="bid_info",
                     facebook_fields=[GraphAPIInsightsFields.bid_info],
                     mapper=OneToOneFieldMapper(),
                     field_type=FieldType.STRUCTURE,
                     data_type_id=FieldDataTypeEnum.TEXT.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    billing_event = Field(name="billing_event",
                          facebook_fields=[GraphAPIInsightsFields.billing_event],
                          mapper=OneToOneFieldMapper(),
                          field_type=FieldType.STRUCTURE,
                          data_type_id=FieldDataTypeEnum.TEXT.value,
                          aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    campaign = Field(name="campaign",
                     facebook_fields=[GraphAPIInsightsFields.campaign],
                     mapper=OneToOneFieldMapper(),
                     field_type=FieldType.STRUCTURE,
                     data_type_id=FieldDataTypeEnum.TEXT.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    daily_min_spend_target = Field(name="daily_min_spend_target",
                                   facebook_fields=[GraphAPIInsightsFields.daily_min_spend_target],
                                   mapper=OneToOneFieldMapper(),
                                   field_type=FieldType.STRUCTURE)
    destination_type = Field(name="destination_type",
                             facebook_fields=[GraphAPIInsightsFields.destination_type],
                             mapper=OneToOneFieldMapper(),
                             field_type=FieldType.STRUCTURE,
                             data_type_id=FieldDataTypeEnum.TEXT.value,
                             aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    end_time = Field(name="end_time",
                     facebook_fields=[GraphAPIInsightsFields.end_time],
                     mapper=OneToOneFieldMapper(),
                     field_type=FieldType.STRUCTURE,
                     data_type_id=FieldDataTypeEnum.DATE.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    frequency_control_specs = Field(name="frequency_control_specs",
                                    facebook_fields=[GraphAPIInsightsFields.frequency_control_specs],
                                    mapper=OneToOneFieldMapper(),
                                    field_type=FieldType.STRUCTURE,
                                    data_type_id=FieldDataTypeEnum.TEXT.value,
                                    aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    instagram_actor_id = Field(name="instagram_actor_id",
                               facebook_fields=[GraphAPIInsightsFields.instagram_actor_id],
                               mapper=OneToOneFieldMapper(),
                               field_type=FieldType.STRUCTURE,
                               data_type_id=FieldDataTypeEnum.TEXT.value,
                               aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    is_dynamic_creative = Field(name="is_dynamic_creative",
                                facebook_fields=[GraphAPIInsightsFields.is_dynamic_creative],
                                mapper=OneToOneFieldMapper(),
                                field_type=FieldType.STRUCTURE,
                                data_type_id=FieldDataTypeEnum.TEXT.value,
                                aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    issues_info = Field(name="issues_info",
                        facebook_fields=[GraphAPIInsightsFields.issues_info],
                        mapper=OneToOneFieldMapper(),
                        field_type=FieldType.STRUCTURE,
                        data_type_id=FieldDataTypeEnum.TEXT.value,
                        aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    lifetime_imps = Field(name="lifetime_imps",
                          facebook_fields=[GraphAPIInsightsFields.lifetime_imps],
                          mapper=OneToOneFieldMapper(),
                          field_type=FieldType.STRUCTURE,
                          data_type_id=FieldDataTypeEnum.TEXT.value,
                          aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    lifetime_spend_cap = Field(name="lifetime_spend_cap",
                               facebook_fields=[GraphAPIInsightsFields.lifetime_spend_cap],
                               mapper=OneToOneFieldMapper(),
                               field_type=FieldType.STRUCTURE)
    optimization_goal = Field(name="optimization_goal",
                              facebook_fields=[GraphAPIInsightsFields.optimization_goal],
                              mapper=OneToOneFieldMapper(),
                              field_type=FieldType.STRUCTURE,
                              data_type_id=FieldDataTypeEnum.TEXT.value,
                              aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    optimization_sub_event = Field(name="optimization_sub_event",
                                   facebook_fields=[GraphAPIInsightsFields.optimization_sub_event],
                                   mapper=OneToOneFieldMapper(),
                                   field_type=FieldType.STRUCTURE,
                                   data_type_id=FieldDataTypeEnum.TEXT.value,
                                   aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    source_adset = Field(name="source_adset",
                         facebook_fields=[GraphAPIInsightsFields.source_adset],
                         mapper=OneToOneFieldMapper(),
                         field_type=FieldType.STRUCTURE,
                         data_type_id=FieldDataTypeEnum.TEXT.value,
                         aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    source_adset_id = Field(name="source_adset_id",
                            facebook_fields=[GraphAPIInsightsFields.source_adset_id],
                            mapper=OneToOneFieldMapper(),
                            field_type=FieldType.STRUCTURE,
                            data_type_id=FieldDataTypeEnum.TEXT.value,
                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    targeting = Field(name="targeting",
                      facebook_fields=[GraphAPIInsightsFields.targeting],
                      mapper=OneToOneFieldMapper(),
                      field_type=FieldType.STRUCTURE,
                      data_type_id=FieldDataTypeEnum.TEXT.value,
                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    time_based_ad_rotation_id_blocks = Field(name="time_based_ad_rotation_id_blocks",
                                             facebook_fields=[GraphAPIInsightsFields.time_based_ad_rotation_id_blocks],
                                             mapper=OneToOneFieldMapper(),
                                             field_type=FieldType.STRUCTURE,
                                             data_type_id=FieldDataTypeEnum.TEXT.value,
                                             aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    time_based_ad_rotation_intervals = Field(name="time_based_ad_rotation_intervals",
                                             facebook_fields=[GraphAPIInsightsFields.time_based_ad_rotation_intervals],
                                             mapper=OneToOneFieldMapper(),
                                             field_type=FieldType.STRUCTURE,
                                             data_type_id=FieldDataTypeEnum.TEXT.value,
                                             aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    use_new_app_click = Field(name="use_new_app_click",
                              facebook_fields=[GraphAPIInsightsFields.use_new_app_click],
                              mapper=OneToOneFieldMapper(),
                              field_type=FieldType.STRUCTURE,
                              data_type_id=FieldDataTypeEnum.TEXT.value,
                              aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    lifetime_min_spend_target = Field(name="lifetime_min_spend_target",
                                      facebook_fields=[GraphAPIInsightsFields.lifetime_min_spend_target],
                                      mapper=OneToOneFieldMapper(),
                                      field_type=FieldType.STRUCTURE)
    targetingsentencelines = Field(name="targetingsentencelines",
                                   facebook_fields=[GraphAPIInsightsFields.targetingsentencelines],
                                   mapper=OneToOneFieldMapper(),
                                   field_type=FieldType.STRUCTURE,
                                   data_type_id=FieldDataTypeEnum.TEXT.value,
                                   aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    daily_spend_cap = Field(name="daily_spend_cap",
                            facebook_fields=[GraphAPIInsightsFields.daily_spend_cap],
                            mapper=OneToOneFieldMapper(),
                            field_type=FieldType.STRUCTURE)
    adset = Field(name="adset",
                  facebook_fields=[GraphAPIInsightsFields.adset],
                  mapper=OneToOneFieldMapper(),
                  field_type=FieldType.STRUCTURE,
                  data_type_id=FieldDataTypeEnum.TEXT.value,
                  aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    creative = Field(name="creative",
                     facebook_fields=[GraphAPIInsightsFields.creative],
                     mapper=OneToOneFieldMapper(),
                     field_type=FieldType.STRUCTURE,
                     data_type_id=FieldDataTypeEnum.TEXT.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    last_updated_by_app_id = Field(name="last_updated_by_app_id",
                                   facebook_fields=[GraphAPIInsightsFields.last_updated_by_app_id],
                                   mapper=OneToOneFieldMapper(),
                                   field_type=FieldType.STRUCTURE,
                                   data_type_id=FieldDataTypeEnum.DATE.value,
                                   aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    source_ad = Field(name="source_ad",
                      facebook_fields=[GraphAPIInsightsFields.source_ad],
                      mapper=OneToOneFieldMapper(),
                      field_type=FieldType.STRUCTURE,
                      data_type_id=FieldDataTypeEnum.TEXT.value,
                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    source_ad_id = Field(name="source_ad_id",
                         facebook_fields=[GraphAPIInsightsFields.source_ad_id],
                         mapper=OneToOneFieldMapper(),
                         field_type=FieldType.STRUCTURE,
                         data_type_id=FieldDataTypeEnum.TEXT.value,
                         aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    tracking_specs = Field(name="tracking_specs",
                           facebook_fields=[GraphAPIInsightsFields.tracking_specs],
                           mapper=OneToOneFieldMapper(),
                           field_type=FieldType.STRUCTURE,
                           data_type_id=FieldDataTypeEnum.TEXT.value,
                           aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    ad_creatives = Field(name="adcreatives",
                         facebook_fields=[GraphAPIInsightsFields.adcreatives],
                         mapper=OneToOneFieldMapper(),
                         field_type=FieldType.STRUCTURE,
                         data_type_id=FieldDataTypeEnum.TEXT.value,
                         aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    campaign_structure_name = Field(name="campaign_name",
                                    facebook_fields=[GraphAPIInsightsFields.campaign_name_structure],
                                    mapper=OneToOneFieldMapper(),
                                    field_type=FieldType.STRUCTURE,
                                    data_type_id=FieldDataTypeEnum.TEXT.value,
                                    aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    campaign_structure_id = Field(name="campaign_id",
                                  facebook_fields=[GraphAPIInsightsFields.campaign_id],
                                  mapper=OneToOneFieldMapper(),
                                  field_type=FieldType.STRUCTURE,
                                  data_type_id=FieldDataTypeEnum.TEXT.value,
                                  aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    adset_structure_name = Field(name="adset_name",
                                 facebook_fields=[GraphAPIInsightsFields.adset_name_structure],
                                 mapper=OneToOneFieldMapper(),
                                 field_type=FieldType.STRUCTURE,
                                 data_type_id=FieldDataTypeEnum.TEXT.value,
                                 aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    adset_structure_id = Field(name="adset_id",
                               facebook_fields=[GraphAPIInsightsFields.adset_id],
                               mapper=OneToOneFieldMapper(),
                               field_type=FieldType.STRUCTURE,
                               data_type_id=FieldDataTypeEnum.TEXT.value,
                               aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    ad_structure_name = Field(name="ad_name",
                              facebook_fields=[GraphAPIInsightsFields.ad_name],
                              mapper=OneToOneFieldMapper(),
                              field_type=FieldType.STRUCTURE,
                              data_type_id=FieldDataTypeEnum.TEXT.value,
                              aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    ad_structure_id = Field(name="ad_id",
                            facebook_fields=[GraphAPIInsightsFields.ad_id],
                            mapper=OneToOneFieldMapper(),
                            field_type=FieldType.STRUCTURE,
                            data_type_id=FieldDataTypeEnum.TEXT.value,
                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    ad_account_structure_id = Field(name="account_id",
                                    facebook_fields=[GraphAPIInsightsFields.account_id],
                                    mapper=OneToOneFieldMapper(),
                                    field_type=FieldType.STRUCTURE,
                                    data_type_id=FieldDataTypeEnum.TEXT.value,
                                    aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    ad_account_structure_name = Field(name="account_name",
                                      facebook_fields=[GraphAPIInsightsFields.account_name],
                                      mapper=OneToOneFieldMapper(),
                                      field_type=FieldType.STRUCTURE,
                                      data_type_id=FieldDataTypeEnum.TEXT.value,
                                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    objective_structure = Field(name="objective",
                                facebook_fields=[GraphAPIInsightsFields.objective],
                                mapper=OneToOneFieldMapper(),
                                field_type=FieldType.STRUCTURE,
                                data_type_id=FieldDataTypeEnum.TEXT.value,
                                aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    status = Field(name="status",
                   facebook_fields=[GraphAPIInsightsFields.status],
                   mapper=OneToOneFieldMapper(),
                   field_type=FieldType.STRUCTURE,
                   data_type_id=FieldDataTypeEnum.TEXT.value,
                   aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    delivery = Field(name="effective_status",
                     facebook_fields=[GraphAPIInsightsFields.effective_status],
                     mapper=OneToOneFieldMapper(),
                     field_type=FieldType.STRUCTURE,
                     data_type_id=FieldDataTypeEnum.TEXT.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    adset_delivery = Field(name="adset_delivery",
                           facebook_fields=[GraphAPIInsightsFields.adset,
                                            GraphAPIInsightsFields.effective_status],
                           mapper=OneToOneFieldMapper(facebook_field_name=GraphAPIInsightsFields.effective_status),
                           field_type=FieldType.STRUCTURE,
                           data_type_id=FieldDataTypeEnum.TEXT.value,
                           aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    lifetime_spent = Field(name="lifetime_spent",
                           facebook_fields=[GraphAPIInsightsFields.lifetime_spent],
                           mapper=OneToOneFieldMapper(),
                           field_type=FieldType.STRUCTURE)
    location = Field(name="location",
                     facebook_fields=[GraphAPIInsightsFields.targetingsentencelines],
                     mapper=StructureFieldMapper(field_filter=[
                         ActionFieldCondition(field_name=GraphAPIInsightsFields.targeting_sentence_lines_content,
                                              operator=ActionFieldConditionOperatorEnum.LIKE,
                                              field_value=GraphAPIInsightsFields.location_structure)],
                         structure_details_type=StructureDetailsTypeEnum.TARGETING_SENTENCE_LINES),
                     field_type=FieldType.STRUCTURE,
                     data_type_id=FieldDataTypeEnum.TEXT.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    age = Field(name="age",
                facebook_fields=[GraphAPIInsightsFields.targetingsentencelines],
                mapper=StructureFieldMapper(field_filter=[
                    ActionFieldCondition(field_name=GraphAPIInsightsFields.targeting_sentence_lines_content,
                                         operator=ActionFieldConditionOperatorEnum.LIKE,
                                         field_value=GraphAPIInsightsFields.age_structure)],
                    structure_details_type=StructureDetailsTypeEnum.TARGETING_SENTENCE_LINES),
                field_type=FieldType.STRUCTURE,
                data_type_id=FieldDataTypeEnum.TEXT.value,
                aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    gender = Field(name="gender",
                   facebook_fields=[GraphAPIInsightsFields.targetingsentencelines],
                   mapper=StructureFieldMapper(field_filter=[
                       ActionFieldCondition(field_name=GraphAPIInsightsFields.targeting_sentence_lines_content,
                                            operator=ActionFieldConditionOperatorEnum.LIKE,
                                            field_value=GraphAPIInsightsFields.gender_structure)],
                       structure_details_type=StructureDetailsTypeEnum.TARGETING_SENTENCE_LINES),
                   field_type=FieldType.STRUCTURE,
                   data_type_id=FieldDataTypeEnum.TEXT.value,
                   aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    included_custom_audiences = Field(name="included_custom_audiences",
                                      facebook_fields=[GraphAPIInsightsFields.targetingsentencelines],
                                      mapper=StructureFieldMapper(
                                          field_filter=[ActionFieldCondition(
                                              field_name=GraphAPIInsightsFields.targeting_sentence_lines_content,
                                              operator=ActionFieldConditionOperatorEnum.LIKE,
                                              field_value=GraphAPIInsightsFields.included_custom_audiences_structure)],
                                          structure_details_type=StructureDetailsTypeEnum.TARGETING_SENTENCE_LINES),
                                      field_type=FieldType.STRUCTURE,
                                      data_type_id=FieldDataTypeEnum.TEXT.value,
                                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    excluded_custom_audiences = Field(name="excluded_custom_audiences",
                                      facebook_fields=[GraphAPIInsightsFields.targetingsentencelines],
                                      mapper=StructureFieldMapper(
                                          field_filter=[ActionFieldCondition(
                                              field_name=GraphAPIInsightsFields.targeting_sentence_lines_content,
                                              operator=ActionFieldConditionOperatorEnum.LIKE,
                                              field_value=GraphAPIInsightsFields.excluded_custom_audiences_structure)],
                                          structure_details_type=StructureDetailsTypeEnum.TARGETING_SENTENCE_LINES),
                                      field_type=FieldType.STRUCTURE,
                                      data_type_id=FieldDataTypeEnum.TEXT.value,
                                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    page_name = Field(name="page_name",
                      facebook_fields=[GraphAPIInsightsFields.page_id_structure],
                      mapper=StructureFieldMapper(structure_details_type=StructureDetailsTypeEnum.TRACKING_SPECS),
                      field_type=FieldType.STRUCTURE,
                      data_type_id=FieldDataTypeEnum.TEXT.value,
                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    headline = Field(name="headline",
                     facebook_fields=[GraphAPIInsightsFields.headline],
                     mapper=StructureFieldMapper(),
                     field_type=FieldType.STRUCTURE,
                     data_type_id=FieldDataTypeEnum.TEXT.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    body = Field(name="ad_copy_body",
                 facebook_fields=[GraphAPIInsightsFields.body],
                 mapper=StructureFieldMapper(),
                 field_type=FieldType.STRUCTURE,
                 data_type_id=FieldDataTypeEnum.TEXT.value,
                 aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    link = Field(name="ad_copy_link",
                 facebook_fields=[GraphAPIInsightsFields.link_url],
                 mapper=StructureFieldMapper(),
                 field_type=FieldType.STRUCTURE,
                 data_type_id=FieldDataTypeEnum.TEXT.value,
                 aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    destination = Field(name="destination",
                        facebook_fields=[GraphAPIInsightsFields.targetingsentencelines],
                        mapper=StructureFieldMapper(field_filter=[
                            ActionFieldCondition(field_name=GraphAPIInsightsFields.targeting_sentence_lines_content,
                                                 operator=ActionFieldConditionOperatorEnum.LIKE,
                                                 field_value=GraphAPIInsightsFields.excluded_custom_audiences_structure)],
                            structure_details_type=StructureDetailsTypeEnum.TARGETING_SENTENCE_LINES),
                        field_type=FieldType.STRUCTURE,
                        data_type_id=FieldDataTypeEnum.TEXT.value,
                        aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    url_parameters = Field(name="url_parameters",
                           facebook_fields=[GraphAPIInsightsFields.url_parameters],
                           mapper=StructureFieldMapper(),
                           field_type=FieldType.STRUCTURE,
                           data_type_id=FieldDataTypeEnum.TEXT.value,
                           aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    pixel = Field(name="pixel",
                  facebook_fields=[GraphAPIInsightsFields.facebook_pixel_structure],
                  mapper=StructureFieldMapper(structure_details_type=StructureDetailsTypeEnum.PROMOTED_OBJECT),
                  field_type=FieldType.STRUCTURE,
                  data_type_id=FieldDataTypeEnum.TEXT.value,
                  aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    learning_stage_info = Field(name="learning_stage_info",
                                facebook_fields=[GraphAPIInsightsFields.learning_stage_info],
                                mapper=StructureFieldMapper(),
                                field_type=FieldType.STRUCTURE,
                                data_type_id=FieldDataTypeEnum.TEXT.value,
                                aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    # todo: check app event values from tracking spec
    app_event = Field(name="app_event",
                      facebook_fields=[GraphAPIInsightsFields.app_event_structure],
                      mapper=StructureFieldMapper(structure_details_type=StructureDetailsTypeEnum.PROMOTED_OBJECT),
                      field_type=FieldType.STRUCTURE,
                      data_type_id=FieldDataTypeEnum.TEXT.value,
                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    # todo: investigate how to get this value from FB
    # offline_event = Field(name="offline_event",
    #                       facebook_fields=[GraphAPIInsightsFields.targetingsentencelines],
    #                       mapper=StructureFieldMapper(),
    #                       field_type=FieldType.STRUCTURE)
