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

        if GraphAPIInsightsFields.account_id in data.keys():
            data[GraphAPIInsightsFields.account_id] = data.get(GraphAPIInsightsFields.account_id)

        if GraphAPIInsightsFields.name in data.keys():
            data[GraphAPIInsightsFields.adset_name] = data.get(GraphAPIInsightsFields.name)

        if GraphAPIInsightsFields.structure_id in data.keys():
            data[GraphAPIInsightsFields.adset_id] = data.get(GraphAPIInsightsFields.structure_id)

        if GraphAPIInsightsFields.budget_remaining in data.keys():
            data[GraphAPIInsightsFields.budget_remaining] = data.get(GraphAPIInsightsFields.budget_remaining)

        if GraphAPIInsightsFields.daily_budget in data.keys():
            data[GraphAPIInsightsFields.daily_budget] = data.get(GraphAPIInsightsFields.daily_budget)

        if GraphAPIInsightsFields.lifetime_budget in data.keys():
            data[GraphAPIInsightsFields.lifetime_budget] = data.get(GraphAPIInsightsFields.lifetime_budget)

        if GraphAPIInsightsFields.learning_stage_info in data.keys():
            data[GraphAPIInsightsFields.learning_stage_info] = data.get(GraphAPIInsightsFields.learning_stage_info)

        if GraphAPIInsightsFields.created_time in data.keys():
            data[GraphAPIInsightsFields.created_time] = data[GraphAPIInsightsFields.created_time]

        if GraphAPIInsightsFields.start_time in data.keys():
            data[GraphAPIInsightsFields.start_time] = data[GraphAPIInsightsFields.start_time]

        if GraphAPIInsightsFields.end_time in data.keys():
            data[GraphAPIInsightsFields.end_time] = data[GraphAPIInsightsFields.end_time]

        if GraphAPIInsightsFields.campaign in data.keys():
            data[GraphAPIInsightsFields.campaign_name] = data[GraphAPIInsightsFields.campaign][
                GraphAPIInsightsFields.name]

        data[MiscFieldsEnum.last_updated_at] = data.get(GraphAPIInsightsFields.updated_time, None)
        data[MiscFieldsEnum.details] = BSON.encode(copy.deepcopy(data))
        data[MiscFieldsEnum.actions] = {}
        data[MiscFieldsEnum.status] = map_facebook_status(data.get(GraphAPIInsightsFields.effective_status, None))

        return self._remove_unknown_data(data)
