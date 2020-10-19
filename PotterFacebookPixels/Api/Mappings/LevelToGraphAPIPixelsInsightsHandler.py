from Core.Tools.Misc.EnumerationBase import EnumerationBase
from PotterFacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPICustomConversionsInsightsHandler import \
    GraphAPICustomConversionsInsightsHandler
from PotterFacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIPixelsInsightsHandler import \
    GraphAPIPixelsInsightsHandler
from PotterFacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIStandardEventsInsightsHandler import \
    GraphAPIStandardEventsInsightsHandler


class LevelToGraphAPIPixelsInsightsHandler(EnumerationBase):
    PIXEL = GraphAPIPixelsInsightsHandler
    STANDARD_EVENT = GraphAPIStandardEventsInsightsHandler
    CUSTOM_CONVERSION = GraphAPICustomConversionsInsightsHandler
