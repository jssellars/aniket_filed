dot = "."
placeholder = "__DOT__"


def key_has_dot(value):
    return isinstance(value, str) and value.find(dot) > -1


def key_has_placeholder(value):
    return isinstance(value, str) and value.find(placeholder)


def convert_key_dot_to_placeholder(value):
    if key_has_dot(value):
        return value.replace(dot, placeholder)
    else:
        return value


def convert_placeholder_to_key_dot(value):
    if key_has_placeholder(value):
        return value.replace(placeholder, dot)
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
    return new
