import typing

from facebook_business.adobjects.adspixel import AdsPixel

from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIFields import GraphAPIPixelStatsFields
from FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelStatsDto import GraphAPIPixelStatsDto
from FacebookPixels.Infrastructure.GraphAPIHandlers.Helpers import connect_to_graph_api_sdk
from FacebookPixels.Infrastructure.GraphAPIMappings.GraphAPIPixelStatsMapping import GraphAPIPixelStatsMapping


class GraphAPIPixelsInsightsHandler:

    @classmethod
    def handle(cls,
               business_owner_facebook_id: typing.AnyStr = None,
               facebook_id: typing.AnyStr = None,
               breakdown: typing.AnyStr = None,
               start_time: typing.AnyStr = None,
               end_time: typing.AnyStr = None,
               config: typing.Any = None,
               fixtures: typing.Any = None,
               **kwargs) -> typing.List[GraphAPIPixelStatsDto]:
        connect_to_graph_api_sdk(business_owner_facebook_id, config, fixtures)
        return cls.get_insights(pixel_id=facebook_id, aggregation=breakdown, start_time=start_time, end_time=end_time)

    @classmethod
    def get_insights(cls,
                     pixel_id: typing.AnyStr = None,
                     aggregation: typing.AnyStr = None,
                     start_time: typing.AnyStr = None,
                     end_time: typing.AnyStr = None) -> typing.List[GraphAPIPixelStatsDto]:
        pixel = AdsPixel(fbid=pixel_id)
        params = cls._build_get_stats_params(aggregation=aggregation, start_time=start_time, end_time=end_time)
        insights = pixel.get_stats(fields=GraphAPIPixelStatsFields.get_values(), params=params)

        insights_mapper = GraphAPIPixelStatsMapping(target=GraphAPIPixelStatsDto)
        insights = insights_mapper.load(insights, many=True)

        return insights

    @staticmethod
    def _build_get_stats_params(aggregation: typing.AnyStr = None,
                                start_time: typing.AnyStr = None,
                                end_time: typing.AnyStr = None) -> typing.Dict:
        return {
            "aggregation": aggregation,
            "start_time": start_time,
            "end_time": end_time
        }
