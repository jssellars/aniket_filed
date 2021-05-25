from enum import Enum


def id_to_string(x):
    if x is None:
        return x

    return str(x)


def float_to_percentage(x):
    if x is None:
        return x

    return float("{:.2f}".format(round(x * 100, 2)))


def money_conversion(x):
    if x is None:
        return x

    return float("{:.2f}".format(round(x / 1_000_000, 2)))


def round_float(x):
    if x is None:
        return x

    return float(round(x, 2))


def enum_to_string(x: Enum):
    if x is None:
        return x

    return x.name.capitalize()
