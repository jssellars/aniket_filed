import typing

from marshmallow import INCLUDE, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from Potter.FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import BusinessDto
from Potter.FacebookPixels.Infrastructure.GraphAPIDtos.GraphAPIPixelDto import CreatorDto, AdAccountDto


class GraphAPIPixelMapping(MapperBase):
    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.Dict):
            data = Tools.convert_to_json(data)

        if "creator" in data.keys():
            data["creator"] = CreatorDto(**data["creator"])

        if "owner_ad_account" in data.keys():
            data["owner_ad_account"] = AdAccountDto(**data["owner_ad_account"])

        if "owner_business" in data.keys():
            data["owner_business"] = BusinessDto(**data["owner_business"])

        return data
