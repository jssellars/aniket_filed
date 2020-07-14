from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from Core.Tools.Misc.ObjectSerializers import object_to_json


class CatalogBase:

    def to_json(self):
        items = extract_class_attributes_values(self)

        return [item.to_json() if hasattr(item, 'to_json') else item for item in items]

