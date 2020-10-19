import typing

from marshmallow import fields, pre_load, EXCLUDE

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Tools.Misc.ObjectSerializers import object_to_json


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
