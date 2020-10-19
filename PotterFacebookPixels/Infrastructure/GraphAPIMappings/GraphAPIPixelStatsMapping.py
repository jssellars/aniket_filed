import typing

from marshmallow import INCLUDE, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from PotterFacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelStatsDto import GraphAPIPixelStatsDataDto


class GraphAPIPixelStatsMapping(MapperBase):
    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.Dict):
            data = Tools.convert_to_json(data)

        if "data" in data.keys():
            data["data"] = [GraphAPIPixelStatsDataDto(**entry) for entry in data["data"]]

        return data
