from marshmallow import INCLUDE

from Core.mapper import MappingBase


class PixelsInsightsCommandMapping(MappingBase):
    class Meta:
        unknown = INCLUDE
