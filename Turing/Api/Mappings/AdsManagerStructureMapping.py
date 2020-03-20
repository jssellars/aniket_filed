import typing
from marshmallow import fields, pre_load, EXCLUDE

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Turing.Infrastructure.Mappings.LevelMapping import LevelToFacebookIdKeyMapping, LevelToFacebookNameKeyMapping


class AdsManagerStructureMapping(MapperBase):
    facebook_id = fields.String()
    name = fields.String()
    facebook_details = fields.Dict()
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

        id_field_key = LevelToFacebookIdKeyMapping.get_by_name(self.__level)
        data["facebook_id"] = data.pop(id_field_key)

        name_field_key = LevelToFacebookNameKeyMapping.get_by_name(self.__level)
        data["name"] = data.pop(name_field_key)

        data["facebook_details"] = data.pop("details")
        data["action_details"] = data.pop("actions")

        return data