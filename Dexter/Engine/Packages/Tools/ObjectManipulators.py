from inspect import isfunction


def extract_class_attributes_values(an_object):
    attributes_values = [getattr(an_object, attribute) for attribute in dir(an_object) if
                         not callable(getattr(an_object, attribute)) and not isfunction(getattr(an_object, attribute)) and not attribute.startswith('__')]

    return attributes_values


def extract_class_attributes(an_object):
    attributes = [attribute for attribute in dir(an_object) if
                  not callable(getattr(an_object, attribute)) and not isfunction(getattr(an_object, attribute)) and not attribute.startswith('__')]

    return attributes
#
