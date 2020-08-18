import copy
import typing

from bson import BSON
from marshmallow import pre_load, INCLUDE

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Mappings.FacebookToTuringStatusMapping import map_facebook_status


class CampaignMapping(MapperBase):
    """Mappers between Facebook Campaign Object and Domain campaign model"""

    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = Tools.convert_to_json(data)

        if not data:
            return data

        # map facebook structure details
        data[MiscFieldsEnum.business_owner_facebook_id] = None
        data[GraphAPIInsightsFields.account_id] = data.get(GraphAPIInsightsFields.account_id, None)
        data[GraphAPIInsightsFields.campaign_name] = data.get(GraphAPIInsightsFields.name, None)
        data[GraphAPIInsightsFields.campaign_id] = data.get(GraphAPIInsightsFields.structure_id, None)
        data[GraphAPIInsightsFields.objective] = data.get(GraphAPIInsightsFields.objective, None)
        data[GraphAPIInsightsFields.daily_budget] = data.get(GraphAPIInsightsFields.daily_budget, None)
        data[GraphAPIInsightsFields.lifetime_budget] = data.get(GraphAPIInsightsFields.lifetime_budget, None)
        data[GraphAPIInsightsFields.created_time] = data.get(GraphAPIInsightsFields.created_time, None)
        data[GraphAPIInsightsFields.start_time] = data.get(GraphAPIInsightsFields.start_time, None)
        data[GraphAPIInsightsFields.end_time] = data.get(GraphAPIInsightsFields.end_time, None)
        data[MiscFieldsEnum.last_updated_at] = data.get(GraphAPIInsightsFields.updated_time, None)

        # encode structure details
        data[MiscFieldsEnum.details] = BSON.encode(copy.deepcopy(data))

        # map facebook status
        data[MiscFieldsEnum.status] = map_facebook_status(data.get(GraphAPIInsightsFields.effective_status, None))
        data[MiscFieldsEnum.actions] = {}

        return self._remove_unknown_data(data)
