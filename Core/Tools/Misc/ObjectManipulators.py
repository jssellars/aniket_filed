from inspect import isfunction


def extract_class_attributes_values(obj):
    attributes_values = [getattr(obj, attribute) for attribute in dir(obj) if not callable(getattr(obj, attribute)) and not isfunction(getattr(obj, attribute)) and not attribute.startswith('__')]

    return attributes_values


def extract_class_attributes(obj):
    attributes = [attribute for attribute in dir(obj) if not callable(getattr(obj, attribute)) and not isfunction(getattr(obj, attribute)) and not attribute.startswith('__')]

    return attributes
