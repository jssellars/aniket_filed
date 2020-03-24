import json

class BaseConfig(object):

    def __init__(self, aDict):
        if isinstance(aDict, str):
            try:
                aDict = json.loads(aDict)
            except json.decoder.JSONDecodeError:
                with open(aDict, 'r') as aDictJson:
                    aDict = json.load(aDictJson)

        self.from_dict(aDict)

    def from_dict(self, aDict):
        self.__dict__ = {}
        for key, value in aDict.items():
            self.__dict__[key] = value

    def to_dict(self):
        output_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Config):
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

