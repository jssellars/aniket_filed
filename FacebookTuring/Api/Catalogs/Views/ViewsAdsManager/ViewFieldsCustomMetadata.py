from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnCategoryEnum import ViewColumnCategoryEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewFieldsCustomMetadata:
    conversions = ViewColumn(Autoincrement.hex_string('conversions'), display_name="Conversions (All)",
                             primary_value=FieldsMetadata.conversions,
                             type_id=ViewColumnTypeEnum.NUMBER.value,
                             category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    cost_per_conversion = ViewColumn(Autoincrement.hex_string('cost_per_conversion'),
                                     display_name="Cost per conversion (All)",
                                     primary_value=FieldsMetadata.cost_per_conversion,
                                     type_id=ViewColumnTypeEnum.CURRENCY.value,
                                     category_id=ViewColumnCategoryEnum.PERFORMANCE.value, is_fixed=False)
    messaging_conversation_started_7d = ViewColumn(Autoincrement.hex_string('messaging_conversation_started_7d'),
                                                   display_name="Messaging conversations started in the last 7 days",
                                                   primary_value=FieldsMetadata.messaging_conversation_started_7d,
                                                   type_id=ViewColumnTypeEnum.NUMBER.value,
                                                   category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    click_to_play_video_25p = ViewColumn(Autoincrement.hex_string('click_to_play_video_25p'),
                                         display_name="Click to play 25% watched actions",
                                         primary_value=FieldsMetadata.click_to_play_video_25p,
                                         type_id=ViewColumnTypeEnum.NUMBER.value,
                                         category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    autoplay_video_25p = ViewColumn(Autoincrement.hex_string('autoplay_video_25p'),
                                    display_name="Auto play 25% watched actions",
                                    primary_value=FieldsMetadata.autoplay_video_25p,
                                    type_id=ViewColumnTypeEnum.NUMBER.value,
                                    category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    click_to_play_video_50p = ViewColumn(Autoincrement.hex_string('click_to_play_video_50p'),
                                         display_name="Click to play 50% watched actions",
                                         primary_value=FieldsMetadata.click_to_play_video_50p,
                                         type_id=ViewColumnTypeEnum.NUMBER.value,
                                         category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    autoplay_video_50p = ViewColumn(Autoincrement.hex_string('autoplay_video_50p'),
                                    display_name="Auto play 50% watched actions",
                                    primary_value=FieldsMetadata.autoplay_video_50p,
                                    type_id=ViewColumnTypeEnum.NUMBER.value,
                                    category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    click_to_play_video_75p = ViewColumn(Autoincrement.hex_string('click_to_play_video_75p'),
                                         display_name="Click to play 75% watched actions",
                                         primary_value=FieldsMetadata.click_to_play_video_75p,
                                         type_id=ViewColumnTypeEnum.NUMBER.value,
                                         category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    autoplay_video_75p = ViewColumn(Autoincrement.hex_string('autoplay_video_75p'),
                                    display_name="Auto play 75% watched actions",
                                    primary_value=FieldsMetadata.autoplay_video_75p,
                                    type_id=ViewColumnTypeEnum.NUMBER.value,
                                    category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    click_to_play_video_95p = ViewColumn(Autoincrement.hex_string('click_to_play_video_95p'),
                                         display_name="Click to play 95% watched actions",
                                         primary_value=FieldsMetadata.click_to_play_video_95p,
                                         type_id=ViewColumnTypeEnum.NUMBER.value,
                                         category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    autoplay_video_95p = ViewColumn(Autoincrement.hex_string('autoplay_video_95p'),
                                    display_name="Auto play 95% watched actions",
                                    primary_value=FieldsMetadata.autoplay_video_95p,
                                    type_id=ViewColumnTypeEnum.NUMBER.value,
                                    category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    click_to_play_video_100p = ViewColumn(Autoincrement.hex_string('click_to_play_video_100p'),
                                          display_name="Click to play 100% watched actions",
                                          primary_value=FieldsMetadata.click_to_play_video_100p,
                                          type_id=ViewColumnTypeEnum.NUMBER.value,
                                          category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    autoplay_video_100p = ViewColumn(Autoincrement.hex_string('autoplay_video_100p'),
                                     display_name="Auto play 100% watched actions",
                                     primary_value=FieldsMetadata.autoplay_video_100p,
                                     type_id=ViewColumnTypeEnum.NUMBER.value,
                                     category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
    post_likes = ViewColumn(Autoincrement.hex_string('post_likes'), display_name="Post likes",
                            primary_value=FieldsMetadata.post_likes, type_id=ViewColumnTypeEnum.NUMBER.value,
                            category_id=ViewColumnCategoryEnum.ENGAGEMENT.value, is_fixed=False)
