import copy
import typing

from marshmallow import INCLUDE, pre_load

from Core.mapper import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesPermissionsForActionsDto import \
    GraphAPIAudiencesPermissionsForActionsDto
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesSentenceLineDto import \
    GraphAPIAudiencesSentenceLineDto
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPISavedAudienceDto import AdAccount


class GraphAPISavedAudienceMapping(MapperBase):
    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.Dict):
            data = Tools.convert_to_json(data)

        if "account" in data.keys():
            data["account"] = AdAccount(**data["account"])

        if "permission_for_actions" in data.keys():
            data["permission_for_actions"] = GraphAPIAudiencesPermissionsForActionsDto(
                **data["permission_for_actions"])

        if "sentence_lines" in data.keys():
            data["sentence_lines"] = [GraphAPIAudiencesSentenceLineDto(**sentence_line) for sentence_line in
                                      data["sentence_lines"]]

        if "targeting" in data.keys() and not isinstance(data["targeting"], typing.Dict):
            targeting = data.pop("targeting")
            targeting = Tools.convert_to_json(targeting)
            data["targeting"] = copy.deepcopy(targeting)

        return data
