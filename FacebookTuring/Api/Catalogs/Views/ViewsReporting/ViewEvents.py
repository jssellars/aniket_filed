from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnTypeEnum import ViewColumnTypeEnum


class ViewEvents:
    rsvp = ViewColumn(id=Autoincrement.hex_string("rsvp"), display_name="RSVP",
                      primary_value=FieldsMetadata.event_responses, type_id=ViewColumnTypeEnum.NUMBER.value,
                      group_display_name=ViewColumnGroupEnum.EVENTS.value)
