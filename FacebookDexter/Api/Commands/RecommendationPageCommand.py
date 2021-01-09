from dataclasses import dataclass

from marshmallow import fields, INCLUDE
from marshmallow.validate import Range
from typing import Optional, List

from Core.mapper import MapperBase


class RecommendationPageCommandMapping(MapperBase):
    ad_account_id = fields.String(required=True)
    page_number = fields.Integer(required=True, validate=Range(min=1))
    page_size = fields.Integer(required=True, validate=Range(min=1))
    level = fields.String(required=False)
    priorities = fields.List(fields.String(), required=False)

    class Meta:
        # Include unknown fields in the deserialized output
        unknown = INCLUDE


@dataclass
class RecommendationPageCommand:
    ad_account_id: str
    page_number: int
    page_size: int
    level: Optional[str] = None
    priorities: Optional[List[str]] = None


class NumberOfPagesCommandMapping(MapperBase):
    ad_account_id = fields.String(required=True)
    level = fields.String(required=False)
    priorities = fields.List(fields.String(), required=False)
    page_size = fields.Integer(required=True, validate=Range(min=1))

    class Meta:
        # Include unknown fields in the deserialized output
        unknown = INCLUDE


@dataclass
class NumberOfPagesCommand:
    ad_account_id: str
    page_size: int
    level: Optional[str] = None
    priorities: Optional[List[str]] = None
