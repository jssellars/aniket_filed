import typing

from marshmallow import INCLUDE, pre_load

from Core.Tools.Mapper.MapperBase import MapperBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from Potter.FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppEventTypeDto import GraphAPIAppEventTypeDto
from Potter.FacebookApps.Infrastructure.GraphAPIDtos.GraphAPIAppFields import GraphAPIAppFields


class GraphAPIAppMapping(MapperBase):
    class Meta:
        unknown = INCLUDE

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        if not isinstance(data, typing.Dict):
            data = Tools.convert_to_json(data)

        if GraphAPIAppFields.APP_EVENT_TYPES.value in data.keys():
            data[GraphAPIAppFields.APP_EVENT_TYPES.value] = [GraphAPIAppEventTypeDto(**entry)
                                                             for entry in
                                                             data[GraphAPIAppFields.APP_EVENT_TYPES.value]]

        return data
