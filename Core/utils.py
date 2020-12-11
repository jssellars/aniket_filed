import humps


def snake_to_camelcase(data):
    if isinstance(data, list):
        camelcase = [{humps.camelize(key): value for key, value in entry.items()} for entry in data]
    else:
        camelcase = {humps.camelize(key): value for key, value in data.items()}

    return camelcase


DOT = "."
PLACEHOLDER = "__DOT__"


def key_has_dot(value):
    return isinstance(value, str) and value.find(DOT) > -1


def key_has_placeholder(value):
    return isinstance(value, str) and value.find(PLACEHOLDER)


def convert_key_dot_to_placeholder(value):
    if key_has_dot(value):
        return value.replace(DOT, PLACEHOLDER)
    else:
        return value


def convert_placeholder_to_key_dot(value):
    if key_has_placeholder(value):
        return value.replace(PLACEHOLDER, DOT)
    else:
        return value


def converter_dot_placeholder(obj, convert):
    """
    Recursively goes through the dictionary obj and replaces keys with the convert function.
    """
    if isinstance(obj, (str, int, float)):
        return obj
    if isinstance(obj, dict):
        new = obj.__class__()
        for k, v in obj.items():
            new[convert(k)] = converter_dot_placeholder(v, convert)
    elif isinstance(obj, (list, set, tuple)):
        new = obj.__class__(converter_dot_placeholder(v, convert) for v in obj)
    else:
        return obj
