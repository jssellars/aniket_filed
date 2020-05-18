import typing

from facebook_business.adobjects.adspixelstatsresult import AdsPixelStatsResult

from Potter.FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelStatsDto import GraphAPIPixelStatsDto
from Potter.FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIPixelsInsightsHandler import \
    GraphAPIPixelsInsightsHandler
from Potter.FacebookPixels.Infrastructure.GraphAPIHandlers.Helpers import connect_to_graph_api_sdk


class GraphAPIStandardEventsInsightsHandler(GraphAPIPixelsInsightsHandler):

    @classmethod
    def handle(cls, facebook_name: typing.AnyStr = None, **kwargs) -> typing.List[GraphAPIPixelStatsDto]:

        if kwargs["breakdown"] != AdsPixelStatsResult.Aggregation.event:
            raise ValueError("Invalid breakdown. For standard events, use 'event' breakdown value")

        _ = connect_to_graph_api_sdk(kwargs["business_owner_facebook_id"], kwargs["startup"])
        insights = cls.get_insights(pixel_id=kwargs["facebook_id"],
                                    aggregation=kwargs["breakdown"],
                                    start_time=kwargs["start_time"],
                                    end_time=kwargs["end_time"])

        return cls.__filter_insights_by_event_name(facebook_name, insights)

    @staticmethod
    def __filter_insights_by_event_name(event_name: typing.AnyStr = None,
                                        insights: typing.List[GraphAPIPixelStatsDto] = None) -> typing.List[
        GraphAPIPixelStatsDto]:
        for index, insight in enumerate(insights):
            event_insights = [event for event in insight.data if event.value == event_name]
            insights[index].data = event_insights

        return insights
