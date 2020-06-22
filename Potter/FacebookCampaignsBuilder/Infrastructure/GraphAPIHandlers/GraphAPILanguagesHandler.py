import typing

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

    def __init__(self, facebook_config: typing.Any = None, permanent_token=None):
        self.__graph_api_sdk = GraphAPISdkBase(facebook_config=facebook_config,
                                               business_owner_permanent_token=permanent_token)

    def get_all(self):
        results = TargetingSearch.search(api=self.__graph_api_sdk,
                                         params=self.__params)
        languages = [Tools.convert_to_json(result) for result in results]
        return languages
