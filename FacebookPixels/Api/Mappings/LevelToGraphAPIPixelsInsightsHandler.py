from Core.Tools.Misc.EnumerationBase import EnumerationBase
from FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPICustomConversionsInsightsHandler import \
    GraphAPICustomConversionsInsightsHandler
from FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIPixelsInsightsHandler import \
    GraphAPIPixelsInsightsHandler
from FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIStandardEventsInsightsHandler import \
    GraphAPIStandardEventsInsightsHandler


class LevelToGraphAPIPixelsInsightsHandler(EnumerationBase):
    PIXEL = GraphAPIPixelsInsightsHandler
    STANDARD_EVENT = GraphAPIStandardEventsInsightsHandler
    CUSTOM_CONVERSION = GraphAPICustomConversionsInsightsHandler
