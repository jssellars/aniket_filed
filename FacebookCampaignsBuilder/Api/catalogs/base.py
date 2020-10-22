from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values


class Base:
    def to_json(self):
        return [i.to_json() if hasattr(i, "to_json") else i for i in extract_class_attributes_values(self)]
