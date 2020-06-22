from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewEngagement:
    page_likes = ViewColumn(id=Autoincrement.hex_string("page_likes"), display_name="Page likes",
                            primary_value=FieldsMetadata.page_likes, type_id=ViewColumnTypeEnum.NUMBER.value,
                            group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    page_engagements = ViewColumn(id=Autoincrement.hex_string("page_engagements"), display_name="Page engagements",
                                  primary_value=FieldsMetadata.page_engagement,
                                  type_id=ViewColumnTypeEnum.NUMBER.value,
                                  group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    post_engagements = ViewColumn(id=Autoincrement.hex_string("post_engagements"), display_name="Post engagements",
                                  primary_value=FieldsMetadata.page_likes, type_id=ViewColumnTypeEnum.NUMBER.value,
                                  group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    post_likes = ViewColumn(id=Autoincrement.hex_string("post_likes"), display_name="Post likes",
                            primary_value=FieldsMetadata.post_likes, type_id=ViewColumnTypeEnum.NUMBER.value,
                            group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    post_comments = ViewColumn(id=Autoincrement.hex_string("post_comments"), display_name="Post comments",
                               primary_value=FieldsMetadata.page_likes, type_id=ViewColumnTypeEnum.NUMBER.value,
                               group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    post_shares = ViewColumn(id=Autoincrement.hex_string('post_shares'), display_name='Post shares',
                             primary_value=FieldsMetadata.post_shares, type_id=ViewColumnTypeEnum.NUMBER.value,
                             group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    photo_views = ViewColumn(id=Autoincrement.hex_string("photo_views"), display_name="Photo views",
                             primary_value=FieldsMetadata.photo_views, type_id=ViewColumnTypeEnum.NUMBER.value,
                             group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    checkins = ViewColumn(id=Autoincrement.hex_string("checkins"), display_name="checkins",
                          primary_value=FieldsMetadata.checkins, type_id=ViewColumnTypeEnum.NUMBER.value,
                          group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    game_plays = ViewColumn(id=Autoincrement.hex_string("game_plays"), display_name="Game plays",
                            primary_value=FieldsMetadata.game_plays_total, type_id=ViewColumnTypeEnum.NUMBER.value,
                            group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    post_engagement_rate = ViewColumn(id=Autoincrement.hex_string("engagement_rate"),
                                      display_name="Post engagement rate (%)",
                                      primary_value=FieldsMetadata.post_engagement_rate,
                                      type_id=ViewColumnTypeEnum.PERCENTAGE.value,
                                      group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    blocked_messaging_conversations = ViewColumn(id=Autoincrement.hex_string('blocked_messaging_conversations'),
                                                 display_name='Blocked messaging conversations',
                                                 primary_value=FieldsMetadata.blocked_messaging_connections,
                                                 type_id=ViewColumnTypeEnum.NUMBER.value,
                                                 group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    messaging_replies = ViewColumn(id=Autoincrement.hex_string('messaging_replies'),
                                   display_name='Messaging replies',
                                   primary_value=FieldsMetadata.messaging_replies,
                                   type_id=ViewColumnTypeEnum.NUMBER.value,
                                   group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    new_messaging_connections = ViewColumn(id=Autoincrement.hex_string('new_messaging_connections'),
                                           display_name='New messaging connections',
                                           primary_value=FieldsMetadata.new_messaging_connections,
                                           type_id=ViewColumnTypeEnum.NUMBER.value,
                                           group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    messaging_conversations_started = ViewColumn(id=Autoincrement.hex_string('messaging_conversations_started'),
                                                 display_name='Messaging conversations started',
                                                 primary_value=FieldsMetadata.messaging_conversation_started_7d,
                                                 type_id=ViewColumnTypeEnum.NUMBER.value,
                                                 group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
    engagement_rate = ViewColumn(id=Autoincrement.hex_string('engagement_rate'),
                                 display_name='Engagement rate (%)',
                                 primary_value=FieldsMetadata.engagement_rate,
                                 type_id=ViewColumnTypeEnum.PERCENTAGE.value,
                                 group_display_name=ViewColumnGroupEnum.ENGAGEMENT.value)
