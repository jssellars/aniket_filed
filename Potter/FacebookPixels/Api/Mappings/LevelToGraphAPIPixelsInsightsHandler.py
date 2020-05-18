from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Potter.FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPICustomConversionsInsightsHandler import \
    GraphAPICustomConversionsInsightsHandler
from Potter.FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIPixelsInsightsHandler import \
    GraphAPIPixelsInsightsHandler
from Potter.FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIStandardEventsInsightsHandler import \
    GraphAPIStandardEventsInsightsHandler


class LevelToGraphAPIPixelsInsightsHandler(EnumerationBase):
    PIXEL = GraphAPIPixelsInsightsHandler
    STANDARD_EVENT = GraphAPIStandardEventsInsightsHandler
    CUSTOM_CONVERSION = GraphAPICustomConversionsInsightsHandler
