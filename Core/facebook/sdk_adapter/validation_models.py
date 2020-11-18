from enum import Enum
from typing import Tuple, Union, Dict, List
from dataclasses import dataclass


def flatten_nested_dict(obj: Dict, *, parent_key: Union[str, Tuple[str, ...]] = ""):
    if not isinstance(obj, dict):
        raise TypeError

    result: List[Tuple] = []

    for k, v in obj.items():
        key = flatten_tuple(parent_key, maybe_enum_to_str(k))
        if isinstance(v, dict):
            result.extend(flatten_nested_dict(v, parent_key=key).items())

            continue

        if isinstance(v, (list, tuple)):
            for i in v:
                result.append((flatten_tuple(key, maybe_enum_to_str(i)), None))

            continue

        result.append((key, flatten_nested_dict(v)))

    # if all(isinstance(i, tuple) and len(i) == 2 and i[1] for i in result):
    return dict(result)


def maybe_enum_to_str(value: Enum) -> str:
    return f"{value.__class__.__name__}.{value.name}" if isinstance(value, Enum) else value


def flatten_tuple(*items: Union[str, Tuple[str, ...]]):
    result = []

    for item in items:
        if not item:
            continue

        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, tuple):
            result.extend(item)
        else:
            raise TypeError(str(item))

    return tuple(result)


@dataclass
class JointCat:
    items: List[Tuple]
    fields: Tuple[str, ...]

    @property
    def unique_field_joins(self):
        result = {tuple(ii.split(".")[0] for ii in i) for i in self.items}

        if len(result) != 1:
            raise ValueError

        return result.pop()

    @classmethod
    def from_dict(cls, data: Dict, *cat_types: type) -> "JointCat":
        return cls(list(flatten_nested_dict(data)), tuple(t.__name__ for t in cat_types))
