import typing
from queue import Queue
from threading import Thread
from typing import Dict, List

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.InterestsTreeMapping import map_interests
from Core.Web.FacebookGraphAPI.Tools import Tools
from facebook_business.adobjects.targetingsearch import TargetingSearch


# TODO: add all graph api search related classes here
class GraphAPICountryGroupsLegend:
    __maximum_results = int(1e6)
    _location_search_types = ["country", "country_group", "region", "geo_market", "city", "zip", "electoral_district"]

    __continents = [
        "africa",
        "asia",
        "caribbean",
        "central_america",
        "europe",
        "north_america",
        "oceania",
        "south_america",
        "worldwide",
    ]
    __free_trade_areas = ["afta", "mercosur", "cisfta", "eea", "nafta", "gcc", "apec"]
    __app_store_regions = ["android_free_store", "android_paid_store", "itunes_app_store"]
    __emerging_markets = ["emerging_markets"]
    __euro_area = ["euro_area"]

    _country_groups_legend = {
        "continent": __continents,
        "free_trade_areas": __free_trade_areas,
        "app_store_regions": __app_store_regions,
        "emerging_markets": __emerging_markets,
        "euro_area": __euro_area,
    }

    __countries = None
    __regions = None
    __geo_markets = None
    __electoral_districts = None

    def __init__(self, graph_api_sdk=None):
        self.__graph_api_sdk = graph_api_sdk

    @property
    def countries(self):
        if not self.__countries:
            self.__countries = self._search(query_string="", location_types="country")
        return self.__countries

    @property
    def regions(self):
        if not self.__regions:
            self.__regions = self._search(query_string="", location_types="region")
        return self.__regions

    @property
    def geo_markets(self):
        if not self.__geo_markets:
            self.__geo_markets = self._search(query_string="", location_types="geo_market")
        return self.__geo_markets

    @property
    def electoral_districts(self):
        if not self.__electoral_districts:
            self.__electoral_districts = self._search(query_string="", location_types="electoral_district")
        return self.__electoral_districts

    def _search(self, query_string="", search_type=None, location_types=None, limit=None):
        if isinstance(search_type, str):
            search_type = search_type.strip(" ").split(",")
        elif not search_type:
            search_type = TargetingSearch.TargetingSearchTypes.geolocation
        if not location_types:
            location_types = self._location_search_types
        if not limit:
            limit = self.__maximum_results

        params = {"q": query_string, "type": search_type, "location_types": location_types, "limit": limit}
        try:
            results = TargetingSearch.search(params=params)
            results = [Tools.convert_to_json(result) for result in results]
        except Exception as e:
            raise e

        return results


class GraphAPILocationsHandler(GraphAPICountryGroupsLegend):
    __search_results = 50
    __default_type = ["country_group"]
    __all_types = ["country", "country_group", "region", "geo_market", "electoral_district"]

    def __init__(self, graph_api_sdk: GraphAPISdkBase = None):
        super().__init__(graph_api_sdk)

    def get_country_groups(self) -> typing.List[typing.Dict]:
        country_groups = self._search(query_string="", location_types="country_group")
        country_groups = [self.__append_countries_names(country_group) for country_group in country_groups]
        country_groups = [self.__add_region(country_group) for country_group in country_groups]
        return country_groups

    def __add_region(self, country_group: typing.Dict) -> typing.Dict:
        for region in self._country_groups_legend.keys():
            if country_group["key"] in self._country_groups_legend[region]:
                country_group["region"] = region
                break
        return country_group

    def __append_countries_names(self, country_group: typing.Dict) -> typing.Dict:
        countries = dict()
        for entry in country_group["country_codes"]:
            country = self.__find_country_by_code(entry)
            if country:
                countries[country["key"]] = country["name"]
        country_group["country_codes"] = countries
        country_group["geolocation_type"] = country_group.pop("type")
        return country_group

    def __find_country_by_code(self, country_code: typing.AnyStr = None) -> typing.Dict:
        return next(filter(lambda x: x.get("key") == country_code, self.countries), None)

    def search_location(self, query_string: typing.AnyStr = None):
        responses = []
        threads = []
        queue = Queue()
        for location_type in self._location_search_types:
            t = Thread(
                target=lambda q, arg1, arg2, arg3: q.put(
                    self._search(query_string=arg1, location_types=[arg2], limit=arg3)
                ),
                args=(queue, query_string.lower(), location_type, self.__search_results),
            )
            threads.append(t)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        if queue.not_empty:
            responses = [entry for element in queue.queue for entry in element]
        return responses


class GraphAPILanguagesHandler:
    __max_results = int(1e6)
    __params = {"q": "", "type": "adlocale", "limit": __max_results}

    def __init__(self, graph_api_sdk: GraphAPISdkBase = None):
        self.__graph_api_sdk = graph_api_sdk

    def get_all(self):
        results = TargetingSearch.search(params=self.__params)
        languages = [Tools.convert_to_json(result) for result in results]
        return languages


class GraphAPIInterestsHandler:
    __maximum_results = int(1e6)
    __maximum_search_results = 500

    __interest_search_type = [
        TargetingSearch.TargetingSearchTypes.education,
        TargetingSearch.TargetingSearchTypes.major,
        TargetingSearch.TargetingSearchTypes.interest,
        TargetingSearch.TargetingSearchTypes.employer,
        TargetingSearch.TargetingSearchTypes.position,
    ]

    def __init__(self, graph_api_sdk: GraphAPISdkBase = None):
        self.__graph_api_sdk = graph_api_sdk
        self.__interests = None

    @property
    def interests(self) -> Dict[str, Dict]:
        if not self.__interests:
            self.__interests = self.__get_raw_interests()
            self.__interests = {interest["id"]: interest for interest in self.__interests if "id" in interest}

        return self.__interests

    def get_regulated_interests(self, regulated_categories: List[str] = None) -> List[Dict]:
        params = {"type": "adTargetingCategory", "class": "interests", "regulated_categories": regulated_categories}

        results = TargetingSearch.search(params=params)
        results = [Tools.convert_to_json(result) for result in results]

        return results

    def __get_raw_interests(self):
        params = {
            "class": "interests",
            "type": "adinterest",
            "limit": self.__maximum_search_results,
        }

        results = TargetingSearch.search(params=params)
        results = [Tools.convert_to_json(result) for result in results]

        return results

    def search_interest(self, query_string="", search_type=None):
        params = {
            "q": query_string,
            "type": TargetingSearch.TargetingSearchTypes.interest,
            "limit": self.__maximum_search_results,
        }
        results = TargetingSearch.search(params=params)
        results = self.__map_interests(results)
        return results

    def __map_interests(self, raw_interests=None):
        for index, _ in enumerate(raw_interests):
            raw_interests[index] = Tools.convert_to_json(raw_interests[index])
            path = raw_interests[index].get("path")
            if path:
                raw_interests[index]["type"] = "_".join(path[0].lower().split(" "))
        return raw_interests

    # TODO: check if we still need this endpoint
    def suggest_interests(self, source_interests=None):
        if not source_interests:
            source_interests = []

        params = {
            "interest_list": source_interests,
            "type": TargetingSearch.TargetingSearchTypes.interest_suggestion,
            "limit": self.__maximum_search_results,
        }

        results = TargetingSearch.search(params=params)
        results = [Tools.convert_to_json(result) for result in results]
        mapped_interests = map_interests(results)
        return mapped_interests
