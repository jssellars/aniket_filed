import copy
import logging
from functools import lru_cache
from typing import Any, Dict

from Core.mapper import MapperBase
from Core.Web.FacebookGraphAPI.search import GraphAPICountryGroupsLegend, GraphAPILanguagesHandler
from Core.Web.FacebookGraphAPI.Tools import Tools
from facebook_business.adobjects.abstractcrudobject import AbstractCrudObject
from facebook_business.adobjects.flexibletargeting import FlexibleTargeting
from facebook_business.adobjects.targeting import Targeting
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesPermissionsForActionsDto import (
    GraphAPIAudiencesPermissionsForActionsDto,
)
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesSentenceLineDto import (
    GraphAPIAudiencesSentenceLineDto,
)
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPISavedAudienceDto import AdAccount
from marshmallow import INCLUDE, pre_load

logger = logging.getLogger(__name__)


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
            data["permission_for_actions"] = GraphAPIAudiencesPermissionsForActionsDto(**data["permission_for_actions"])

        if "sentence_lines" in data.keys():
            data["sentence_lines"] = [
                GraphAPIAudiencesSentenceLineDto(**sentence_line) for sentence_line in data["sentence_lines"]
            ]

        if "targeting" in data.keys() and not isinstance(data["targeting"], Dict):
            targeting = data.pop("targeting")
            targeting = Tools.convert_to_json(targeting)
            data["targeting"] = copy.deepcopy(targeting)

        if "targeting" in data:
            self.__map_audience_locations(data)
            self.__map_audience_languages(data)
            self.__map_audience_interests(data)

        return data

    def __map_audience_locations(self, data: Any):
        _countries = {country["country_code"]: country for country in GraphAPICountryGroupsLegend().countries}

        targeting = data["targeting"]
        data["locations"] = []

        if Targeting.Field.geo_locations in targeting:
            geo_locations = targeting[Targeting.Field.geo_locations]

            for location_type, locations in geo_locations.items():
                _locations = []
                if location_type == Targeting.Field.countries:
                    _locations = [_countries[country_code] for country_code in locations]
                elif location_type in self.LOCATION_TYPES_TO_SINGULAR:
                    _locations = locations

                for _location in _locations:
                    _location["type"] = self.LOCATION_TYPES_TO_SINGULAR[location_type]

                    if "name" in _location:
                        _location["country_name"] = _location["name"]

                data["locations"].extend(_locations)

    def __map_audience_languages(self, data: Any):  # noqa
        targeting = data["targeting"]
        data["languages"] = []
        if Targeting.Field.locales in targeting:
            _languages = {language["key"]: language for language in GraphAPILanguagesHandler().get_all()}

            data["languages"].extend(
                [_languages[key] for key in targeting[Targeting.Field.locales] if key in _languages]
            )

    def __map_audience_interests(self, data: Any):
        data["interests"] = []
        data["narrow_interests"] = []
        data["excluded_interests"] = []

        targeting = data["targeting"]
        if Targeting.Field.flexible_spec in targeting:
            flexible_spec = targeting[Targeting.Field.flexible_spec]
            flexible_targeting = flexible_spec[0]
            for interest in flexible_targeting.get(FlexibleTargeting.Field.interests, []):
                self.__try_add_interest_to_audience(data["interests"], interest)

            # TODO: for now we are intersecting just 2 audiences, we might extend this in the near future
            if len(flexible_spec) > 1:
                flexible_targeting = flexible_spec[1]
                for interest in flexible_targeting.get(FlexibleTargeting.Field.interests, []):
                    self.__try_add_interest_to_audience(data["narrow_interests"], interest)
        else:
            for interest in targeting.get(FlexibleTargeting.Field.interests, []):
                self.__try_add_interest_to_audience(data["interests"], interest)

        for interest in targeting.get(Targeting.Field.exclusions, {}).get(FlexibleTargeting.Field.interests, []):
            self.__try_add_interest_to_audience(data["excluded_interests"], interest)

    @staticmethod
    def __try_add_interest_to_audience(interests, interest):
        _interest = GraphAPISavedAudienceMapping.__get_interest(interest["id"])
        if _interest:
            interests.append(_interest)

    @staticmethod
    @lru_cache(maxsize=1024)  # TODO: this can be changed and extracted as a constant
    def __get_interest(interest_id):
        try:
            interest_obj = AbstractCrudObject()
            fb_api = interest_obj.get_api()
            interest = fb_api.call(method="GET", path=(interest_id,))
            return interest.json()
        except Exception as e:
            # Some interests might be removed from facebook
            logger.exception(repr(e))
            return None
