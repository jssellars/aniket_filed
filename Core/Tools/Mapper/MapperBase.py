import typing
from inspect import isfunction

from marshmallow import Schema, post_load, fields, pre_load, EXCLUDE, INCLUDE

from Core.Tools.Misc.ObjectSerializers import object_to_json


class MapperNestedField(fields.Field):
    def __init__(self, target: typing.Any = None, **kwargs):
        super().__init__(**kwargs)
        self._target = target

    def _convert_to_object(self, value: typing.Any) -> typing.Any:
        if isinstance(value, list):
            return [self._target(**entry) for entry in value]
        else:
            return self._target(**value)

    def _deserialize(self, value: typing.Any, attr: str, data: typing.Any, **kwargs):
        if not self._target:
            return value
        else:
            return self._convert_to_object(value)

    def _serialize(self, value: typing.Any, attr: str, data: typing.Any, **kwargs):
        if not self._target:
            return value
        else:
            return object_to_json(value)


class MapperBase(Schema):
    def __init__(self, target: typing.Any = None, **kwargs):
        super().__init__(**kwargs)
        self._target = target

    @pre_load
    def convert(self, data: typing.Any, **kwargs):
        """Implement a version of a preload function for each mapping
        whereby you define any custom mapping between input and model"""
        if not isinstance(data, typing.MutableMapping):
            return object_to_json(data)
        else:
            return data

    @post_load
    def build(self, data: typing.Any, **kwargs):
        if self._target:
            return self._target(**data)
        else:
            return data

    def _remove_unknown_data(self, data):
        if self._target:
            required_fields = self._target().__dict__.keys()
            data = {key: data.get(key) for key in required_fields}

        return data


class MappingBase(MapperBase):
    # todo: needs testing. Not sure about initializing Meta properties from self
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self._target:
            input_fields = [attribute for attribute in dir(self._target) if not callable(getattr(self._target, attribute)) and not isfunction(getattr(self._target, attribute)) and not attribute.startswith('__')]
            self.Meta.fields = input_fields

    class Meta:
        unknown = INCLUDE
