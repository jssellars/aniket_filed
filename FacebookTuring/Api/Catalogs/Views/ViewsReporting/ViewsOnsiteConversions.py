from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewPerformance:
    post_saves = ViewColumn(id=Autoincrement.hex_string("post_saves"), display_name="Post saves",
                            primary_value=FieldsMetadata.post_saves, type_id=ViewColumnTypeEnum.NUMBER.value,
                            group_display_name=ViewColumnGroupEnum.ONSITE_CONVERSIONS.value)
