import typing

from marshmallow import fields, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPIAdAccountBusinessMapping(MapperBase):
    id = fields.String()
    name = fields.String()

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = Tools.convert_to_json(data)

        business = data.pop("business")
        data["id"] = business["id"]
        data["name"] = business["name"]

        return data
