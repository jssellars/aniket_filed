import json
from dataclasses import dataclass


@dataclass
class QueueDetails:
    name: str = None
    key: str = None


@dataclass
class ExchangeDetails:
    name: str = None
    type: str = None
    inbound_queue: QueueDetails = None
    outbound_queue: QueueDetails = None


class BaseConfig(object):

    def __init__(self, input_dict):
        if isinstance(input_dict, str):
            try:
                input_dict = json.loads(input_dict)
            except json.decoder.JSONDecodeError:
                with open(input_dict, 'r') as aDictJson:
                    input_dict = json.load(aDictJson)

        self.from_dict(input_dict)

    def from_dict(self, input_dict):
        self.__dict__ = {}
        for key, value in input_dict.items():
            self.__dict__[key] = value

    def to_dict(self):
        output_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, BaseConfig):
                value = value.to_dict()
            output_dict[key] = value
        return output_dict

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def get_property(self, property_name):
        if property_name not in self.__dict__.keys():
            return None
        return self.__dict__[property_name]
