from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import ActionFieldCondition, \
    ActionFieldConditionOperatorEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldMapper import ActionFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.CostPerActionFieldMapper import CostPerActionFieldMapper
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType


class FieldsCustomMetadata:
    conversions = Field(name="conversions",
                        facebook_fields=[GraphAPIInsightsFields.actions],
                        mapper=ActionFieldMapper(
                            field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.LIKE,
                                                               field_value=GraphAPIInsightsFields.conversions)]),
                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                        field_type=FieldType.ACTION_INSIGHT)
    cost_per_conversion = Field(name="cost_per_conversion",
                                facebook_fields=[GraphAPIInsightsFields.actions],
                                mapper=CostPerActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                       field_value=GraphAPIInsightsFields.conversions)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                field_type=FieldType.ACTION_INSIGHT)
    messaging_conversation_started_7d = Field(name="messaging_conversation_started_7d",
                                              facebook_fields=[GraphAPIInsightsFields.actions],
                                              mapper=ActionFieldMapper(field_filter=[
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.messaging_conversation_started_7d)]),
                                              action_breakdowns=[GraphAPIInsightsFields.action_type],
                                              field_type=FieldType.ACTION_INSIGHT)
    click_to_play_video_25p = Field(name="click_to_play_video_25p",
                                    facebook_fields=[GraphAPIInsightsFields.video_p25_watched_actions],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.video_view),
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_video_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.video_click_to_play)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    autoplay_video_25p = Field(name="autoplay_video_25p",
                               facebook_fields=[GraphAPIInsightsFields.video_p25_watched_actions],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.video_view),
                                                 ActionFieldCondition(
                                                     field_name=GraphAPIInsightsFields.action_video_type,
                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                     field_value=GraphAPIInsightsFields.video_auto_play)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                               field_type=FieldType.ACTION_INSIGHT)
    click_to_play_video_50p = Field(name="click_to_play_video_50p",
                                    facebook_fields=[GraphAPIInsightsFields.video_p50_watched_actions],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.video_view),
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_video_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.video_click_to_play)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    autoplay_video_50p = Field(name="autoplay_video_50p",
                               facebook_fields=[GraphAPIInsightsFields.video_p50_watched_actions],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.video_view),
                                                 ActionFieldCondition(
                                                     field_name=GraphAPIInsightsFields.action_video_type,
                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                     field_value=GraphAPIInsightsFields.video_auto_play)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                               field_type=FieldType.ACTION_INSIGHT)
    click_to_play_video_75p = Field(name="click_to_play_video_75p",
                                    facebook_fields=[GraphAPIInsightsFields.video_p75_watched_actions],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.video_view),
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_video_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.video_click_to_play)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    autoplay_video_75p = Field(name="autoplay_video_75p",
                               facebook_fields=[GraphAPIInsightsFields.video_p75_watched_actions],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.video_view),
                                                 ActionFieldCondition(
                                                     field_name=GraphAPIInsightsFields.action_video_type,
                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                     field_value=GraphAPIInsightsFields.video_auto_play)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                               field_type=FieldType.ACTION_INSIGHT)
    click_to_play_video_95p = Field(name="click_to_play_video_95p",
                                    facebook_fields=[GraphAPIInsightsFields.video_p95_watched_actions],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.video_view),
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_video_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.video_click_to_play)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    autoplay_video_95p = Field(name="autoplay_video_95p",
                               facebook_fields=[GraphAPIInsightsFields.video_p95_watched_actions],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.video_view),
                                                 ActionFieldCondition(
                                                     field_name=GraphAPIInsightsFields.action_video_type,
                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                     field_value=GraphAPIInsightsFields.video_auto_play)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                               field_type=FieldType.ACTION_INSIGHT)
    click_to_play_video_100p = Field(name="click_to_play_video_100p",
                                     facebook_fields=[GraphAPIInsightsFields.video_p100_watched_actions],
                                     mapper=ActionFieldMapper(field_filter=[
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.video_view),
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_video_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.video_click_to_play)]),
                                     action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                                     field_type=FieldType.ACTION_INSIGHT)
    autoplay_video_100p = Field(name="autoplay_video_100p",
                                facebook_fields=[GraphAPIInsightsFields.video_p100_watched_actions],
                                mapper=ActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.video_view),
                                                  ActionFieldCondition(
                                                      field_name=GraphAPIInsightsFields.action_video_type,
                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                      field_value=GraphAPIInsightsFields.video_auto_play)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                                field_type=FieldType.ACTION_INSIGHT)
    post_likes = Field(name="post_likes",
                       facebook_fields=[GraphAPIInsightsFields.actions],
                       mapper=ActionFieldMapper(
                           field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.post_reaction),
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_reaction,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.post_likes)]),
                       action_breakdowns=[GraphAPIInsightsFields.action_type,
                                          GraphAPIInsightsFields.action_reaction],
                       field_type=FieldType.ACTION_INSIGHT)
