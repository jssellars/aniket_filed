import typing

from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchBaseQuery import TargetingSearchBaseQuery
from Potter.FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIInterestsHandler import \
    GraphAPIInterestsHandler


class TargetingSearchInterestsSearchQuery(TargetingSearchBaseQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, query_string: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            results = handler.search_interest(query_string=query_string)
        except Exception as e:
            raise e

        return results
