import typing

from marshmallow import fields, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPIAdAccountSpentMapping(MapperBase):
    ad_account_id = fields.String()
    business_id = fields.String()
    business_name = fields.String()
    amount_spent = fields.Float()
    currency = fields.String()

    @pre_load
    def convert(self, data: typing.Dict, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            return Tools.convert_to_json(data)

        if "id" in data.keys():
            data["ad_account_id"] = data.pop("id")

        if "account_id" in data.keys():
            data["ad_account_id"] = data.pop("account_id")

        if "currency" in data.keys():
            data["currency"] = data.pop("currency")

        if "business" in data.keys():
            data["business_id"] = data["business"]["id"]
            data["business_name"] = data["business"]["name"]
            del data["business"]

        if "insights" in data.keys():
            data["amount_spent"] = data["insights"]["data"][0]["spend"]
            if data["amount_spent"] is None:
                data["amount_spent"] = 0.0
            del data["insights"]

        return data
