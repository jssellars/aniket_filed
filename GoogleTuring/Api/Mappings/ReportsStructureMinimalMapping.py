import typing

from marshmallow import fields, pre_load

from Core.mapper import MapperBase
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.Web.GoogleAdsAPI.AdsAPIMappings.LevelMapping import (
    LevelToGoogleDeleteNamesKeyMapping,
    LevelToGoogleNameKeyMapping,
    LevelToGoogleRequiredIdsKeyMapping,
)


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

        id_field_keys = LevelToGoogleRequiredIdsKeyMapping.get_by_name(self.__level)

        data["keys"] = {}
        for id_field_key in id_field_keys:
            data["keys"][id_field_key] = data.pop(id_field_key)

        name_field_key = LevelToGoogleNameKeyMapping.get_by_name(self.__level)
        data["display_name"] = data.pop(name_field_key)

        keys_to_remove = getattr(LevelToGoogleDeleteNamesKeyMapping, self.__level.upper())
        for key_to_remove in keys_to_remove:
            data.pop(key_to_remove)

        return data
