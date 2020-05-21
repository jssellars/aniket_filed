import typing

from marshmallow import INCLUDE, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPIAppEventTypesMapping(MapperBase):
    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.Dict):
            data = Tools.convert_to_json(data)

        return data
