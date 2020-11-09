from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewVideos:
    thru_plays = ViewColumn(id=Autoincrement.hex_string("video_views"), display_name="Video views",
                             primary_value=FieldsMetadata.thru_plays, type_id=ViewColumnTypeEnum.NUMBER.value,
                             group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    average_duration_video_view = ViewColumn(id=Autoincrement.hex_string('avg_duration_video_viewed'),
                                             display_name='Avg duration video viewed (secs)',
                                             primary_value=FieldsMetadata.video_average_play_time,
                                             type_id=ViewColumnTypeEnum.NUMBER.value,
                                             group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    video_views_25p = ViewColumn(id=Autoincrement.hex_string('video_views_25p'),
                                 display_name='Video views to 25% (secs)',
                                 primary_value=FieldsMetadata.video_plays_25p,
                                 type_id=ViewColumnTypeEnum.NUMBER.value,
                                 group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    video_views_50p = ViewColumn(id=Autoincrement.hex_string('video_views_50p'),
                                 display_name='Video views to 50% (secs)',
                                 primary_value=FieldsMetadata.video_plays_50p,
                                 type_id=ViewColumnTypeEnum.NUMBER.value,
                                 group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    video_views_75p = ViewColumn(id=Autoincrement.hex_string('video_views_75p'),
                                 display_name='Video views to 75% (secs)',
                                 primary_value=FieldsMetadata.video_plays_75p,
                                 type_id=ViewColumnTypeEnum.NUMBER.value,
                                 group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    video_views_95p = ViewColumn(id=Autoincrement.hex_string('video_views_95p'),
                                 display_name='Video views to 95% (secs)',
                                 primary_value=FieldsMetadata.video_plays_95p,
                                 type_id=ViewColumnTypeEnum.NUMBER.value,
                                 group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    video_views_100p = ViewColumn(id=Autoincrement.hex_string('video_views_100p'),
                                  display_name='Video views to 100% (secs)',
                                  primary_value=FieldsMetadata.video_plays_100p,
                                  type_id=ViewColumnTypeEnum.NUMBER.value,
                                  group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    videos_completely_viewed = ViewColumn(id=Autoincrement.hex_string('videos_completely_viewed'),
                                          display_name='Video completely viewed (secs)',
                                          primary_value=FieldsMetadata.video_plays,
                                          type_id=ViewColumnTypeEnum.NUMBER.value,
                                          group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    continuous_video_views_2s = ViewColumn(id=Autoincrement.hex_string('continuous_video_views_2s'),
                                           display_name='2-second continuous video views',
                                           primary_value=FieldsMetadata.continuous_video_plays_2s,
                                           type_id=ViewColumnTypeEnum.NUMBER.value,
                                           group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    cost_per_2s_continuous_video_views = ViewColumn(id=Autoincrement.hex_string('cost_per_2s_continuous_video_views'),
                                                    display_name='Cost per 2-second continuous video view',
                                                    primary_value=FieldsMetadata.cost_per_continuous_video_play_2s,
                                                    type_id=ViewColumnTypeEnum.CURRENCY.value,
                                                    group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    video_plays = ViewColumn(id=Autoincrement.hex_string('video_playes'),
                             display_name='Video plays',
                             primary_value=FieldsMetadata.video_plays,
                             type_id=ViewColumnTypeEnum.NUMBER.value,
                             group_display_name=ViewColumnGroupEnum.VIDEOS.value)
    video_views_15s = ViewColumn(id=Autoincrement.hex_string('video_views_15s'),
                                 display_name='15 sec video views',
                                 primary_value=FieldsMetadata.video_plays_15s,
                                 type_id=ViewColumnTypeEnum.NUMBER.value,
                                 group_display_name=ViewColumnGroupEnum.VIDEOS.value)
