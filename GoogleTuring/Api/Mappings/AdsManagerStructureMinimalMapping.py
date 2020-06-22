import typing

from marshmallow import fields, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Tools.Misc.ObjectSerializers import object_to_json
from GoogleTuring.Infrastructure.Mappings.LevelMapping import LevelToGoogleNameKeyMapping, \
    LevelToGoogleIdKeyMapping


class AdsManagerStructureMinimalMapping(MapperBase):
    google_id = fields.String()
    name = fields.String()

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

        return data
