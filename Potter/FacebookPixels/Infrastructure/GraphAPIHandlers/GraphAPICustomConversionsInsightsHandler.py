import typing

from facebook_business.adobjects.customconversion import CustomConversion

from Potter.FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIFields import GraphAPICustomConversionStatsFields
from Potter.FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelStatsDto import GraphAPIPixelStatsDto
from Potter.FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIPixelsInsightsHandler import \
    GraphAPIPixelsInsightsHandler
from Potter.FacebookPixels.Infrastructure.GraphAPIHandlers.Helpers import connect_to_graph_api_sdk
from Potter.FacebookPixels.Infrastructure.GraphAPIMappings.GraphAPICustomConversionStatsMapping import \
    GraphAPICustomConversionStatsMapping


class GraphAPICustomConversionsInsightsHandler(GraphAPIPixelsInsightsHandler):

    @classmethod
    def handle(cls, **kwargs) -> typing.List[GraphAPIPixelStatsDto]:
        _ = connect_to_graph_api_sdk(kwargs["business_owner_facebook_id"], kwargs["startup"])
        insights = cls.get_insights(custom_conversion_id=kwargs["facebook_id"],
                                    aggregation=kwargs["breakdown"],
                                    start_time=kwargs["start_time"],
                                    end_time=kwargs["end_time"])
        return insights

    @classmethod
    def get_insights(cls,
                     custom_conversion_id: typing.AnyStr = None,
                     aggregation: typing.AnyStr = None,
                     start_time: typing.AnyStr = None,
                     end_time: typing.AnyStr = None) -> typing.List[GraphAPIPixelStatsDto]:
        pixel = CustomConversion(fbid=custom_conversion_id)
        params = cls._build_get_stats_params(aggregation=aggregation, start_time=start_time, end_time=end_time)
        insights = pixel.get_stats(fields=GraphAPICustomConversionStatsFields.get_values(), params=params)

        insights_mapper = GraphAPICustomConversionStatsMapping(target=GraphAPIPixelStatsDto)
        insights = insights_mapper.load(insights, many=True)

        return insights
