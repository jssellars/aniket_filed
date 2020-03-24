import dataclasses


def dataclass_from_dict(target_class, source_dict):
    try:
        fieldtypes = {f.name: f.type for f in dataclasses.fields(target_class)}
        return target_class(**{f: dataclass_from_dict(fieldtypes[f], source_dict[f]) for f in source_dict})
    except:
        return source_dict  # Not a dataclass field
