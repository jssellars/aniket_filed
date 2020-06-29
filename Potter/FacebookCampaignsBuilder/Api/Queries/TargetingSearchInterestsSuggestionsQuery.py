import typing
import urllib.parse

from Potter.FacebookCampaignsBuilder.Api.Queries.TargetingSearchBaseQuery import TargetingSearchBaseQuery
from Potter.FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIInterestsHandler import \
    GraphAPIInterestsHandler


class TargetingSearchInterestsSuggestionsQuery(TargetingSearchBaseQuery):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def search(self, query_string: typing.AnyStr = None) -> typing.List[typing.Dict]:
        try:
            source_interests = urllib.parse.unquote(query_string)
            source_interests = source_interests.replace('&', '')
            source_interests = [i.title() for i in source_interests.split(',')]

            handler = GraphAPIInterestsHandler(graph_api_sdk=self._graph_api_sdk)
            results = handler.suggest_interests(source_interests=source_interests)
        except Exception as e:
            raise e

        return results
