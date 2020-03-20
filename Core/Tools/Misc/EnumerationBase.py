from enum import Enum


class EnumerationBase(Enum):

    @classmethod
    def get_values(cls):
        return list(map(lambda v: v.value.lower(), cls))

    @classmethod
    def get_names(cls):
        return list(map(lambda v: v.name.lower(), cls))

    @classmethod
    def get_by_value(cls, value):
        match = next(filter(lambda x: x.value == value, cls), None)
        return match.name if match else None

    @classmethod
    def get_by_name(cls, name):
        match = next(filter(lambda x: x.name.lower() == name, cls))
        return match.value if match else None

    @classmethod
    def get_enum_by_name(cls, name):
        match = next(filter(lambda x: x.name == name, cls))
        return match if match else None

    @classmethod
    def get_enum_by_value(cls, value):
        match = next(filter(lambda x: x.value == value, cls), None)
        return match if match else None