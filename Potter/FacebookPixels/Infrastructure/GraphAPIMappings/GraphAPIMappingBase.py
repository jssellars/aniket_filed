import typing
from marshmallow import INCLUDE, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools


class GraphAPIMappingBase(MapperBase):
    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.Dict):
            return Tools.convert_to_json(data)
        else:
            return data


class GraphAPIPixelCustomAudienceMapping(GraphAPIMappingBase):
    pass


class GraphAPIPixelDAChecksMapping(GraphAPIMappingBase):
    pass

