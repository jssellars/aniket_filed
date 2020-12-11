import typing

from marshmallow import INCLUDE, fields, EXCLUDE, pre_load
from Core.Tools.Misc.EnumerationBase import EnumerationBase
from Core.Tools.Misc.ObjectSerializers import object_to_json
from Core.mapper import MappingBase, MapperBase
from FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPICustomConversionsInsightsHandler import (
    GraphAPICustomConversionsInsightsHandler,
)
from FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIPixelsInsightsHandler import GraphAPIPixelsInsightsHandler
from FacebookPixels.Infrastructure.GraphAPIHandlers.GraphAPIStandardEventsInsightsHandler import (
    GraphAPIStandardEventsInsightsHandler,
)


class LevelToGraphAPIPixelsInsightsHandler(EnumerationBase):
    PIXEL = GraphAPIPixelsInsightsHandler
    STANDARD_EVENT = GraphAPIStandardEventsInsightsHandler
    CUSTOM_CONVERSION = GraphAPICustomConversionsInsightsHandler


class PixelsInsightsCommandMapping(MappingBase):
    class Meta:
        unknown = INCLUDE


class PixelsInsightsLevel(EnumerationBase):
    PIXEL = "pixel"
    STANDARD_EVENT = "standardevent"
    CUSTOM_CONVERSION = "customconversion"


class PixelsInsightsResponseDtoMapping(MapperBase):
    breakdown = fields.String(allow_none=True)
    value = fields.String(allow_none=True)
    count = fields.Integer(allow_none=True)
    timestamp = fields.String(allow_none=True)

    class Meta:
        unknown = EXCLUDE

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.MutableMapping):
            data = object_to_json(data)

        if "aggregation" in data.keys():
            data["breakdown"] = data.pop("aggregation")

        if "start_time" in data.keys():
            data["timestamp"] = data.pop("start_time")

        return data
