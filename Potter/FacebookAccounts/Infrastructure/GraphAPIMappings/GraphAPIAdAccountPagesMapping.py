import typing

from marshmallow import fields, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPIAdAccountPagesMapping(MapperBase):
    pages = fields.List(fields.Dict)

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = Tools.convert_to_json(data)

        if "owned_pages" in data.keys():
            pages = data.pop("owned_pages")["data"]
        elif "client_pages" in data.keys():
            pages = data.pop("client_pages")["data"]
        else:
            pages = []

        data["pages"] = [{"facebook_id": entry["id"], "name": entry["name"]} for entry in pages]
        del data["id"]

        return data
