import json


class BaseConfig:
    def __init__(self, input_dict):
        if isinstance(input_dict, str):
            try:
                input_dict = json.loads(input_dict)
            except json.decoder.JSONDecodeError:
                with open(input_dict) as file:
                    input_dict = json.load(file)

        self.__dict__ = input_dict

    def to_dict(self):
        return {k: v.to_dict() if isinstance(v, BaseConfig) else v for k, v in self.__dict__.items()}

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def get_property(self, property_name):
        return self.__dict__.get(property_name)
