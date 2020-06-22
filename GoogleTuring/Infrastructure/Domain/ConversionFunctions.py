from GoogleTuring.Infrastructure.PersistenceLayer.MongoIdToNameCache import MongoIdToNameCache


def id_to_string(x):
    if x is None:
        return x

    return str(x)


def percentage_to_float(x):
    if x is None:
        return x

    return float(x[:-1])


def money_conversion(x):
    if x is None:
        return x

    return float('{:.2f}'.format(round(x / 1_000_000, 2)))


def id_to_location_name(x):
    if x is None:
        return x

    return MongoIdToNameCache.id_to_name_cache[int(x)]
