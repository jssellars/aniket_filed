import typing

from marshmallow import INCLUDE, post_load

from Core.mapper import MapperBase


class LoggingCommandMapping(MapperBase):
    class Meta:
        unknown = INCLUDE

    @post_load
    def build(self, data: typing.Any, **kwargs):
        mapped_data = {
            'details': data
        }

        if self._target:
            return self._target(**mapped_data)
        else:
            return data
