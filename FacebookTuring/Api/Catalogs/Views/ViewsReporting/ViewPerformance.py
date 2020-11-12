from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType


class ViewPerformance:
    reach = ViewColumn(id=Autoincrement.hex_string("reach"), display_name="Reach",
                       primary_value=FieldsMetadata.reach, type_id=ViewColumnType.NUMBER.value,
                       group_display_name=ViewColumnGroupEnum.PERFORMANCE.value)
    frequency = ViewColumn(id=Autoincrement.hex_string("frequency"), display_name="Frequency",
                           primary_value=FieldsMetadata.frequency, type_id=ViewColumnType.NUMBER.value,
                           group_display_name=ViewColumnGroupEnum.PERFORMANCE.value)
    impressions = ViewColumn(id=Autoincrement.hex_string("impressions"), display_name="Impressions",
                             primary_value=FieldsMetadata.impressions, type_id=ViewColumnType.NUMBER.value,
                             group_display_name=ViewColumnGroupEnum.PERFORMANCE.value)
    total_conversion_value = ViewColumn(id=Autoincrement.hex_string('total_conversion_value'),
                                        display_name='Total conversion value',
                                        primary_value=FieldsMetadata.total_conversion_value,
                                        type_id=ViewColumnType.CURRENCY.value,
                                        group_display_name=ViewColumnGroupEnum.PERFORMANCE.value)
    estimated_ad_recallers = ViewColumn(id=Autoincrement.hex_string('estimated_ad_recallers'),
                                        display_name='Estimated ad recallers',
                                        primary_value=FieldsMetadata.estimated_ad_recall_lift,
                                        type_id=ViewColumnType.NUMBER.value,
                                        group_display_name=ViewColumnGroupEnum.PERFORMANCE.value)
    estimated_ad_recaller_rate = ViewColumn(id=Autoincrement.hex_string('estimated_ar_recaller_rate'),
                                            display_name='Estimated ad recaller rate (%)',
                                            primary_value=FieldsMetadata.estimated_ad_recall_lift_rate,
                                            type_id=ViewColumnType.PERCENTAGE.value,
                                            group_display_name=ViewColumnGroupEnum.PERFORMANCE.value)
    cost_per_estimated_ad_recaller = ViewColumn(id=Autoincrement.hex_string('cost_per_estimated_ad_recaller'),
                                                display_name='Cost per estimated ad recaller',
                                                primary_value=FieldsMetadata.cost_per_estimated_ad_recall_lift,
                                                type_id=ViewColumnType.CURRENCY.value,
                                                group_display_name=ViewColumnGroupEnum.PERFORMANCE.value)
    canvas_view_percentage = ViewColumn(id=Autoincrement.hex_string('canvas_view_percentage'),
                                        display_name='Canvas view percentage',
                                        primary_value=FieldsMetadata.instant_experience_view_percentage,
                                        type_id=ViewColumnType.PERCENTAGE.value,
                                        group_display_name=ViewColumnGroupEnum.PERFORMANCE.value)
    canvas_average_view_time = ViewColumn(id=Autoincrement.hex_string('canvas_average_view_time'),
                                          display_name='Canvas average view time',
                                          primary_value=FieldsMetadata.instant_experience_view_percentage,
                                          type_id=ViewColumnType.PERCENTAGE.value,
                                          group_display_name=ViewColumnGroupEnum.PERFORMANCE.value)
