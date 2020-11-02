import copy
from dataclasses import dataclass
from typing import List, Dict, Union, Optional

import humps


@dataclass
class Node:
    key: str
    children: Optional[List["Node"]] = None

    def __init__(self, key: str, *children: Union[str, "Node"]) -> None:
        self.key = key
        self.children = list(children) if children else None
        self.convert_children_to_objects()

    def with_children(self, *children: Union[str, "Node"]) -> "Node":
        result = copy.deepcopy(self)
        result.children = list(children)
        result.convert_children_to_objects()

        return result

    def convert_children_to_objects(self) -> None:
        if self.children is None:
            return

        self.children = [Node.from_other(c) for c in self.children]

    def to_json(self) -> Dict:
        result = {}
        for key, value in self.__dict__.items():
            if value is None:
                continue

            if isinstance(value, Node):
                result[humps.camelize(key)] = value.to_json()
                continue

            if isinstance(value, List):
                result[humps.camelize(key)] = [i.to_json() for i in value]
                continue

            result[humps.camelize(key)] = value

        return result

    @staticmethod
    def from_other(other: Union[str, "Node"]) -> "Node":
        if isinstance(other, Node):
            return other

        return Node(other)
