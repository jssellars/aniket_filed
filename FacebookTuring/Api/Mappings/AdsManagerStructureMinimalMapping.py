import typing

from marshmallow import fields, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Tools.Misc.ObjectSerializers import object_to_json
from FacebookTuring.Infrastructure.Mappings.LevelMapping import LevelToFacebookNameKeyMapping, \
    LevelToFacebookIdKeyMapping


class AdsManagerStructureMinimalMapping(MapperBase):
    facebook_id = fields.String()
    name = fields.String()

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

        return data
