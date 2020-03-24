from Packages.Tools.ConvertToJsonBase import ConvertToJsonBase
from Packages.Tools.ObjectManipulators import extract_class_attributes


class EnumerationBase(ConvertToJsonBase):

    def from_display_name(self, display_name):
        attributes = extract_class_attributes(self)
        for attribute in attributes:
            if getattr(self, attribute).display_name == display_name:
                return getattr(self, attribute)


class Enumeration(ConvertToJsonBase):
    def __init__(self, id=None, name=None, display_name=None):
        self.id = id
        self.name = name
        self.display_name = display_name

    def to_string(self):
        return self.name
