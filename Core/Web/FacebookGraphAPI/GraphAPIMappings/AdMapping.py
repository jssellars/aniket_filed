import copy
import typing

from bson import BSON
from marshmallow import INCLUDE, pre_load

from Core.mapper import MapperBase
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookMiscFields
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FacebookToTuringStatusMapping import map_facebook_status
from Core.Web.FacebookGraphAPI.Tools import Tools


class AdMapping(MapperBase):
    """Mappers between Facebook ad object and Domain ad model"""

    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = Tools.convert_to_json(data)

        # map structure
        data[FacebookMiscFields.business_owner_facebook_id] = None
        data[GraphAPIInsightsFields.account_id] = data.get(GraphAPIInsightsFields.account_id, None)
        data[GraphAPIInsightsFields.ad_name] = data.get(GraphAPIInsightsFields.name, None)
        data[GraphAPIInsightsFields.ad_id] = data.get(GraphAPIInsightsFields.structure_id, None)
        if GraphAPIInsightsFields.adset in data.keys():
            data[GraphAPIInsightsFields.adset_name] = data[GraphAPIInsightsFields.adset].get(
                GraphAPIInsightsFields.name, None
            )
        data[GraphAPIInsightsFields.created_time] = data.get(GraphAPIInsightsFields.created_time, None)
        data[GraphAPIInsightsFields.start_time] = data.get(GraphAPIInsightsFields.start_time, None)
        data[GraphAPIInsightsFields.end_time] = data.get(GraphAPIInsightsFields.end_time, None)
        if GraphAPIInsightsFields.campaign in data.keys():
            data[GraphAPIInsightsFields.campaign_name] = data[GraphAPIInsightsFields.campaign].get(
                GraphAPIInsightsFields.name, None
            )
        data[FacebookMiscFields.last_updated_at] = data.get(GraphAPIInsightsFields.updated_time, None)

        # encode structure details
        data[FacebookMiscFields.details] = BSON.encode(copy.deepcopy(data))

        # map facebook status
        data[FacebookMiscFields.status] = map_facebook_status(data.get(GraphAPIInsightsFields.effective_status, None))
        data[FacebookMiscFields.actions] = {}

        return self._remove_unknown_data(data)
