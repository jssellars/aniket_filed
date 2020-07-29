from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnCategoryEnum import ViewColumnCategoryEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewFieldsBreakdownsMetadata:
    age_breakdown = ViewColumn(Autoincrement.hex_string('age_breakdown'), display_name="Age",
                               primary_value=FieldsMetadata.age_breakdown,
                               type_id=ViewColumnTypeEnum.TEXT.value,
                               category_id=ViewColumnCategoryEnum.COMMON.value, is_fixed=False)
    gender_breakdown = ViewColumn(Autoincrement.hex_string('gender_breakdown'), display_name="Gender",
                                  primary_value=FieldsMetadata.gender_breakdown,
                                  type_id=ViewColumnTypeEnum.TEXT.value,
                                  category_id=ViewColumnCategoryEnum.COMMON.value, is_fixed=False)
    placements = ViewColumn(Autoincrement.hex_string('placements'), display_name="Placements",
                            primary_value=FieldsMetadata.placement,
                            type_id=ViewColumnTypeEnum.TEXT.value,
                            category_id=ViewColumnCategoryEnum.COMMON.value, is_fixed=False)
    country = ViewColumn(Autoincrement.hex_string('country'), display_name="Country",
                         primary_value=FieldsMetadata.country,
                         type_id=ViewColumnTypeEnum.TEXT.value,
                         category_id=ViewColumnCategoryEnum.COMMON.value, is_fixed=False)
    region = ViewColumn(Autoincrement.hex_string('region'), display_name="Region",
                        primary_value=FieldsMetadata.region,
                        type_id=ViewColumnTypeEnum.TEXT.value,
                        category_id=ViewColumnCategoryEnum.COMMON.value, is_fixed=False)
    publisher_platform = ViewColumn(Autoincrement.hex_string('publisher_platform'), display_name="Publisher platform",
                                    primary_value=FieldsMetadata.publisher_platform,
                                    type_id=ViewColumnTypeEnum.TEXT.value,
                                    category_id=ViewColumnCategoryEnum.COMMON.value, is_fixed=False)
    dma = ViewColumn(Autoincrement.hex_string('dma'), display_name="DMA",
                     primary_value=FieldsMetadata.dma,
                     type_id=ViewColumnTypeEnum.TEXT.value,
                     category_id=ViewColumnCategoryEnum.COMMON.value, is_fixed=False)
    frequency_value = ViewColumn(Autoincrement.hex_string('frequency_value'), display_name="Frequency value",
                                 primary_value=FieldsMetadata.frequency_value,
                                 type_id=ViewColumnTypeEnum.TEXT.value,
                                 category_id=ViewColumnCategoryEnum.COMMON.value, is_fixed=False)
    device_platform = ViewColumn(Autoincrement.hex_string('device_platform'), display_name="Device platform",
                                 primary_value=FieldsMetadata.device_platform,
                                 type_id=ViewColumnTypeEnum.TEXT.value,
                                 category_id=ViewColumnCategoryEnum.COMMON.value, is_fixed=False)
    action_destination = ViewColumn(Autoincrement.hex_string('device_platform'), display_name="Destination",
                                    primary_value=FieldsMetadata.destination_breakdown,
                                    type_id=ViewColumnTypeEnum.TEXT.value,
                                    category_id=ViewColumnCategoryEnum.COMMON.value, is_fixed=False)
