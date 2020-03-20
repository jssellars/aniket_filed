import json
import typing
from dataclasses import asdict

from Core.Tools.Misc.ObjectEncoder import ObjectEncoder


def object_to_json(data: typing.Any = None) -> typing.Dict:
    try:
        return asdict(data)
    except Exception as e:
        return json.loads(json.dumps(data, cls=ObjectEncoder))


def object_to_attribute_values_list(data: object) -> typing.List[typing.Dict]:
    return [value for _, value in object_to_json(data).items()]