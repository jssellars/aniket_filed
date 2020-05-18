import json


class ClassGenerator:

    def __init__(self, dict_input=None):
        if dict_input:
            if isinstance(dict_input, str):
                try:
                    dict_input = json.loads(dict_input)
                except json.decoder.JSONDecodeError:
                    with open(dict_input, 'r') as dict_inputJson:
                        dict_input = json.load(dict_inputJson)

            self.from_dict(dict_input)

    def from_dict(self, dict_input):
        self.__dict__ = {}
        for key, value in dict_input.items():
            self.__dict__[key] = value

    def to_dict(self):
        output_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ClassGenerator):
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
