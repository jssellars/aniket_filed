import pandas as pd
from GoogleTuring.Infrastructure.PersistanceLayer.MongoIdToNameCache import MongoIdToNameCache


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

    return MongoIdToNameCache.id_to_name_cache[int(x)]

