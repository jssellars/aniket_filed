from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import ActionFieldCondition, \
    ActionFieldConditionOperatorEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldMapper import ActionFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.OneToOneFieldMapper import OneToOneFieldMapper
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType


class FieldsMetricEngagementMetadata:
    page_engagement = Field(name="page_engagement",
                            facebook_fields=[GraphAPIInsightsFields.actions],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.page_engagement)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    page_likes = Field(name="page_likes",
                       facebook_fields=[GraphAPIInsightsFields.actions],
                       mapper=ActionFieldMapper(
                           field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.page_like)]),
                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                       field_type=FieldType.ACTION_INSIGHT)
    post_comments = Field(name="post_comments",
                          facebook_fields=[GraphAPIInsightsFields.actions],
                          mapper=ActionFieldMapper(
                              field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.post_comment)]),
                          action_breakdowns=[GraphAPIInsightsFields.action_type],
                          field_type=FieldType.ACTION_INSIGHT)
    post_engagement = Field(name="post_engagement",
                            facebook_fields=[GraphAPIInsightsFields.actions],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.post_engagement)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    post_reactions = Field(name="post_reactions",
                           facebook_fields=[GraphAPIInsightsFields.actions],
                           mapper=ActionFieldMapper(
                               field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                  operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                  field_value=GraphAPIInsightsFields.post_reaction)]),
                           action_breakdowns=[GraphAPIInsightsFields.action_type],
                           field_type=FieldType.ACTION_INSIGHT)
    post_saves = Field(name="post_saves",
                       facebook_fields=[GraphAPIInsightsFields.actions],
                       mapper=ActionFieldMapper(
                           field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.post_saves)]),
                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                       field_type=FieldType.ACTION_INSIGHT)
    post_shares = Field(name="post_shares",
                        facebook_fields=[GraphAPIInsightsFields.actions],
                        mapper=ActionFieldMapper(
                            field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.post_shares)]),
                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                        field_type=FieldType.ACTION_INSIGHT)

    photo_views = Field(name="photo_views",
                        facebook_fields=[GraphAPIInsightsFields.actions],
                        mapper=ActionFieldMapper(
                            field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.photo_views)]),
                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                        field_type=FieldType.ACTION_INSIGHT)

    event_responses = Field(name="event_responses",
                            facebook_fields=[GraphAPIInsightsFields.actions],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.event_responses)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    checkins = Field(name="checkins",
                     facebook_fields=[GraphAPIInsightsFields.actions],
                     mapper=ActionFieldMapper(
                         field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.checkins)]),
                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                     field_type=FieldType.ACTION_INSIGHT)
    inview_impressions_100p = Field(name="inview_impressions_100p",
                                    facebook_fields=[GraphAPIInsightsFields.full_view_impressions],
                                    mapper=OneToOneFieldMapper(),
                                    field_type=FieldType.INSIGHT)
    inview_reach_100p = Field(name="inview_reach_100p",
                              facebook_fields=[GraphAPIInsightsFields.full_view_reach],
                              mapper=OneToOneFieldMapper(),
                              field_type=FieldType.INSIGHT)
    cost_per_page_engagement = Field(name="cost_per_page_engagement",
                                     facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                     mapper=ActionFieldMapper(field_filter=[
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.page_engagement)]),
                                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                                     field_type=FieldType.ACTION_INSIGHT)
    cost_per_page_like = Field(name="cost_per_page_like",
                               facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.page_like)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_type],
                               field_type=FieldType.ACTION_INSIGHT)
    cost_per_post_engagement = Field(name="cost_per_post_engagement",
                                     facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                     mapper=ActionFieldMapper(field_filter=[
                                         ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.post_engagement)]),
                                     action_breakdowns=[GraphAPIInsightsFields.action_type],
                                     field_type=FieldType.ACTION_INSIGHT)
    cost_per_event_response = Field(name="cost_per_event_response",
                                    facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.event_responses)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    new_messaging_connections = Field(name="new_messaging_connections",
                                      facebook_fields=[GraphAPIInsightsFields.actions],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.new_messaging_connections)]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type],
                                      field_type=FieldType.ACTION_INSIGHT)
    messaging_first_reply = Field(name="messaging_first_reply",
                                  facebook_fields=[GraphAPIInsightsFields.actions],
                                  mapper=ActionFieldMapper(field_filter=[
                                      ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                           operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                           field_value=GraphAPIInsightsFields.new_messaging_connections)]),
                                  action_breakdowns=[GraphAPIInsightsFields.action_type],
                                  field_type=FieldType.ACTION_INSIGHT)
    messaging_conversations_started = Field(name="messaging_conversations_started",
                                            facebook_fields=[GraphAPIInsightsFields.actions],
                                            mapper=ActionFieldMapper(field_filter=[
                                                ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                     operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                     field_value=GraphAPIInsightsFields.messaging_conversation_started_7d)]),
                                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                                            field_type=FieldType.ACTION_INSIGHT)
    blocked_messaging_connections = Field(name="blocked_messaging_connections",
                                          facebook_fields=[GraphAPIInsightsFields.actions],
                                          mapper=ActionFieldMapper(field_filter=[
                                              ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.blocked_messaging_connections)]),
                                          action_breakdowns=[GraphAPIInsightsFields.action_type],
                                          field_type=FieldType.ACTION_INSIGHT)
    cost_per_new_messaging_connection = Field(name="cost_per_new_messaging_connection",
                                              facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                              mapper=ActionFieldMapper(field_filter=[
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.new_messaging_connections)]),
                                              action_breakdowns=[GraphAPIInsightsFields.action_type],
                                              field_type=FieldType.ACTION_INSIGHT)
    cost_per_messaging_first_reply = Field(name="cost_per_messaging_first_reply",
                                           facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                           mapper=ActionFieldMapper(field_filter=[
                                               ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.new_messaging_connections)]),
                                           action_breakdowns=[GraphAPIInsightsFields.action_type],
                                           field_type=FieldType.ACTION_INSIGHT)
    cost_per_blocked_messaging_connections = Field(name="cost_per_blocked_messaging_connections",
                                                   facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                                   mapper=ActionFieldMapper(field_filter=[
                                                       ActionFieldCondition(
                                                           field_name=GraphAPIInsightsFields.action_type,
                                                           operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                           field_value=GraphAPIInsightsFields.blocked_messaging_connections)]),
                                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                   field_type=FieldType.ACTION_INSIGHT)
    cost_per_messaging_conversation_started = Field(name="cost_per_messaging_conversation_started",
                                                    facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                                    mapper=ActionFieldMapper(field_filter=[
                                                        ActionFieldCondition(
                                                            field_name=GraphAPIInsightsFields.action_type,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.messaging_conversation_started_7d)]),
                                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                    field_type=FieldType.ACTION_INSIGHT)
    continuous_video_plays_2s_unique = Field(name="continuous_video_plays_2s_unique",
                                             facebook_fields=[GraphAPIInsightsFields.unique_actions],
                                             mapper=ActionFieldMapper(field_filter=[
                                                 ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.video_view)]),
                                             action_breakdowns=[GraphAPIInsightsFields.action_type],
                                             field_type=FieldType.ACTION_INSIGHT)

    continuous_video_plays_2s = Field(name="continuous_video_plays_2s_unique",
                                      facebook_fields=[GraphAPIInsightsFields.actions],
                                      mapper=ActionFieldMapper(field_filter=[
                                          ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.video_view)]),
                                      action_breakdowns=[GraphAPIInsightsFields.action_type],
                                      field_type=FieldType.ACTION_INSIGHT)
    video_plays_3s = Field(name="video_plays_3s",
                           facebook_fields=[GraphAPIInsightsFields.actions],
                           mapper=ActionFieldMapper(
                               field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                  operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                  field_value=GraphAPIInsightsFields.video_view)]),
                           action_breakdowns=[GraphAPIInsightsFields.action_type],
                           field_type=FieldType.ACTION_INSIGHT)
    thru_plays = Field(name="thru_plays",
                       facebook_fields=[GraphAPIInsightsFields.thru_plays],
                       mapper=ActionFieldMapper(
                           field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                              operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                              field_value=GraphAPIInsightsFields.video_view)]),
                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                       field_type=FieldType.ACTION_INSIGHT)

    video_plays_25p = Field(name="video_plays_25p",
                            facebook_fields=[GraphAPIInsightsFields.video_p25_watched_actions],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.video_view)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    video_plays_50p = Field(name="video_plays_50p",
                            facebook_fields=[GraphAPIInsightsFields.video_p50_watched_actions],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.video_view)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    video_plays_75p = Field(name="video_plays_75p",
                            facebook_fields=[GraphAPIInsightsFields.video_p75_watched_actions],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.video_view)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    video_plays_95p = Field(name="video_plays_95p",
                            facebook_fields=[GraphAPIInsightsFields.video_p95_watched_actions],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.video_view)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)

    video_plays_100p = Field(name="video_plays_100p",
                             facebook_fields=[GraphAPIInsightsFields.video_p100_watched_actions],
                             mapper=ActionFieldMapper(
                                 field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.video_view)]),
                             action_breakdowns=[GraphAPIInsightsFields.action_type],
                             field_type=FieldType.ACTION_INSIGHT)
    video_average_play_time = Field(name="video_average_play_time",
                                    facebook_fields=[GraphAPIInsightsFields.video_avg_time_watched_actions],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.video_view)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    video_plays = Field(name="video_plays",
                        facebook_fields=[GraphAPIInsightsFields.video_play_actions],
                        mapper=ActionFieldMapper(
                            field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.video_view)]),
                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                        field_type=FieldType.ACTION_INSIGHT)
    instant_experience_view_time = Field(name="instant_experience_view_time",
                                         facebook_fields=[GraphAPIInsightsFields.canvas_avg_view_time],
                                         mapper=OneToOneFieldMapper(),
                                         field_type=FieldType.INSIGHT)
    instant_experience_view_percentage = Field(name="instant_experience_view_percentage",
                                               facebook_fields=[GraphAPIInsightsFields.canvas_avg_view_percent],
                                               mapper=OneToOneFieldMapper(),
                                               field_type=FieldType.INSIGHT)
    cost_per_continuous_video_play_2s = Field(name="cost_per_continuous_video_play_2s",
                                              facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                              mapper=ActionFieldMapper(field_filter=[
                                                  ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.video_view)]),
                                              action_breakdowns=[GraphAPIInsightsFields.action_type],
                                              field_type=FieldType.ACTION_INSIGHT)
    cost_per_video_view = Field(name="cost_per_video_view",
                                facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                mapper=ActionFieldMapper(field_filter=[
                                    ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                         operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                         field_value=GraphAPIInsightsFields.video_view)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                field_type=FieldType.ACTION_INSIGHT)
    cost_per_thru_play = Field(name="cost_per_thru_play",
                               facebook_fields=[GraphAPIInsightsFields.cost_per_thruplay],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.video_view)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_type],
                               field_type=FieldType.ACTION_INSIGHT)
    link_clicks = Field(name="link_clicks",
                        facebook_fields=[GraphAPIInsightsFields.actions],
                        mapper=ActionFieldMapper(
                            field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                               operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                               field_value=GraphAPIInsightsFields.link_click)]),
                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                        field_type=FieldType.ACTION_INSIGHT)
    unique_link_clicks = Field(name="unique_link_clicks",
                               facebook_fields=[GraphAPIInsightsFields.unique_actions],
                               mapper=ActionFieldMapper(
                                   field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.link_click)]),
                               action_breakdowns=[GraphAPIInsightsFields.action_type],
                               field_type=FieldType.ACTION_INSIGHT)
    inline_link_click = Field(name=GraphAPIInsightsFields.inline_link_click,
                              facebook_fields=[GraphAPIInsightsFields.inline_link_click],
                              mapper=OneToOneFieldMapper(),
                              field_type=FieldType.INSIGHT)
    inline_link_click_ctr = Field(name=GraphAPIInsightsFields.inline_link_click_ctr,
                                  facebook_fields=[GraphAPIInsightsFields.inline_link_click_ctr],
                                  mapper=OneToOneFieldMapper(),
                                  field_type=FieldType.INSIGHT)
    unique_inline_link_click = Field(name=GraphAPIInsightsFields.unique_inline_link_click,
                                     facebook_fields=[GraphAPIInsightsFields.unique_inline_link_click],
                                     mapper=OneToOneFieldMapper(),
                                     field_type=FieldType.INSIGHT)
    unique_inline_link_click_ctr = Field(name=GraphAPIInsightsFields.unique_inline_link_click_ctr,
                                         facebook_fields=[GraphAPIInsightsFields.unique_inline_link_click_ctr],
                                         mapper=OneToOneFieldMapper(),
                                         field_type=FieldType.INSIGHT)
    cost_per_inline_link_click = Field(name=GraphAPIInsightsFields.cost_per_inline_link_click,
                                       facebook_fields=[GraphAPIInsightsFields.cost_per_inline_link_click],
                                       mapper=OneToOneFieldMapper(),
                                       field_type=FieldType.INSIGHT)
    cost_per_unique_inline_link_click = Field(name=GraphAPIInsightsFields.cost_per_unique_inline_link_click,
                                              facebook_fields=[
                                                  GraphAPIInsightsFields.cost_per_unique_inline_link_click],
                                              mapper=OneToOneFieldMapper(),
                                              field_type=FieldType.INSIGHT)
    inline_post_engagement = Field(name=GraphAPIInsightsFields.inline_post_engagement,
                                   facebook_fields=[GraphAPIInsightsFields.inline_post_engagement],
                                   mapper=OneToOneFieldMapper(),
                                   field_type=FieldType.INSIGHT)
    cost_per_inline_post_engagement = Field(name=GraphAPIInsightsFields.cost_per_inline_post_engagement,
                                            facebook_fields=[GraphAPIInsightsFields.cost_per_inline_post_engagement],
                                            mapper=OneToOneFieldMapper(),
                                            field_type=FieldType.INSIGHT)
    outbound_clicks = Field(name="outbound_clicks",
                            facebook_fields=[GraphAPIInsightsFields.outbound_clicks],
                            mapper=ActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                   field_value=GraphAPIInsightsFields.outbound_click)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT)
    unique_outbound_clicks = Field(name="unique_outbound_clicks",
                                   facebook_fields=[GraphAPIInsightsFields.outbound_clicks],
                                   mapper=ActionFieldMapper(field_filter=[
                                       ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                            operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                            field_value=GraphAPIInsightsFields.outbound_click)]),
                                   action_breakdowns=[GraphAPIInsightsFields.action_type],
                                   field_type=FieldType.ACTION_INSIGHT)
    link_click_through_rate = Field(name="link_click_through_rate",
                                    facebook_fields=[GraphAPIInsightsFields.website_ctr],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.link_click)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    unique_link_click_through_rate = Field(name="unique_link_click_through_rate",
                                           facebook_fields=[GraphAPIInsightsFields.unique_link_clicks_ctr],
                                           mapper=OneToOneFieldMapper(),
                                           field_type=FieldType.INSIGHT)
    outbound_link_click_through_rate = Field(name="outbound_link_click_through_rate",
                                             facebook_fields=[GraphAPIInsightsFields.outbound_clicks_ctr],
                                             mapper=ActionFieldMapper(field_filter=[
                                                 ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                      operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                      field_value=GraphAPIInsightsFields.outbound_click)]),
                                             action_breakdowns=[GraphAPIInsightsFields.action_type],
                                             field_type=FieldType.ACTION_INSIGHT)
    unique_outbound_linK_click_through_rate = Field(name="unique_outbound_linK_click_through_rate",
                                                    facebook_fields=[
                                                        GraphAPIInsightsFields.unique_outbound_clicks_ctr],
                                                    mapper=ActionFieldMapper(field_filter=[ActionFieldCondition(
                                                        field_name=GraphAPIInsightsFields.action_type,
                                                        operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                        field_value=GraphAPIInsightsFields.outbound_click)]),
                                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                                    field_type=FieldType.ACTION_INSIGHT)
    unique_clicks_all = Field(name="unique_clicks_all",
                              facebook_fields=[GraphAPIInsightsFields.unique_clicks],
                              mapper=OneToOneFieldMapper(),
                              field_type=FieldType.INSIGHT)
    unique_ctr_all = Field(name="unique_ctr_all",
                           facebook_fields=[GraphAPIInsightsFields.unique_ctr],
                           mapper=OneToOneFieldMapper(),
                           field_type=FieldType.INSIGHT)
    instant_experience_clicks_to_open = Field(name="instant_experience_clicks_to_open",
                                              facebook_fields=[
                                                  GraphAPIInsightsFields.instant_experience_clicks_to_open],
                                              mapper=OneToOneFieldMapper(),
                                              field_type=FieldType.INSIGHT)
    instant_experience_clicks_to_start = Field(name="instant_experience_clicks_to_start",
                                               facebook_fields=[
                                                   GraphAPIInsightsFields.instant_experience_clicks_to_start],
                                               mapper=OneToOneFieldMapper(),
                                               field_type=FieldType.INSIGHT)

    instant_experience_outbound_clicks = Field(name="instant_experience_outbound_clicks",
                                               facebook_fields=[
                                                   GraphAPIInsightsFields.instant_experience_outbound_clicks],
                                               mapper=OneToOneFieldMapper(),
                                               field_type=FieldType.INSIGHT)
    cost_per_link_click = Field(name="cost_per_link_click",
                                facebook_fields=[GraphAPIInsightsFields.cost_per_action_type],
                                mapper=ActionFieldMapper(
                                    field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                       operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                       field_value=GraphAPIInsightsFields.link_click)]),
                                action_breakdowns=[GraphAPIInsightsFields.action_type],
                                field_type=FieldType.ACTION_INSIGHT)

    cost_per_unique_link_click = Field(name="cost_per_unique_link_click",
                                       facebook_fields=[GraphAPIInsightsFields.cost_per_unique_action_type],
                                       mapper=ActionFieldMapper(field_filter=[
                                           ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                field_value=GraphAPIInsightsFields.link_click)]),
                                       action_breakdowns=[GraphAPIInsightsFields.action_type],
                                       field_type=FieldType.ACTION_INSIGHT)
    cost_per_outbound_click = Field(name="cost_per_outbound_click",
                                    facebook_fields=[GraphAPIInsightsFields.cost_per_outbound_click],
                                    mapper=ActionFieldMapper(field_filter=[
                                        ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                             operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                             field_value=GraphAPIInsightsFields.outbound_click)]),
                                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                                    field_type=FieldType.ACTION_INSIGHT)
    cost_per_unique_outbound_click = Field(name="cost_per_unique_outbound_click",
                                           facebook_fields=[GraphAPIInsightsFields.cost_per_unique_outbound_click],
                                           mapper=ActionFieldMapper(field_filter=[
                                               ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                    operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                    field_value=GraphAPIInsightsFields.outbound_click)]),
                                           action_breakdowns=[GraphAPIInsightsFields.action_type],
                                           field_type=FieldType.ACTION_INSIGHT)
    cost_per_unique_click_all = Field(name="cost_per_unique_click_all",
                                      facebook_fields=[GraphAPIInsightsFields.cost_per_unique_click],
                                      mapper=OneToOneFieldMapper(),
                                      field_type=FieldType.INSIGHT)
    estimated_ad_recall_lift = Field(name="estimated_ad_recall_lift",
                                     facebook_fields=[GraphAPIInsightsFields.estimated_ad_recallers],
                                     mapper=OneToOneFieldMapper(),
                                     field_type=FieldType.INSIGHT)
    estimated_ad_recall_lift_rate = Field(name="estimated_ad_recall_lift_rate",
                                          facebook_fields=[GraphAPIInsightsFields.estimated_ad_recall_rate],
                                          mapper=OneToOneFieldMapper(),
                                          field_type=FieldType.INSIGHT)
    cost_per_estimated_ad_recall_lift = Field(name="cost_per_estimated_ad_recall_lift",
                                              facebook_fields=[
                                                  GraphAPIInsightsFields.cost_per_estimated_ad_recall_lift],
                                              mapper=OneToOneFieldMapper(),
                                              field_type=FieldType.INSIGHT)
    social_spend = Field(name="social_spend",
                         facebook_fields=[GraphAPIInsightsFields.social_spend],
                         mapper=OneToOneFieldMapper(),
                         field_type=FieldType.INSIGHT)
