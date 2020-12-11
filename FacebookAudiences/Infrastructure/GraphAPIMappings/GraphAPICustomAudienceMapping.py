import typing

from marshmallow import INCLUDE, pre_load

from Core.mapper import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesLookalikeSpecDto import \
    GraphAPIAudiencesLookalikeSpecDto
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesPermissionsForActionsDto import \
    GraphAPIAudiencesPermissionsForActionsDto
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPICustomAudienceDto import OperationStatus, DataSource, \
    SharingStatus


class GraphAPICustomAudienceMapping(MapperBase):
    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = Tools.convert_to_json(data)

        if "permissions_for_actions" in data.keys():
            data["permissions_for_actions"] = GraphAPIAudiencesPermissionsForActionsDto(
                **data["permissions_for_actions"])

        if "external_event_source" in data.keys():
            data["external_event_source"] = data["external_event_source"]["id"]

        if "operation_status" in data.keys():
            data["operation_status"] = OperationStatus(**data["operation_status"])

        if "delivery_status" in data.keys():
            data["delivery_status"] = OperationStatus(**data["delivery_status"])

        if "data_source" in data.keys():
            data["data_source"] = DataSource(**data["data_source"])

        if "sharing_status" in data.keys():
            data["sharing_status"] = SharingStatus(**data["sharing_status"])

        if "lookalike_spec" in data.keys():
            data["lookalike_spec"] = GraphAPIAudiencesLookalikeSpecDto(**data["lookalike_spec"])

        return data
