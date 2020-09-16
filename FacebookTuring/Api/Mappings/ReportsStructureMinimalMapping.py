import typing

from marshmallow import fields, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Tools.Misc.ObjectSerializers import object_to_json
from FacebookTuring.Infrastructure.Mappings.LevelMapping import LevelToFacebookNameKeyMapping, \
    LevelToFacebookRequiredIdsKeyMapping, LevelToFacebookDeleteNamesKeyMapping


class ReportsStructureMinimalMapping(MapperBase):
    keys = fields.Dict()
    display_name = fields.String()
    status = fields.Integer()

    def __init__(self, level=None, **kwargs):
        self.__level = level
        super().__init__(**kwargs)

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = object_to_json(data)

        id_field_keys = LevelToFacebookRequiredIdsKeyMapping.get_by_name(self.__level)

        data['keys'] = {}
        for id_field_key in id_field_keys:
            data["keys"][id_field_key] = data.pop(id_field_key)


        name_field_key = LevelToFacebookNameKeyMapping.get_by_name(self.__level)
        data["display_name"] = data.pop(name_field_key)

        keys_to_remove = LevelToFacebookDeleteNamesKeyMapping.get_by_name(self.__level)
        for key_to_remove in keys_to_remove:
            data.pop(key_to_remove)

        return data
