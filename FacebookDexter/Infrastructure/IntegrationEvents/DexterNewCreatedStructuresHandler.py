from dataclasses import dataclass
from typing import List

from marshmallow import EXCLUDE, fields

from Core.mapper import MapperBase, MapperNestedField


@dataclass
class NewCreatedStructureKeys:
    level: str
    account_id: str
    facebook_id: str


class DexterCreatedEventMapping(MapperBase):
    business_owner_id = fields.String()
    new_created_structures = MapperNestedField(target=NewCreatedStructureKeys, many=True)

    class Meta:
        unknown = EXCLUDE


@dataclass
class DexterNewCreatedStructureEvent:
    business_owner_id: str
    new_created_structures: List[NewCreatedStructureKeys]
    message_type: str = "DexterNewCreatedStructureEvent"
