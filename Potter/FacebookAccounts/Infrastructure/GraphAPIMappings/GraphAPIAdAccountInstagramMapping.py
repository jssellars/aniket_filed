import typing

from marshmallow import fields, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPIAdAccountInstagramMapping(MapperBase):
    ig_accounts = fields.List(fields.Dict)

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = Tools.convert_to_json(data)

        if "instagram_accounts" in data.keys():
            instagram_accounts = data.pop("instagram_accounts")["data"]
        else:
            instagram_accounts = []

        data["ig_accounts"] = [{"facebook_id": entry["id"], "name": entry["username"]} for entry in instagram_accounts]
        del data["id"]

        return data
