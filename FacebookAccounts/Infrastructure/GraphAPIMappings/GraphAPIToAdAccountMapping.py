import hashlib
import typing

from marshmallow import fields, EXCLUDE, pre_load

from Core.mapper import MapperBase
from Core.Tools.Misc.FiledEntityStatus import FiledEntityStatus
from Core.Tools.Misc.ObjectSerializers import object_to_json


class GraphAPIToAdAccountMapping(MapperBase):
    class Meta:
        unknown = EXCLUDE

    facebook_id = fields.String()
    name = fields.String()
    owner_business_facebook_id = fields.String()
    owner_business_name = fields.String()
    currency = fields.String()
    status = fields.Integer()

    @pre_load
    def map(self, data, **kwargs):
        if not isinstance(data, typing.Mapping):
            data = object_to_json(data)

        if "business" in data.keys():
            business_details = data.pop("business")
            data["owner_business_facebook_id"] = business_details.pop("id")
            data["owner_business_name"] = business_details.pop("name")

        if "account_status" in data and data["account_status"]:
            status = data.pop("account_status")
            data["status"] = self.__map_facebook_status(status) if status else FiledEntityStatus.ACTIVE.value
        else:
            data["status"] = data.pop("account_status")

        facebook_id = data.pop("id")
        data["facebook_id"] = facebook_id if facebook_id else self.__create_hash_id(data["name"], data["currency"])

        return data

    @staticmethod
    def __create_hash_id(facebook_name: typing.AnyStr = None,
                         currency: typing.AnyStr = None) -> typing.AnyStr:

        if not facebook_name:
            facebook_name = "Unknown"

        name_string = currency + facebook_name
        return hashlib.sha1(name_string.encode('utf-8')).hexdigest()

    def __map_facebook_status(self, facebook_status: int) -> int:
        facebook_to_filed_status_mapping = {
            '1': FiledEntityStatus.ACTIVE.value,
            '2': FiledEntityStatus.PAUSED.value,
            '3': FiledEntityStatus.PAUSED.value,
            '7': FiledEntityStatus.PAUSED.value,
            '8': FiledEntityStatus.PAUSED.value,
            '9': FiledEntityStatus.PAUSED.value,
            '100': FiledEntityStatus.PAUSED.value,
            '101': FiledEntityStatus.PAUSED.value,
            '201': FiledEntityStatus.ACTIVE.value,
            '202': FiledEntityStatus.PAUSED.value,
        }

        return facebook_to_filed_status_mapping[str(facebook_status)]
