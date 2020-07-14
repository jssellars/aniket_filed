import typing
from dataclasses import dataclass

import humps

from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from Core.Tools.Misc.ObjectSerializers import object_to_json


@dataclass
class CatalogNode:
    key: typing.AnyStr = None
    display_name: typing.AnyStr = None
    image_name: typing.AnyStr = None
    description: typing.AnyStr = None
    children: typing.List = None

    def to_json(self):
        json = {}
        for k, v in self.__dict__.items():
            if v is None:
                continue

            if isinstance(v, CatalogNode):
                json[humps.camelize(k)] = v.to_json()
                continue

            if isinstance(v, typing.List):
                json[humps.camelize(k)] = [x.to_json() for x in v]
                continue

            json[humps.camelize(k)] = v
        return json

