import pandas as pd
from DbInstance import DbInstance


def id_to_string(x):
    if x is pd.np.nan:
        return x

    return str(x)


def percentage_to_float(x):
    if x is pd.np.nan:
        return x

    return float(x[:-1])


def id_to_location_name(x):
    if x is pd.np.nan:
        return x

    # TODO: refactor this
    return DbInstance.get_id_to_location_dict()[int(x)]

