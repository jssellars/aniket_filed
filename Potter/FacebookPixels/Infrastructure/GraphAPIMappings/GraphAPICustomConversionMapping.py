import typing
from marshmallow import INCLUDE, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from Potter.FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import BusinessDto
from Potter.FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPICustomConversionDto import DataSourcesDto


class GraphAPICustomConversionMapping(MapperBase):
    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.Dict):
            data = Tools.convert_to_json(data)

        if "business" in data.keys():
            data["business"] = BusinessDto(**data["business"])

        if "data_sources" in data.keys():
            data["data_sources"] = [DataSourcesDto(**entry) for entry in data["data_sources"]]

        if "pixel" in data.keys():
            pixel = data.pop("pixel")
            data["pixel_id"] = pixel["id"]

        return data
