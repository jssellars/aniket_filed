import json

from Packages.Tools.ObjectEncoder import ObjectEncoder


class ConvertToJsonBase:

    def to_json(self):
        object_json = json.dumps(self, cls=ObjectEncoder)
        return object_json

    def to_dict(self):
        object_dict = json.loads(self.to_json())
        return object_dict

    def to_attribute_values_list(self):
        object_dict = json.loads(self.to_json())
        return [value for _, value in object_dict.items()]