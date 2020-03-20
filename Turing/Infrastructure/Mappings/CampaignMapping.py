import copy
import typing

from marshmallow import pre_load, INCLUDE

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class CampaignMapping(MapperBase):
    """Mappers between Facebook Campaign Object and Domain campaign model"""
    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = Tools.convert_to_json(data)

        data["business_owner_facebook_id"] = None
        if "name" in data.keys():
            data["campaign_name"] = data.pop("name")

        if "id" in data.keys():
            data["campaign_id"] = data.pop("id")

        data["last_updated_at"] = None
        data["details"] = copy.deepcopy(data)
        data["actions"] = {}
        data["status"] = None

        return self._remove_unknown_data(data)
