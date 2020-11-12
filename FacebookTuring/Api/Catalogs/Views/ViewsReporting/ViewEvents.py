from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumn import ViewColumn
from FacebookTuring.Api.Catalogs.Columns.ViewColumns.ViewColumnGroupEnum import ViewColumnGroupEnum
from Core.Metadata.Columns.ViewColumns.ViewColumnType import ViewColumnType


class ViewEvents:
    rsvp = ViewColumn(id=Autoincrement.hex_string("rsvp"), display_name="RSVP",
                      primary_value=FieldsMetadata.event_responses, type_id=ViewColumnType.NUMBER.value,
                      group_display_name=ViewColumnGroupEnum.EVENTS.value)
