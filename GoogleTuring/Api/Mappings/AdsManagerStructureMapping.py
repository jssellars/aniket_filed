import typing

from marshmallow import EXCLUDE, fields, pre_load

from Core.mapper import MapperBase
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.GoogleAdsAPI.AdsAPIMappings.LevelMapping import LevelToGoogleIdKeyMapping, LevelToGoogleNameKeyMapping


class AdsManagerStructureMapping(MapperBase):
    google_id = fields.String()
    name = fields.String()
    google_details = fields.Dict()
    action_details = fields.Dict(allow_none=True)

    class Meta:
        unknown = EXCLUDE

    def __init__(self, level=None, **kwargs):
        self.__level = level
        super().__init__(**kwargs)

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = object_to_json(data)

        id_field_key = LevelToGoogleIdKeyMapping.get_by_name(self.__level)
        data["google_id"] = data.pop(id_field_key)

        name_field_key = LevelToGoogleNameKeyMapping.get_by_name(self.__level)
        data["name"] = data.pop(name_field_key)

        data["google_details"] = data.pop("details")
        data["action_details"] = data.pop("actions")

        return data
