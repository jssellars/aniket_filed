from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import ActionFieldCondition, \
    ActionFieldConditionOperatorEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldMapper import ActionFieldMapper
from Core.Web.FacebookGraphAPI.Models.Field import FieldType, Field


class FieldsMetricStandardEventsMetadata:
    # todo: check all standard events again
    # todo: add on-facebook options where applicable
    # todo: applications submitted
    # todo: appointments scheduled
    # todo: contacts
    # todo: get direction clicks
    # todo: donations
    # todo: in-app ad clicks
    # todo: in-app ad impressions
    # todo: location searches
    # todo: trial started
    # todo: phone number clicks
    # todo: products customised
    # todo: store visits
    # todo: levels achieved
    # todo: ratings submitted
    # todo: on-facebook adds to cart on-facebook add to cart conversion value
    # todo: on-facebook view content event and on-facebook view content conversion value
    # todo: mobile app custom events
    # todo: other offline conversions
    # todo: mobile app and website subscriptions

    # achievements unlocked
    achievements_unlocked_total = Field(name='achievements_unlocked_total',
                                        facebook_fields=[GraphAPIInsightsFields.actions],
                                        mapper=ActionFieldMapper(field_filter=[
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.mobile_achievement_unlocked)]),
                                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                                        field_type=FieldType.ACTION_INSIGHT)
    achievements_unlocked_unique = Field(name='achievements_unlocked_unique',
                                         facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                         mapper=ActionFieldMapper(field_filter=[
                                             ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                  operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                  field_value=GraphAPIInsightsFields.mobile_achievement_unlocked)]),
                                         action_breakdowns=[GraphAPIInsightsFields.action_type],
                                         field_type=FieldType.ACTION_INSIGHT)
    achievements_unlocked_unique_cost = Field(name='achievements_unlocked_unique_cost',
                                              facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                              mapper=ActionFieldMapper(field_filter=[
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.mobile_achievement_unlocked)]),
                                              action_breakdowns=[GraphAPIInsightsFields.action_type],
                                              field_type=FieldType.ACTION_INSIGHT)
    achievements_unlocked_cost = Field(name='achievements_unlocked_cost',
                                       facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.mobile_achievement_unlocked)]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                                       field_type=FieldType.ACTION_INSIGHT)
    achievements_unlocked_value = Field(name='achievements_unlocked_value',
                                        facebook_fields=[GraphAPIInsightsFields.action_values],
                                        mapper=ActionFieldMapper(field_filter=[
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.mobile_achievement_unlocked)]),
                                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                                        field_type=FieldType.ACTION_INSIGHT)
    # app ads of payment info
    mobile_app_adds_of_payment_info_total = Field(name='mobile_app_adds_of_payment_info_total',
                                                  facebook_fields=[GraphAPIInsightsFields.actions],
                                                  mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                      field_name=GraphAPIInsightsFields.action_type,
                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                      field_value=GraphAPIInsightsFields.app_adds_of_payment_info),
                                                      ActionFieldCondition(
                                                          field_name=GraphAPIInsightsFields.action_device,
                                                          operator=ActionFieldConditionOperatorEnum.IN,
                                                          field_value=[
                                                              GraphAPIInsightsFields.action_device_ipad,
                                                              GraphAPIInsightsFields.action_device_android,
                                                              GraphAPIInsightsFields.action_device_iphone,
                                                              GraphAPIInsightsFields.action_device_ipod,
                                                              GraphAPIInsightsFields.action_device_smartphone,
                                                              GraphAPIInsightsFields.action_device_tablet])]),
                                                  action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                  field_type=FieldType.ACTION_INSIGHT)
    website_app_adds_of_payment_info_total = Field(name='website_app_adds_of_payment_info_total',
                                                   facebook_fields=[GraphAPIInsightsFields.actions],
                                                   mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                       field_name=GraphAPIInsightsFields.action_type,
                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                       field_value=GraphAPIInsightsFields.app_adds_of_payment_info),
                                                       ActionFieldCondition(
                                                           field_name=GraphAPIInsightsFields.action_device,
                                                           operator=ActionFieldConditionOperatorEnum.IN,
                                                           field_value=[
                                                               GraphAPIInsightsFields.action_device_web])]),
                                                   action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                                      GraphAPIInsightsFields.action_device],
                                                   field_type=FieldType.ACTION_INSIGHT)
    offline_app_adds_of_payment_info_total = Field(name='offline_app_adds_of_payment_info_total',
                                                   facebook_fields=[GraphAPIInsightsFields.actions],
                                                   mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                       field_name=GraphAPIInsightsFields.action_type,
                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                       field_value=GraphAPIInsightsFields.app_adds_of_payment_info),
                                                       ActionFieldCondition(
                                                           field_name=GraphAPIInsightsFields.action_device,
                                                           operator=ActionFieldConditionOperatorEnum.IN,
                                                           field_value=[
                                                               GraphAPIInsightsFields.action_device_offline])]),
                                                   action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                                      GraphAPIInsightsFields.action_device],
                                                   field_type=FieldType.ACTION_INSIGHT)
    app_adds_of_payment_info_unique = Field(name='app_adds_of_payment_info_unique',
                                            facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                            mapper=ActionFieldMapper(field_filter=[
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.app_adds_of_payment_info)]),
                                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                                            field_type=FieldType.ACTION_INSIGHT)

    mobile_app_adds_of_payment_info_value = Field(name='mobile_app_adds_of_payment_info_value',
                                                  facebook_fields=[GraphAPIInsightsFields.action_values],
                                                  mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                      field_name=GraphAPIInsightsFields.action_type,
                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                      field_value=GraphAPIInsightsFields.app_adds_of_payment_info),
                                                      ActionFieldCondition(
                                                          field_name=GraphAPIInsightsFields.action_device,
                                                          operator=ActionFieldConditionOperatorEnum.IN,
                                                          field_value=[
                                                              GraphAPIInsightsFields.action_device_ipad,
                                                              GraphAPIInsightsFields.action_device_android,
                                                              GraphAPIInsightsFields.action_device_iphone,
                                                              GraphAPIInsightsFields.action_device_ipod,
                                                              GraphAPIInsightsFields.action_device_smartphone,
                                                              GraphAPIInsightsFields.action_device_tablet])]),
                                                  action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                                     GraphAPIInsightsFields.action_device],
                                                  field_type=FieldType.ACTION_INSIGHT)
    website_app_adds_of_payment_info_value = Field(name='website_app_adds_of_payment_info_value',
                                                   facebook_fields=[GraphAPIInsightsFields.action_values],
                                                   mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                       field_name=GraphAPIInsightsFields.action_type,
                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                       field_value=GraphAPIInsightsFields.app_adds_of_payment_info),
                                                       ActionFieldCondition(
                                                           field_name=GraphAPIInsightsFields.action_device,
                                                           operator=ActionFieldConditionOperatorEnum.IN,
                                                           field_value=[
                                                               GraphAPIInsightsFields.action_device_web])]),
                                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                   field_type=FieldType.ACTION_INSIGHT)
    offline_app_adds_of_payment_info_value = Field(name='offline_app_adds_of_payment_info_value',
                                                   facebook_fields=[GraphAPIInsightsFields.action_values],
                                                   mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                       field_name=GraphAPIInsightsFields.action_type,
                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                       field_value=GraphAPIInsightsFields.app_adds_of_payment_info),
                                                       ActionFieldCondition(
                                                           field_name=GraphAPIInsightsFields.action_device,
                                                           operator=ActionFieldConditionOperatorEnum.IN,
                                                           field_value=[
                                                               GraphAPIInsightsFields.action_device_offline])]),
                                                   action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                                      GraphAPIInsightsFields.action_device],
                                                   field_type=FieldType.ACTION_INSIGHT)
    app_adds_of_payment_info_cost = Field(name='app_adds_of_payment_info_cost',
                                          facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                          mapper=ActionFieldMapper(field_filter=[
                                              ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.app_adds_of_payment_info)]),
                                          action_breakdowns=[GraphAPIInsightsFields.action_type],
                                          field_type=FieldType.ACTION_INSIGHT)
    app_adds_of_payment_info_unique_cost = Field(name='app_adds_of_payment_info_unique_cost',
                                                 facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                                 mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                     field_name=GraphAPIInsightsFields.action_type,
                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                     field_value=GraphAPIInsightsFields.app_adds_of_payment_info)]),
                                                 action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                 field_type=FieldType.ACTION_INSIGHT)
    # adds to wishlist
    mobile_adds_to_wish_list_total = Field(name='mobile_adds_to_wish_list_total',
                                           facebook_fields=[GraphAPIInsightsFields.actions],
                                           mapper=ActionFieldMapper(field_filter=[
                                               ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.adds_to_wish_list),
                                               ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                    operator=ActionFieldConditionOperatorEnum.IN,
                                                                    field_value=[
                                                                        GraphAPIInsightsFields.action_device_ipad,
                                                                        GraphAPIInsightsFields.action_device_android,
                                                                        GraphAPIInsightsFields.action_device_iphone,
                                                                        GraphAPIInsightsFields.action_device_ipod,
                                                                        GraphAPIInsightsFields.action_device_smartphone,
                                                                        GraphAPIInsightsFields.action_device_tablet])]),
                                           action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                              GraphAPIInsightsFields.action_device],
                                           field_type=FieldType.ACTION_INSIGHT)
    website_adds_to_wish_list_total = Field(name='website_adds_to_wish_list_total',
                                            facebook_fields=[GraphAPIInsightsFields.actions],
                                            mapper=ActionFieldMapper(field_filter=[
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.adds_to_wish_list),
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                     operator=ActionFieldConditionOperatorEnum.IN,
                                                                     field_value=[
                                                                         GraphAPIInsightsFields.action_device_web])]),
                                            action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                               GraphAPIInsightsFields.action_device],
                                            field_type=FieldType.ACTION_INSIGHT)
    offline_adds_to_wish_list_total = Field(name='offline_adds_to_wish_list_total',
                                            facebook_fields=[GraphAPIInsightsFields.actions],
                                            mapper=ActionFieldMapper(field_filter=[
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.adds_to_wish_list),
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                     operator=ActionFieldConditionOperatorEnum.IN,
                                                                     field_value=[
                                                                         GraphAPIInsightsFields.action_device_offline])]),
                                            action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                               GraphAPIInsightsFields.action_device],
                                            field_type=FieldType.ACTION_INSIGHT)
    adds_to_wish_list_unique = Field(name='adds_to_wish_list_unique',
                                     facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                     mapper=ActionFieldMapper(field_filter=[
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.adds_to_wish_list)]),
                                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                                     field_type=FieldType.ACTION_INSIGHT)
    mobile_adds_to_wish_list_value = Field(name='mobile_adds_to_wish_list_value',
                                           facebook_fields=[GraphAPIInsightsFields.action_values],
                                           mapper=ActionFieldMapper(field_filter=[
                                               ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.adds_to_wish_list),
                                               ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                    operator=ActionFieldConditionOperatorEnum.IN,
                                                                    field_value=[
                                                                        GraphAPIInsightsFields.action_device_ipad,
                                                                        GraphAPIInsightsFields.action_device_android,
                                                                        GraphAPIInsightsFields.action_device_iphone,
                                                                        GraphAPIInsightsFields.action_device_ipod,
                                                                        GraphAPIInsightsFields.action_device_smartphone,
                                                                        GraphAPIInsightsFields.action_device_tablet])]),
                                           action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                              GraphAPIInsightsFields.action_device],
                                           field_type=FieldType.ACTION_INSIGHT)
    website_adds_to_wish_list_value = Field(name='website_adds_to_wish_list_value',
                                            facebook_fields=[GraphAPIInsightsFields.action_values],
                                            mapper=ActionFieldMapper(field_filter=[
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.adds_to_wish_list),
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                     operator=ActionFieldConditionOperatorEnum.IN,
                                                                     field_value=[
                                                                         GraphAPIInsightsFields.action_device_web])]),
                                            action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                               GraphAPIInsightsFields.action_device],
                                            field_type=FieldType.ACTION_INSIGHT)
    offline_adds_to_wish_list_value = Field(name='offline_adds_to_wish_list_value',
                                            facebook_fields=[GraphAPIInsightsFields.action_values],
                                            mapper=ActionFieldMapper(field_filter=[
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.adds_to_wish_list),
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                     operator=ActionFieldConditionOperatorEnum.IN,
                                                                     field_value=[
                                                                         GraphAPIInsightsFields.action_device_offline])]),
                                            action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                               GraphAPIInsightsFields.action_device],
                                            field_type=FieldType.ACTION_INSIGHT)
    adds_to_wish_list_cost = Field(name='adds_to_wish_list_cost',
                                   facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                   mapper=ActionFieldMapper(field_filter=[
                                       ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.adds_to_wish_list)]),
                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                   field_type=FieldType.ACTION_INSIGHT)
    adds_to_wish_list_unique_cost = Field(name='adds_to_wish_list_unique_cost',
                                          facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                          mapper=ActionFieldMapper(field_filter=[
                                              ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.adds_to_wish_list)]),
                                          action_breakdowns=[GraphAPIInsightsFields.action_type],
                                          field_type=FieldType.ACTION_INSIGHT)
    # adds to cart
    mobile_adds_to_cart_total = Field(name='mobile_adds_to_cart_total',
                                      facebook_fields=[GraphAPIInsightsFields.actions],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.adds_to_cart),
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                               operator=ActionFieldConditionOperatorEnum.IN,
                                                               field_value=[
                                                                   GraphAPIInsightsFields.action_device_ipad,
                                                                   GraphAPIInsightsFields.action_device_android,
                                                                   GraphAPIInsightsFields.action_device_iphone,
                                                                   GraphAPIInsightsFields.action_device_ipod,
                                                                   GraphAPIInsightsFields.action_device_smartphone,
                                                                   GraphAPIInsightsFields.action_device_tablet])]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                         GraphAPIInsightsFields.action_device],
                                      field_type=FieldType.ACTION_INSIGHT)
    website_adds_to_cart_total = Field(name='website_adds_to_cart_total',
                                       facebook_fields=[GraphAPIInsightsFields.actions],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.adds_to_cart),
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                operator=ActionFieldConditionOperatorEnum.IN,
                                                                field_value=[
                                                                    GraphAPIInsightsFields.action_device_web])]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                          GraphAPIInsightsFields.action_device],
                                       field_type=FieldType.ACTION_INSIGHT)
    offline_adds_to_cart_total = Field(name='offline_adds_to_cart_total',
                                       facebook_fields=[GraphAPIInsightsFields.actions],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.adds_to_cart),
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                operator=ActionFieldConditionOperatorEnum.IN,
                                                                field_value=[
                                                                    GraphAPIInsightsFields.action_device_offline])]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                          GraphAPIInsightsFields.action_device],
                                       field_type=FieldType.ACTION_INSIGHT)
    adds_to_cart_unique = Field(name='adds_to_cart_unique',
                                facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                mapper=ActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.adds_to_cart)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                field_type=FieldType.ACTION_INSIGHT)
    mobile_adds_to_cart_value = Field(name='mobile_adds_to_cart_value',
                                      facebook_fields=[GraphAPIInsightsFields.action_values],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.adds_to_cart),
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                               operator=ActionFieldConditionOperatorEnum.IN,
                                                               field_value=[
                                                                   GraphAPIInsightsFields.action_device_ipad,
                                                                   GraphAPIInsightsFields.action_device_android,
                                                                   GraphAPIInsightsFields.action_device_iphone,
                                                                   GraphAPIInsightsFields.action_device_ipod,
                                                                   GraphAPIInsightsFields.action_device_smartphone,
                                                                   GraphAPIInsightsFields.action_device_tablet])]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                         GraphAPIInsightsFields.action_device],
                                      field_type=FieldType.ACTION_INSIGHT)
    website_adds_to_cart_value = Field(name='website_adds_to_cart_value',
                                       facebook_fields=[GraphAPIInsightsFields.action_values],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.adds_to_cart),
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                operator=ActionFieldConditionOperatorEnum.IN,
                                                                field_value=[
                                                                    GraphAPIInsightsFields.action_device_web])]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                          GraphAPIInsightsFields.action_device],
                                       field_type=FieldType.ACTION_INSIGHT)
    offline_adds_to_cart_value = Field(name='offline_adds_to_cart_value',
                                       facebook_fields=[GraphAPIInsightsFields.action_values],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.adds_to_cart),
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                operator=ActionFieldConditionOperatorEnum.IN,
                                                                field_value=[
                                                                    GraphAPIInsightsFields.action_device_offline])]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                          GraphAPIInsightsFields.action_device],
                                       field_type=FieldType.ACTION_INSIGHT)
    adds_to_cart_cost = Field(name='adds_to_cart_cost',
                              facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                              mapper=ActionFieldMapper(
                                  field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.adds_to_cart)]),
                              action_breakdowns=[GraphAPIInsightsFields.action_type],
                              field_type=FieldType.ACTION_INSIGHT)
    adds_to_cart_unique_cost = Field(name='adds_to_cart_unique_cost',
                                     facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                     mapper=ActionFieldMapper(field_filter=[
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.adds_to_cart)]),
                                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                                     field_type=FieldType.ACTION_INSIGHT)
    #  app activations
    app_activations_total = Field(name='app_activations_total',
                                  facebook_fields=[GraphAPIInsightsFields.actions],
                                  mapper=ActionFieldMapper(
                                      field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                         operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                         field_value=GraphAPIInsightsFields.app_activations)]),
                                  action_breakdowns=[GraphAPIInsightsFields.action_type],
                                  field_type=FieldType.ACTION_INSIGHT)
    app_activations_unique = Field(name='app_activations_unique',
                                   facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                   mapper=ActionFieldMapper(field_filter=[
                                       ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.app_activations)]),
                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                   field_type=FieldType.ACTION_INSIGHT)
    app_activations_value = Field(name='app_activations_value',
                                  facebook_fields=[GraphAPIInsightsFields.action_values],
                                  mapper=ActionFieldMapper(
                                      field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                         operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                         field_value=GraphAPIInsightsFields.app_activations)]),
                                  action_breakdowns=[GraphAPIInsightsFields.action_type],
                                  field_type=FieldType.ACTION_INSIGHT)
    app_activations_cost = Field(name='app_activations_cost',
                                 facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                 mapper=ActionFieldMapper(
                                     field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                        operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                        field_value=GraphAPIInsightsFields.app_activations)]),
                                 action_breakdowns=[GraphAPIInsightsFields.action_type],
                                 field_type=FieldType.ACTION_INSIGHT)
    app_activations_unique_cost = Field(name='app_activations_unique_cost',
                                        facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                        mapper=ActionFieldMapper(field_filter=[
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.app_activations)]),
                                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                                        field_type=FieldType.ACTION_INSIGHT)
    # app installs
    app_installs_total = Field(name='app_installs_total',
                               facebook_fields=[GraphAPIInsightsFields.actions],
                               mapper=ActionFieldMapper(field_filter=[
                                   ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                        operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                        field_value=GraphAPIInsightsFields.app_installs)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_type],
                               field_type=FieldType.ACTION_INSIGHT)
    mobile_app_installs_total = Field(name='mobile_app_installs_total',
                                      facebook_fields=[GraphAPIInsightsFields.actions],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.mobile_app_install),
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                               operator=ActionFieldConditionOperatorEnum.IN,
                                                               field_value=[
                                                                   GraphAPIInsightsFields.action_device_ipad,
                                                                   GraphAPIInsightsFields.action_device_android,
                                                                   GraphAPIInsightsFields.action_device_iphone,
                                                                   GraphAPIInsightsFields.action_device_ipod,
                                                                   GraphAPIInsightsFields.action_device_smartphone,
                                                                   GraphAPIInsightsFields.action_device_tablet])]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                         GraphAPIInsightsFields.action_device],
                                      field_type=FieldType.ACTION_INSIGHT)
    website_app_installs_total = Field(name='website_app_installs_total',
                                       facebook_fields=[GraphAPIInsightsFields.actions],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.app_installs),
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                operator=ActionFieldConditionOperatorEnum.IN,
                                                                field_value=[
                                                                    GraphAPIInsightsFields.action_device_web])]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                          GraphAPIInsightsFields.action_device],
                                       field_type=FieldType.ACTION_INSIGHT)
    app_install_cost = Field(name='website_app_installs_total',
                             facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                             mapper=ActionFieldMapper(
                                 field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.app_installs)]),
                             action_breakdowns=[GraphAPIInsightsFields.action_type],
                             field_type=FieldType.ACTION_INSIGHT)
    # checkouts initiated
    mobile_checkouts_initiated_total = Field(name='mobile_checkouts_initiated_total',
                                             facebook_fields=[GraphAPIInsightsFields.actions],
                                             mapper=ActionFieldMapper(field_filter=[
                                                 ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.mobile_app_checkouts_initiated)]),
                                             action_breakdowns=[GraphAPIInsightsFields.action_type],
                                             field_type=FieldType.ACTION_INSIGHT)
    website_checkouts_initiated_total = Field(name='website_checkouts_initiated_total',
                                              facebook_fields=[GraphAPIInsightsFields.actions],
                                              mapper=ActionFieldMapper(field_filter=[
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.website_checkouts_initiated)]),
                                              action_breakdowns=[GraphAPIInsightsFields.action_type],
                                              field_type=FieldType.ACTION_INSIGHT)
    offline_checkouts_initiated_total = Field(name='offline_checkouts_initiated_total',
                                              facebook_fields=[GraphAPIInsightsFields.actions],
                                              mapper=ActionFieldMapper(field_filter=[
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.website_checkouts_initiated),
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                       operator=ActionFieldConditionOperatorEnum.IN,
                                                                       field_value=[
                                                                           GraphAPIInsightsFields.action_device_offline])]),
                                              action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                                 GraphAPIInsightsFields.action_device],
                                              field_type=FieldType.ACTION_INSIGHT)
    mobile_checkouts_initiated_value = Field(name='mobile_checkouts_initiated_value',
                                             facebook_fields=[GraphAPIInsightsFields.action_values],
                                             mapper=ActionFieldMapper(field_filter=[
                                                 ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.mobile_app_checkouts_initiated)]),
                                             action_breakdowns=[GraphAPIInsightsFields.action_type],
                                             field_type=FieldType.ACTION_INSIGHT)
    website_checkouts_initiated_value = Field(name='website_checkouts_initiated_value',
                                              facebook_fields=[GraphAPIInsightsFields.action_values],
                                              mapper=ActionFieldMapper(field_filter=[
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.website_checkouts_initiated)]),
                                              action_breakdowns=[GraphAPIInsightsFields.action_type],
                                              field_type=FieldType.ACTION_INSIGHT)
    offline_checkouts_initiated_value = Field(name='offline_checkouts_initiated_value',
                                              facebook_fields=[GraphAPIInsightsFields.action_values],
                                              mapper=ActionFieldMapper(field_filter=[
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.website_checkouts_initiated),
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                       operator=ActionFieldConditionOperatorEnum.IN,
                                                                       field_value=[
                                                                           GraphAPIInsightsFields.action_device_offline])]),
                                              action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                                 GraphAPIInsightsFields.action_device],
                                              field_type=FieldType.ACTION_INSIGHT)
    checkouts_initiated_cost = Field(name='checkouts_initiated_cost',
                                     facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                     mapper=ActionFieldMapper(field_filter=[
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.website_checkouts_initiated)]),
                                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                                     field_type=FieldType.ACTION_INSIGHT)
    checkouts_initiated_unique_cost = Field(name='checkouts_initiated_unique_cost',
                                            facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                            mapper=ActionFieldMapper(field_filter=[
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.website_checkouts_initiated)]),
                                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                                            field_type=FieldType.ACTION_INSIGHT)
    checkouts_initiated_unique_total = Field(name='checkouts_initiated_unique_total',
                                             facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                             mapper=ActionFieldMapper(field_filter=[
                                                 ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.website_checkouts_initiated)]),
                                             action_breakdowns=[GraphAPIInsightsFields.action_type],
                                             field_type=FieldType.ACTION_INSIGHT)
    # content views
    mobile_content_views_total = Field(name='mobile_content_views_total',
                                       facebook_fields=[GraphAPIInsightsFields.actions],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.mobile_app_content_views)]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                                       field_type=FieldType.ACTION_INSIGHT)
    website_content_views_total = Field(name='website_content_views_total',
                                        facebook_fields=[GraphAPIInsightsFields.actions],
                                        mapper=ActionFieldMapper(field_filter=[
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.website_content_views)]),
                                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                                        field_type=FieldType.ACTION_INSIGHT)
    offline_content_views_total = Field(name='offline_content_views_total',
                                        facebook_fields=[GraphAPIInsightsFields.actions],
                                        mapper=ActionFieldMapper(field_filter=[
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.content_views),
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                 operator=ActionFieldConditionOperatorEnum.IN,
                                                                 field_value=[
                                                                     GraphAPIInsightsFields.action_device_offline])]),
                                        action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                           GraphAPIInsightsFields.action_device],
                                        field_type=FieldType.ACTION_INSIGHT)
    mobile_content_views_value = Field(name='mobile_content_views_value',
                                       facebook_fields=[GraphAPIInsightsFields.action_values],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.mobile_app_content_views)]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                                       field_type=FieldType.ACTION_INSIGHT)
    website_content_views_value = Field(name='website_content_views_value',
                                        facebook_fields=[GraphAPIInsightsFields.action_values],
                                        mapper=ActionFieldMapper(field_filter=[
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.website_content_views)]),
                                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                                        field_type=FieldType.ACTION_INSIGHT)
    offline_content_views_value = Field(name='offline_content_views_value',
                                        facebook_fields=[GraphAPIInsightsFields.action_values],
                                        mapper=ActionFieldMapper(field_filter=[
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.content_views),
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                 operator=ActionFieldConditionOperatorEnum.IN,
                                                                 field_value=[
                                                                     GraphAPIInsightsFields.action_device_offline])]),
                                        action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                           GraphAPIInsightsFields.action_device],
                                        field_type=FieldType.ACTION_INSIGHT)
    content_views_cost = Field(name='content_views_cost',
                               facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.content_views)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_type],
                               field_type=FieldType.ACTION_INSIGHT)
    content_views_unique_cost = Field(name='content_views_unique_cost',
                                      facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.content_views)]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type],
                                      field_type=FieldType.ACTION_INSIGHT)
    content_views_unique_total = Field(name='content_views_unique_total',
                                       facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.content_views)]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                                       field_type=FieldType.ACTION_INSIGHT)
    # credit spends
    mobile_credit_spends_total = Field(name='mobile_credit_spends_total',
                                       facebook_fields=[GraphAPIInsightsFields.actions],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.mobile_app_credit_spends)]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                                       field_type=FieldType.ACTION_INSIGHT)
    desktop_credit_spends_total = Field(name='desktop_credit_spends_total',
                                        facebook_fields=[GraphAPIInsightsFields.actions],
                                        mapper=ActionFieldMapper(field_filter=[
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.website_content_views),
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.action_device_web)]),
                                        action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                           GraphAPIInsightsFields.action_device],
                                        field_type=FieldType.ACTION_INSIGHT)
    mobile_credit_spends_value = Field(name='mobile_credit_spends_value',
                                       facebook_fields=[GraphAPIInsightsFields.action_values],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.mobile_app_credit_spends)]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                                       field_type=FieldType.ACTION_INSIGHT)
    desktop_credit_spends_value = Field(name='desktop_credit_spends_value',
                                        facebook_fields=[GraphAPIInsightsFields.action_values],
                                        mapper=ActionFieldMapper(field_filter=[
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.website_content_views),
                                            ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.action_device_web)]),
                                        action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                           GraphAPIInsightsFields.action_device],
                                        field_type=FieldType.ACTION_INSIGHT)
    credit_spends_cost = Field(name='credit_spends_cost',
                               facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.credit_spends)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_type],
                               field_type=FieldType.ACTION_INSIGHT)
    mobile_credit_spends_unique_cost = Field(name='mobile_credit_spends_unique_cost',
                                             facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                             mapper=ActionFieldMapper(field_filter=[
                                                 ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.mobile_app_credit_spends)]),
                                             action_breakdowns=[GraphAPIInsightsFields.action_type],
                                             field_type=FieldType.ACTION_INSIGHT)
    mobile_credit_spends_unique_total = Field(name='mobile_credit_spends_unique_total',
                                              facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                              mapper=ActionFieldMapper(field_filter=[
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.mobile_app_credit_spends)]),
                                              action_breakdowns=[GraphAPIInsightsFields.action_type],
                                              field_type=FieldType.ACTION_INSIGHT)
    # custom events
    custom_events_total = Field(name='custom_events_total',
                                facebook_fields=[GraphAPIInsightsFields.actions],
                                mapper=ActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                       field_value=GraphAPIInsightsFields.custom_events)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                field_type=FieldType.ACTION_INSIGHT)
    custom_events_cost = Field(name='custom_events_cost',
                               facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                      field_value=GraphAPIInsightsFields.custom_events)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_type],
                               field_type=FieldType.ACTION_INSIGHT)
    # app engagements
    desktop_app_engagements_total = Field(name='desktop_app_engagements_total',
                                          facebook_fields=[GraphAPIInsightsFields.actions],
                                          mapper=ActionFieldMapper(field_filter=[
                                              ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                   field_value=GraphAPIInsightsFields.desktop_app_engagements)]),
                                          action_breakdowns=[GraphAPIInsightsFields.action_type],
                                          field_type=FieldType.ACTION_INSIGHT)
    desktop_app_engagements_cost = Field(name='desktop_app_engagements_cost',
                                         facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                         mapper=ActionFieldMapper(field_filter=[
                                             ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                  operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                  field_value=GraphAPIInsightsFields.desktop_app_engagements)]),
                                         action_breakdowns=[GraphAPIInsightsFields.action_type],
                                         field_type=FieldType.ACTION_INSIGHT)
    # desktop app story engagements
    desktop_app_story_engagements_total = Field(name='desktop_app_story_engagements_total',
                                                facebook_fields=[GraphAPIInsightsFields.actions],
                                                mapper=ActionFieldMapper(field_filter=[
                                                    ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                         operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                         field_value=GraphAPIInsightsFields.desktop_app_story_engagements)]),
                                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                field_type=FieldType.ACTION_INSIGHT)
    desktop_app_story_engagements_cost = Field(name='desktop_app_story_engagements_cost',
                                               facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                               mapper=ActionFieldMapper(field_filter=[
                                                   ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                        operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                        field_value=GraphAPIInsightsFields.desktop_app_story_engagements)]),
                                               action_breakdowns=[GraphAPIInsightsFields.action_type],
                                               field_type=FieldType.ACTION_INSIGHT)
    # desktop app uses
    desktop_app_uses_total = Field(name='desktop_app_uses_total',
                                   facebook_fields=[GraphAPIInsightsFields.actions],
                                   mapper=ActionFieldMapper(field_filter=[
                                       ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                            operator=ActionFieldConditionOperatorEnum.LIKE,
                                                            field_value=GraphAPIInsightsFields.desktop_app_uses)]),
                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                   field_type=FieldType.ACTION_INSIGHT)
    desktop_app_uses_cost = Field(name='desktop_app_uses_cost',
                                  facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                  mapper=ActionFieldMapper(
                                      field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                         operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                         field_value=GraphAPIInsightsFields.desktop_app_uses)]),
                                  action_breakdowns=[GraphAPIInsightsFields.action_type],
                                  field_type=FieldType.ACTION_INSIGHT)
    # game plays
    game_plays_total = Field(name='game_plays_total',
                             facebook_fields=[GraphAPIInsightsFields.actions],
                             mapper=ActionFieldMapper(
                                 field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.game_plays)]),
                             action_breakdowns=[GraphAPIInsightsFields.action_type],
                             field_type=FieldType.ACTION_INSIGHT)
    game_plays_cost = Field(name='game_plays_cost',
                            facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.game_plays)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    # landing page views
    landing_page_views_total = Field(name='landing_page_views_total',
                                     facebook_fields=[GraphAPIInsightsFields.actions],
                                     mapper=ActionFieldMapper(field_filter=[
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.landing_page_views)]),
                                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                                     field_type=FieldType.ACTION_INSIGHT)
    landing_page_views_unique = Field(name='landing_page_views_unique',
                                      facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.landing_page_views)]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type],
                                      field_type=FieldType.ACTION_INSIGHT)
    landing_page_views_cost = Field(name='landing_page_views_cost',
                                    facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.landing_page_views)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    landing_page_views_unique_cost = Field(name='landing_page_views_unique_cost',
                                           facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                           mapper=ActionFieldMapper(field_filter=[
                                               ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.landing_page_views)]),
                                           action_breakdowns=[GraphAPIInsightsFields.action_type],
                                           field_type=FieldType.ACTION_INSIGHT)
    # leads
    leads_total = Field(name='leads_total',
                        facebook_fields=[GraphAPIInsightsFields.actions],
                        mapper=ActionFieldMapper(
                            field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.leads)]),
                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                        field_type=FieldType.ACTION_INSIGHT)
    website_leads_total = Field(name='website_leads_total',
                                facebook_fields=[GraphAPIInsightsFields.actions],
                                mapper=ActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.website_leads)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                field_type=FieldType.ACTION_INSIGHT)
    offline_leads_total = Field(name='offline_leads_total',
                                facebook_fields=[GraphAPIInsightsFields.actions],
                                mapper=ActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.leads),
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.action_device_offline)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                   GraphAPIInsightsFields.action_device],
                                field_type=FieldType.ACTION_INSIGHT)
    on_facebook_leads_total = Field(name='on_facebook_leads_total',
                                    facebook_fields=[GraphAPIInsightsFields.actions],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.on_facebook_leads)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    leads_value = Field(name='leads_value',
                        facebook_fields=[GraphAPIInsightsFields.actions],
                        mapper=ActionFieldMapper(
                            field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.leads)]),
                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                        field_type=FieldType.ACTION_INSIGHT)
    website_leads_value = Field(name='website_leads_value',
                                facebook_fields=[GraphAPIInsightsFields.action_values],
                                mapper=ActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.website_leads)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                field_type=FieldType.ACTION_INSIGHT)
    offline_leads_value = Field(name='offline_leads_value',
                                facebook_fields=[GraphAPIInsightsFields.action_values],
                                mapper=ActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.leads),
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.action_device_offline)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                   GraphAPIInsightsFields.action_device],
                                field_type=FieldType.ACTION_INSIGHT)
    on_facebook_leads_value = Field(name='on_facebook_leads_value',
                                    facebook_fields=[GraphAPIInsightsFields.action_values],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.on_facebook_leads)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    leads_cost = Field(name='leads_cost',
                       facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                       mapper=ActionFieldMapper(
                           field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.leads)]),
                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                       field_type=FieldType.ACTION_INSIGHT)
    # on-facebook workflow completions
    on_facebook_workflow_completions_total = Field(name='on_facebook_workflow_completions_total',
                                                   facebook_fields=[GraphAPIInsightsFields.actions],
                                                   mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                       field_name=GraphAPIInsightsFields.action_type,
                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                       field_value=GraphAPIInsightsFields.on_facebook_workflow_completions)]),
                                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                   field_type=FieldType.ACTION_INSIGHT)
    on_facebook_workflow_completions_value = Field(name='on_facebook_workflow_completions_value',
                                                   facebook_fields=[GraphAPIInsightsFields.action_values],
                                                   mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                       field_name=GraphAPIInsightsFields.action_type,
                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                       field_value=GraphAPIInsightsFields.on_facebook_workflow_completions)]),
                                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                   field_type=FieldType.ACTION_INSIGHT)
    on_facebook_workflow_completions_cost = Field(name='on_facebook_workflow_completions_cost',
                                                  facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                                  mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                      field_name=GraphAPIInsightsFields.action_type,
                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                      field_value=GraphAPIInsightsFields.on_facebook_workflow_completions)]),
                                                  action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                  field_type=FieldType.ACTION_INSIGHT)
    # other offline conversions
    other_offline_conversions_total = Field(name='other_offline_conversions_total',
                                            facebook_fields=[GraphAPIInsightsFields.actions],
                                            mapper=ActionFieldMapper(field_filter=[
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.on_facebook_workflow_completions)]),
                                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                                            field_type=FieldType.ACTION_INSIGHT)
    other_offline_conversions_value = Field(name='other_offline_conversions_value',
                                            facebook_fields=[GraphAPIInsightsFields.action_values],
                                            mapper=ActionFieldMapper(field_filter=[
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.on_facebook_workflow_completions)]),
                                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                                            field_type=FieldType.ACTION_INSIGHT)
    other_offline_conversions_cost = Field(name='other_offline_conversions_cost',
                                           facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                           mapper=ActionFieldMapper(field_filter=[
                                               ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.on_facebook_workflow_completions)]),
                                           action_breakdowns=[GraphAPIInsightsFields.action_type],
                                           field_type=FieldType.ACTION_INSIGHT)
    # purchases ROAS
    mobile_app_purchase_roas = Field(name='mobile_app_purchase_roas',
                                     facebook_fields=[GraphAPIInsightsFields.actions],
                                     mapper=ActionFieldMapper(field_filter=[
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.mobile_app_purchase_roas)]),
                                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                                     field_type=FieldType.ACTION_INSIGHT)
    #  purchases
    purchases_total = Field(name='purchases_total',
                            facebook_fields=[GraphAPIInsightsFields.actions],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.purchases)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    mobile_app_purchases_total = Field(name='mobile_app_purchases_total',
                                       facebook_fields=[GraphAPIInsightsFields.actions],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.mobile_app_purchases)]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                                       field_type=FieldType.ACTION_INSIGHT)
    website_purchases_total = Field(name='website_purchases_total',
                                    facebook_fields=[GraphAPIInsightsFields.actions],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.website_purchases)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    offline_purchases_total = Field(name='offline_purchases_total',
                                    facebook_fields=[GraphAPIInsightsFields.actions],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.purchases),
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.action_device_offline)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                       GraphAPIInsightsFields.action_device],
                                    field_type=FieldType.ACTION_INSIGHT)
    purchases_unique = Field(name='purchases_unique',
                             facebook_fields=[GraphAPIInsightsFields.unique_actions],
                             mapper=ActionFieldMapper(
                                 field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.purchases)]),
                             action_breakdowns=[GraphAPIInsightsFields.action_type],
                             field_type=FieldType.ACTION_INSIGHT)
    purchases_value = Field(name='purchases_value',
                            facebook_fields=[GraphAPIInsightsFields.action_values],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                   field_value_map=None)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    mobile_app_purchases_value = Field(name='mobile_app_purchases_value',
                                       facebook_fields=[GraphAPIInsightsFields.action_values],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.mobile_app_purchases)]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                                       field_type=FieldType.ACTION_INSIGHT)
    website_purchases_value = Field(name='website_purchases_value',
                                    facebook_fields=[GraphAPIInsightsFields.action_values],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.website_purchases)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    offline_purchases_value = Field(name='offline_purchases_value',
                                    facebook_fields=[GraphAPIInsightsFields.action_values],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.purchases),
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.action_device_offline)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                       GraphAPIInsightsFields.action_device],
                                    field_type=FieldType.ACTION_INSIGHT)
    purchases_cost = Field(name='purchases_cost',
                           facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                           mapper=ActionFieldMapper(
                               field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                  operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                  field_value=GraphAPIInsightsFields.purchases)]),
                           action_breakdowns=[GraphAPIInsightsFields.action_type],
                           field_type=FieldType.ACTION_INSIGHT)
    purchases_unique_cost = Field(name='purchases_unique_cost',
                                  facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                  mapper=ActionFieldMapper(
                                      field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                         operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                         field_value=GraphAPIInsightsFields.purchases)]),
                                  action_breakdowns=[GraphAPIInsightsFields.action_type],
                                  field_type=FieldType.ACTION_INSIGHT)
    # registrations completed
    registrations_completed_total = Field(name='registrations_completed_total',
                                          facebook_fields=[GraphAPIInsightsFields.actions],
                                          mapper=ActionFieldMapper(field_filter=[
                                              ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.registrations_completed)]),
                                          action_breakdowns=[GraphAPIInsightsFields.action_type],
                                          field_type=FieldType.ACTION_INSIGHT)
    mobile_app_registrations_completed_total = Field(name='mobile_app_registrations_completed_total',
                                                     facebook_fields=[GraphAPIInsightsFields.actions],
                                                     mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                         field_name=GraphAPIInsightsFields.action_type,
                                                         operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                         field_value=GraphAPIInsightsFields.mobile_app_registrations_completed)]),
                                                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                     field_type=FieldType.ACTION_INSIGHT)
    website_registrations_completed_total = Field(name='website_registrations_completed_total',
                                                  facebook_fields=[GraphAPIInsightsFields.actions],
                                                  mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                      field_name=GraphAPIInsightsFields.action_type,
                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                      field_value=GraphAPIInsightsFields.website_registrations_completed)]),
                                                  action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                  field_type=FieldType.ACTION_INSIGHT)
    offline_registrations_completed_total = Field(name='offline_registrations_completed_total',
                                                  facebook_fields=[GraphAPIInsightsFields.actions],
                                                  mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                      field_name=GraphAPIInsightsFields.action_type,
                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                      field_value=GraphAPIInsightsFields.registrations_completed),
                                                      ActionFieldCondition(
                                                          field_name=GraphAPIInsightsFields.action_device,
                                                          operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                          field_value=GraphAPIInsightsFields.action_device_offline)]),
                                                  action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                                     GraphAPIInsightsFields.action_device],
                                                  field_type=FieldType.ACTION_INSIGHT)
    registrations_completed_unique = Field(name='registrations_completed_unique',
                                           facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                           mapper=ActionFieldMapper(field_filter=[
                                               ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.registrations_completed)]),
                                           action_breakdowns=[GraphAPIInsightsFields.action_type],
                                           field_type=FieldType.ACTION_INSIGHT)
    registrations_completed_value = Field(name='registrations_completed_value',
                                          facebook_fields=[GraphAPIInsightsFields.action_values],
                                          mapper=ActionFieldMapper(field_filter=[
                                              ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.registrations_completed)]),
                                          action_breakdowns=[GraphAPIInsightsFields.action_type],
                                          field_type=FieldType.ACTION_INSIGHT)
    mobile_app_registrations_completed_value = Field(name='mobile_app_registrations_completed_value',
                                                     facebook_fields=[GraphAPIInsightsFields.action_values],
                                                     mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                         field_name=GraphAPIInsightsFields.action_type,
                                                         operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                         field_value=GraphAPIInsightsFields.mobile_app_registrations_completed)]),
                                                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                     field_type=FieldType.ACTION_INSIGHT)
    website_registrations_completed_value = Field(name='website_registrations_completed_value',
                                                  facebook_fields=[GraphAPIInsightsFields.action_values],
                                                  mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                      field_name=GraphAPIInsightsFields.action_type,
                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                      field_value=GraphAPIInsightsFields.website_registrations_completed)]),
                                                  action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                  field_type=FieldType.ACTION_INSIGHT)
    offline_registrations_completed_value = Field(name='offline_registrations_completed_value',
                                                  facebook_fields=[GraphAPIInsightsFields.action_values],
                                                  mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                      field_name=GraphAPIInsightsFields.action_type,
                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                      field_value=GraphAPIInsightsFields.registrations_completed),
                                                      ActionFieldCondition(
                                                          field_name=GraphAPIInsightsFields.action_device,
                                                          operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                          field_value=GraphAPIInsightsFields.action_device_offline)]),
                                                  action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                                     GraphAPIInsightsFields.action_device],
                                                  field_type=FieldType.ACTION_INSIGHT)
    registrations_completed_cost = Field(name='registrations_completed_cost',
                                         facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                         mapper=ActionFieldMapper(field_filter=[
                                             ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                  operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                  field_value=GraphAPIInsightsFields.registrations_completed)]),
                                         action_breakdowns=[GraphAPIInsightsFields.action_type],
                                         field_type=FieldType.ACTION_INSIGHT)
    registrations_completed_unique_cost = Field(name='registrations_completed_unique_cost',
                                                facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                                mapper=ActionFieldMapper(field_filter=[
                                                    ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                         operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                         field_value=GraphAPIInsightsFields.registrations_completed)]),
                                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                field_type=FieldType.ACTION_INSIGHT)
    # searches
    searches_total = Field(name='searches_total',
                           facebook_fields=[GraphAPIInsightsFields.actions],
                           mapper=ActionFieldMapper(
                               field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                  operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                  field_value=GraphAPIInsightsFields.searches)]),
                           action_breakdowns=[GraphAPIInsightsFields.action_type],
                           field_type=FieldType.ACTION_INSIGHT)
    mobile_app_searches_total = Field(name='mobile_app_searches_total',
                                      facebook_fields=[GraphAPIInsightsFields.actions],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.mobile_app_searches)]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type],
                                      field_type=FieldType.ACTION_INSIGHT)
    website_searches_total = Field(name='website_searches_total',
                                   facebook_fields=[GraphAPIInsightsFields.actions],
                                   mapper=ActionFieldMapper(field_filter=[
                                       ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.website_searches)]),
                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                   field_type=FieldType.ACTION_INSIGHT)
    offline_searches_total = Field(name='offline_searches_total',
                                   facebook_fields=[GraphAPIInsightsFields.actions],
                                   mapper=ActionFieldMapper(field_filter=[
                                       ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.searches),
                                       ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.action_device_offline)]),
                                   action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                      GraphAPIInsightsFields.action_device],
                                   field_type=FieldType.ACTION_INSIGHT)
    searches_unique = Field(name='searches_unique',
                            facebook_fields=[GraphAPIInsightsFields.unique_actions],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.searches)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    searches_value = Field(name='searches_value',
                           facebook_fields=[GraphAPIInsightsFields.action_values],
                           mapper=ActionFieldMapper(
                               field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                  operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                  field_value=GraphAPIInsightsFields.searches)]),
                           action_breakdowns=[GraphAPIInsightsFields.action_type],
                           field_type=FieldType.ACTION_INSIGHT)
    mobile_app_searches_value = Field(name='mobile_app_searches_value',
                                      facebook_fields=[GraphAPIInsightsFields.action_values],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.mobile_app_searches)]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type],
                                      field_type=FieldType.ACTION_INSIGHT)
    website_searches_value = Field(name='website_searches_value',
                                   facebook_fields=[GraphAPIInsightsFields.action_values],
                                   mapper=ActionFieldMapper(field_filter=[
                                       ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.website_searches)]),
                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                   field_type=FieldType.ACTION_INSIGHT)
    offline_searches_value = Field(name='offline_searches_value',
                                   facebook_fields=[GraphAPIInsightsFields.action_values],
                                   mapper=ActionFieldMapper(field_filter=[
                                       ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.searches),
                                       ActionFieldCondition(field_name=GraphAPIInsightsFields.action_device,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.action_device_offline)]),
                                   action_breakdowns=[GraphAPIInsightsFields.action_type,
                                                      GraphAPIInsightsFields.action_device],
                                   field_type=FieldType.ACTION_INSIGHT)
    searches_cost = Field(name='searches_cost',
                          facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                          mapper=ActionFieldMapper(
                              field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.searches)]),
                          action_breakdowns=[GraphAPIInsightsFields.action_type],
                          field_type=FieldType.ACTION_INSIGHT)
    searches_unique_cost = Field(name='searches_unique_cost',
                                 facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                 mapper=ActionFieldMapper(
                                     field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                        operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                        field_value=GraphAPIInsightsFields.searches)]),
                                 action_breakdowns=[GraphAPIInsightsFields.action_type],
                                 field_type=FieldType.ACTION_INSIGHT)
    #  subscriptions
    subscriptions_total = Field(name='subscriptions_total',
                                facebook_fields=[GraphAPIInsightsFields.actions],
                                mapper=ActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.subscriptions)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                field_type=FieldType.ACTION_INSIGHT)
    subscriptions_value = Field(name='subscriptions_value',
                                facebook_fields=[GraphAPIInsightsFields.action_values],
                                mapper=ActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.subscriptions)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                field_type=FieldType.ACTION_INSIGHT)
    subscriptions_cost = Field(name='subscriptions_cost',
                               facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.subscriptions)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_type],
                               field_type=FieldType.ACTION_INSIGHT)
    # tutorials completed
    tutorials_completed_total = Field(name='tutorials_completed_total',
                                      facebook_fields=[GraphAPIInsightsFields.actions],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.tutorials_completed)]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type],
                                      field_type=FieldType.ACTION_INSIGHT)
    mobile_app_tutorials_completed_total = Field(name='mobile_app_tutorials_completed_total',
                                                 facebook_fields=[GraphAPIInsightsFields.actions],
                                                 mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                     field_name=GraphAPIInsightsFields.action_type,
                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                     field_value=GraphAPIInsightsFields.mobile_app_tutorials_completed)]),
                                                 action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                 field_type=FieldType.ACTION_INSIGHT)
    tutorials_completed_unique = Field(name='tutorials_completed_unique',
                                       facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.tutorials_completed)]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                                       field_type=FieldType.ACTION_INSIGHT)
    tutorials_completed_value = Field(name='tutorials_completed_value',
                                      facebook_fields=[GraphAPIInsightsFields.action_values],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.tutorials_completed)]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type],
                                      field_type=FieldType.ACTION_INSIGHT)
    mobile_app_tutorials_completed_value = Field(name='mobile_app_tutorials_completed_value',
                                                 facebook_fields=[GraphAPIInsightsFields.action_values],
                                                 mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                     field_name=GraphAPIInsightsFields.action_type,
                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                     field_value=GraphAPIInsightsFields.mobile_app_tutorials_completed)]),
                                                 action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                 field_type=FieldType.ACTION_INSIGHT)
    tutorials_completed_cost = Field(name='tutorials_completed_cost',
                                     facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                     mapper=ActionFieldMapper(field_filter=[
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.tutorials_completed)]),
                                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                                     field_type=FieldType.ACTION_INSIGHT)
    tutorials_completed_unique_cost = Field(name='tutorials_completed_unique_cost',
                                            facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                            mapper=ActionFieldMapper(field_filter=[
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.tutorials_completed)]),
                                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                                            field_type=FieldType.ACTION_INSIGHT)
