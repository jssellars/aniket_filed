import typing

from marshmallow import fields, EXCLUDE, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
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
                data["status"] = self.__map_facebook_status(status)
            else:
                # todo: ask Sebi / Razvan to allow for status == null
                data["status"] = data.pop("account_status")

            data["facebook_id"] = data.pop("id")

        return data

    def __map_facebook_status(self, facebook_status):
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
            '202': FiledEntityStatus.PAUSED.value
        }

        return facebook_to_filed_status_mapping[str(facebook_status)]