from inspect import isfunction
from typing import Any, List


def extract_class_attributes_values(obj) -> List:
    return [getattr(obj, attr) for attr in dir(obj) if should_extract(obj, attr)]


def extract_class_attributes(obj) -> List[str]:
    return [attr for attr in dir(obj) if should_extract(obj, attr)]


def should_extract(obj: Any, attr: str) -> bool:
    value = getattr(obj, attr)

    return not (attr.startswith("__") or callable(value) or isfunction(value))
