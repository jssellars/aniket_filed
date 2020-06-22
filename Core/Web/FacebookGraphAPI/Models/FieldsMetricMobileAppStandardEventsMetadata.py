from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import ActionFieldCondition, \
    ActionFieldConditionOperatorEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldMapper import ActionFieldMapper
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType


class FieldsMetricMobileAppStandardEventsMetadata:
    mobile_app_achievements_unlocked_total = Field(name='mobile_app_achievements_unlocked_total',
                                                   facebook_fields=[GraphAPIInsightsFields.actions],
                                                   mapper=ActionFieldMapper(field_filter=[
                                                       ActionFieldCondition(
                                                           field_name=GraphAPIInsightsFields.action_type,
                                                           operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                           field_value=GraphAPIInsightsFields.mobile_achievement_unlocked)]),
                                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                   field_type=FieldType.ACTION_INSIGHT)

    # app_custom_event.fb_mobile_achievement_unlocked
    # app_custom_event.fb_mobile_activate_app
    # app_custom_event.fb_mobile_add_payment_info
    # app_custom_event.fb_mobile_add_to_cart
    # app_custom_event.fb_mobile_add_to_wishlist
    # app_custom_event.fb_mobile_complete_registration
    # app_custom_event.fb_mobile_content_view
    # app_custom_event.fb_mobile_initiated_checkout
    # app_custom_event.fb_mobile_level_achieved
    # app_custom_event.fb_mobile_purchase
    # app_custom_event.fb_mobile_rate
    # app_custom_event.fb_mobile_search
    # app_custom_event.fb_mobile_spent_credits
    # app_custom_event.fb_mobile_tutorial_completion
    # app_custom_event.other
    # mobile_app_install
    # mobile_app_retention
    # mobile_app_roas
