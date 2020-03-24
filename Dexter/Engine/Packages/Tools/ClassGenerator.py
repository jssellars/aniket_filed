import json


class ClassGenerator:
    
    def __init__(self, a_dict=None):
        if a_dict:
            if isinstance(a_dict, str):
                try:
                    a_dict = json.loads(a_dict)
                except json.decoder.JSONDecodeError:
                    with open(a_dict, 'r') as aDictJson:
                        a_dict = json.load(aDictJson)

            self.from_dict(a_dict)

    def from_dict(self, aDict):
        self.__dict__ = {}
        for key, value in aDict.items():
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
