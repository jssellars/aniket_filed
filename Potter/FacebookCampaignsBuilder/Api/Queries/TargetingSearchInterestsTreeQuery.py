import typing

from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchBaseQuery import TargetingSearchBaseQuery
from Potter.FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIInterestsHandler import \
    GraphAPIInterestsHandler


class TargetingSearchInterestsTreeQuery(TargetingSearchBaseQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            results = handler.interests
        except Exception as e:
            raise e

        return results
