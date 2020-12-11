import typing

from marshmallow import fields, pre_load

from Core.mapper import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPIAdAccountPageInstagramMapping(MapperBase):
    facebook_id = fields.String()
    name = fields.String()

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = Tools.convert_to_json(data)

        if "instagram_business_account" in data.keys():
            instagram_accounts = data.pop("instagram_business_account")
        else:
            instagram_accounts = None

        if instagram_accounts:
            data["name"] = instagram_accounts["username"]
            data["facebook_id"] = instagram_accounts["id"]
        del data["id"]

        return data
