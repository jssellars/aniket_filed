import typing

from marshmallow import fields, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPIBusinessMapping(MapperBase):
    id = fields.String()
    name = fields.String()

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            try:
                return [Tools.convert_to_json(entry) for entry in data]
            except Exception as e:
                return Tools.convert_to_json(data)
        else:
            return data
