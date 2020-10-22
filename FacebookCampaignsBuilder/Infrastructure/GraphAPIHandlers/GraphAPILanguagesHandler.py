from facebook_business.adobjects.targetingsearch import TargetingSearch

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPILanguagesHandler:
    __max_results = int(1e6)
    __params = {
        'q': '',
        'type': 'adlocale',
        'limit': __max_results
    }

    def __init__(self, graph_api_sdk: GraphAPISdkBase = None):
        self.__graph_api_sdk = graph_api_sdk

    def get_all(self):
        results = TargetingSearch.search(params=self.__params)
        languages = [Tools.convert_to_json(result) for result in results]
        return languages
