import typing

from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchBaseQuery import TargetingSearchBaseQuery
from Potter.FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIInterestsHandler import \
    GraphAPIInterestsHandler


class TargetingSearchRegulatedInterestsQuery(TargetingSearchBaseQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, regulated_categories: typing.List[typing.AnyStr] = None) -> typing.List[typing.Dict]:
        try:
            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            results = handler.get_regulated_interests(regulated_categories=regulated_categories)
        except Exception as e:
            raise e

        return results
