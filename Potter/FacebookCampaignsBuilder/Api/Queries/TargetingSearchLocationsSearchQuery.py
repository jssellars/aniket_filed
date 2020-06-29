import typing

from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchBaseQuery import TargetingSearchBaseQuery
from Potter.FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPILocationsHandler import \
    GraphAPILocationsHandler


class TargetingSearchLocationsSearchQuery(TargetingSearchBaseQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, query_string: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPILocationsHandler(graph_api_sdk=self._graph_api_sdk)
            results = handler.search_location(query_string=query_string)
        except Exception as e:
            raise e

        return results
