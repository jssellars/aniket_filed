import typing

from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchBaseQuery import TargetingSearchBaseQuery
from Potter.FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPILocationsHandler import \
    GraphAPILocationsHandler


class TargetingSearchLocationsCountryGroupsQuery(TargetingSearchBaseQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPILocationsHandler(graph_api_sdk=self._graph_api_sdk)
            results = handler.get_country_groups()
        except Exception as e:
            raise e
        return results
