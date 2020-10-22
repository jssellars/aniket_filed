from marshmallow import INCLUDE

from Core.Tools.Mapper.MapperBase import MappingBase


class PixelsInsightsCommandMapping(MappingBase):
    class Meta:
        unknown = INCLUDE
