import copy
import typing

from bson import BSON
from marshmallow import INCLUDE, pre_load

from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.Tools import Tools
from Core.mapper import MapperBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from FacebookTuring.Infrastructure.Mappings.FacebookToTuringStatusMapping import map_facebook_status


class AdSetMapping(MapperBase):
    """Mappers between Facebook adset object and Domain adset model"""

    __pixel_id = "pixel_id"

    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = Tools.convert_to_json(data)

        # map structure details
        data[FacebookMiscFields.business_owner_facebook_id] = None
        data[GraphAPIInsightsFields.account_id] = data.get(GraphAPIInsightsFields.account_id, None)
        data[GraphAPIInsightsFields.adset_name] = data.get(GraphAPIInsightsFields.name, None)
        data[GraphAPIInsightsFields.adset_id] = data.get(GraphAPIInsightsFields.structure_id, None)
        data[GraphAPIInsightsFields.budget_remaining] = data.get(GraphAPIInsightsFields.budget_remaining, None)
        data[GraphAPIInsightsFields.daily_budget] = data.get(GraphAPIInsightsFields.daily_budget, None)
        data[GraphAPIInsightsFields.lifetime_budget] = data.get(GraphAPIInsightsFields.lifetime_budget, None)
        data[GraphAPIInsightsFields.learning_stage_info] = data.get(GraphAPIInsightsFields.learning_stage_info, None)
        data[GraphAPIInsightsFields.created_time] = data.get(GraphAPIInsightsFields.created_time, None)
        data[GraphAPIInsightsFields.start_time] = data.get(GraphAPIInsightsFields.start_time, None)
        data[GraphAPIInsightsFields.end_time] = data.get(GraphAPIInsightsFields.end_time, None)
        if GraphAPIInsightsFields.campaign in data.keys():
            data[GraphAPIInsightsFields.campaign_name] = data[GraphAPIInsightsFields.campaign].get(
                GraphAPIInsightsFields.name, None
            )
        data[FacebookMiscFields.last_updated_at] = data.get(GraphAPIInsightsFields.updated_time, None)

        # Save the promoted object custom event type if there is a pixel
        data[GraphAPIInsightsFields.custom_event_type] = None
        promoted_event = data.get(GraphAPIInsightsFields.promoted_object, None)
        if promoted_event:
            if self.__pixel_id in promoted_event:
                data[GraphAPIInsightsFields.custom_event_type] = promoted_event.get(
                    GraphAPIInsightsFields.custom_event_type, None
                )

        # encode structure details
        data[FacebookMiscFields.details] = BSON.encode(copy.deepcopy(data))

        # map facebook status
        data[FacebookMiscFields.status] = map_facebook_status(data.get(GraphAPIInsightsFields.effective_status, None))
        data[FacebookMiscFields.actions] = {}

        return self._remove_unknown_data(data)

