import copy
from typing import Any, Dict

from facebook_business.adobjects.targeting import Targeting
from marshmallow import INCLUDE, pre_load

from Core.Web.FacebookGraphAPI.search import GraphAPICountryGroupsLegend
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

    LOCATION_TYPES_TO_SINGULAR = {
        "countries": "country",
        "regions": "region",
        "geo_markets": "geo_market",
        "cities": "city",
        "zips": "zip",
        "electoral_districts": "electoral_district",
    }

    @pre_load
    def convert(self, data: Any, **kwargs):
        if not isinstance(data, Dict):
            data = Tools.convert_to_json(data)

        if "account" in data.keys():
            data["account"] = AdAccount(**data["account"])

        if "permission_for_actions" in data.keys():
            data["permission_for_actions"] = GraphAPIAudiencesPermissionsForActionsDto(
                **data["permission_for_actions"])

        if "sentence_lines" in data.keys():
            data["sentence_lines"] = [GraphAPIAudiencesSentenceLineDto(**sentence_line) for sentence_line in
                                      data["sentence_lines"]]

        if "targeting" in data.keys() and not isinstance(data["targeting"], Dict):
            targeting = data.pop("targeting")
            targeting = Tools.convert_to_json(targeting)
            data["targeting"] = copy.deepcopy(targeting)

        if "targeting" in data:
            GraphAPISavedAudienceMapping.__map_audience_locations(data)

        return data

    @classmethod
    def __map_audience_locations(cls, data: Any):
        _countries = {
            country["country_code"]: country for country in GraphAPICountryGroupsLegend().countries
        }

        targeting = data["targeting"]
        data["locations"] = []

        if Targeting.Field.geo_locations in targeting:
            geo_locations = targeting[Targeting.Field.geo_locations]

            for location_type, locations in geo_locations.items():
                _locations = []
                if location_type == Targeting.Field.countries:
                    _locations = [_countries[country_code] for country_code in locations]
                elif location_type in cls.LOCATION_TYPES_TO_SINGULAR:
                    _locations = locations

                for _location in _locations:
                    _location["type"] = cls.LOCATION_TYPES_TO_SINGULAR[location_type]

                    if "name" in _location:
                        _location["country_name"] = _location["name"]

                data["locations"].extend(_locations)
