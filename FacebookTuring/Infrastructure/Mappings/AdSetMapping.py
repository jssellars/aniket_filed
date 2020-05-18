import copy
import typing

from bson import BSON
from marshmallow import pre_load, INCLUDE

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Mappings.FacebookToTuringStatusMapping import map_facebook_status


class AdSetMapping(MapperBase):
    """Mappers between Facebook adset object and Domain adset model"""

    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = Tools.convert_to_json(data)

        data[MiscFieldsEnum.business_owner_facebook_id] = None
        if GraphAPIInsightsFields.name in data.keys():
            data[GraphAPIInsightsFields.adset_name] = data.get(GraphAPIInsightsFields.name)

        if GraphAPIInsightsFields.structure_id in data.keys():
            data[GraphAPIInsightsFields.adset_id] = data.get(GraphAPIInsightsFields.structure_id)

        if GraphAPIInsightsFields.campaign in data.keys():
            data[GraphAPIInsightsFields.campaign_name] = data[GraphAPIInsightsFields.campaign][
                GraphAPIInsightsFields.name]

        data[MiscFieldsEnum.last_updated_at] = data.get(GraphAPIInsightsFields.updated_time, None)
        data[MiscFieldsEnum.details] = BSON.encode(copy.deepcopy(data))
        data[MiscFieldsEnum.actions] = {}
        data[MiscFieldsEnum.status] = map_facebook_status(data.get(GraphAPIInsightsFields.status, None))

        return self._remove_unknown_data(data)
