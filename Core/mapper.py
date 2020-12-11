import typing
from inspect import isfunction

from marshmallow import Schema, post_load, fields, pre_load, INCLUDE

from Core.Tools.Misc.ObjectSerializers import object_to_json


class MapperNestedField(fields.Field):
    def __init__(self, target: typing.Any = None, **kwargs):
        super().__init__(**kwargs)
        self._target = target

    def _convert_to_object(self, value: typing.Any) -> typing.Any:
        return [self._target(**entry) for entry in value] if isinstance(value, list) else self._target(**value)

    def _deserialize(self, value: typing.Any, attr: str, data: typing.Any, **kwargs):
        return self._convert_to_object(value) if self._target else value

    def _serialize(self, value: typing.Any, attr: str, data: typing.Any, **kwargs):
        return object_to_json(value) if self._target else value


class MapperBase(Schema):
    def __init__(self, target: typing.Any = None, **kwargs):
        super().__init__(**kwargs)
        self._target = target

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        """Implement a version of a preload function for each mapping
        whereby you define any custom mapping between input and model"""
        return data if isinstance(data, typing.MutableMapping) else object_to_json(data)

    @post_load
    def build(self, data: typing.Any, **kwargs):
        return self._target(**data) if self._target else data

    def _remove_unknown_data(self, data):
        if self._target:
            required_fields = self._target().__dict__.keys()
            data = {key: data.get(key) for key in required_fields}

        return data


class MappingBase(MapperBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self._target:
            self.Meta.fields = [
                attribute
                for attribute in dir(self._target)
                if not callable(getattr(self._target, attribute))
                and not isfunction(getattr(self._target, attribute))
                and not attribute.startswith("__")
            ]

    class Meta:
        unknown = INCLUDE
