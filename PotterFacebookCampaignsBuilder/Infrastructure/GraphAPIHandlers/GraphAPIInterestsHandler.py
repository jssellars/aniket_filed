import typing

from facebook_business.adobjects.targetingsearch import TargetingSearch

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from PotterFacebookCampaignsBuilder.Infrastructure.Mappings.InterestsTreeMapping import map_interests


class GraphAPIInterestsHandler:
    __maximum_results = int(1e6)
    __maximum_search_results = 500

    __interest_search_type = [TargetingSearch.TargetingSearchTypes.education,
                              TargetingSearch.TargetingSearchTypes.major,
                              TargetingSearch.TargetingSearchTypes.interest,
                              TargetingSearch.TargetingSearchTypes.employer,
                              TargetingSearch.TargetingSearchTypes.position]

    def __init__(self, graph_api_sdk: GraphAPISdkBase = None):
        self.__graph_api_sdk = graph_api_sdk
        self.__interests = None

    @property
    def interests(self):
        if not self.__interests:
            self.__interests = self.__get_raw_interests()
            self.__interests = map_interests(self.__interests)
        return self.__interests

    def get_regulated_interests(self,
                                regulated_categories: typing.List[typing.AnyStr] = None) -> typing.List[typing.Dict]:
        params = {
            'type': 'adTargetingCategory',
            'class': 'interests',
            'regulated_categories': regulated_categories
        }

        results = TargetingSearch.search(params=params)
        results = [Tools.convert_to_json(result) for result in results]

        return results

    def __get_raw_interests(self, browse_category=None):
        params = {
            'type': 'adTargetingCategory',
            'class': browse_category,
            'limit': self.__maximum_results
        }

        results = TargetingSearch.search(params=params)
        results = [Tools.convert_to_json(result) for result in results]

        return results

    def search_interest(self, query_string='', search_type=None):
        params = {
            'q': query_string,
            'type': TargetingSearch.TargetingSearchTypes.interest,
            'limit': self.__maximum_search_results
        }
        results = TargetingSearch.search(params=params)
        results = self.__map_interests(results)
        return results

    def __map_interests(self, raw_interests=None):
        for index, _ in enumerate(raw_interests):
            raw_interests[index] = Tools.convert_to_json(raw_interests[index])
            path = raw_interests[index].get('path')
            if path:
                raw_interests[index]['type'] = "_".join(path[0].lower().split(" "))
        return raw_interests

    def suggest_interests(self, source_interests=None):
        if not source_interests:
            source_interests = []

        params = {
            'interest_list': source_interests,
            'type': TargetingSearch.TargetingSearchTypes.interest_suggestion,
            'limit': self.__maximum_search_results
        }

        results = TargetingSearch.search(params=params)
        results = [Tools.convert_to_json(result) for result in results]
        mapped_interests = map_interests(results)
        return mapped_interests
