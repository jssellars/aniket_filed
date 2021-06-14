from dataclasses import dataclass, field
from typing import Dict, List, Optional

from marshmallow import INCLUDE, fields
from marshmallow.validate import Range

from Core.mapper import MapperBase


class RecommendationPageCommandMapping(MapperBase):
    ad_account_id = fields.String(required=True)
    page_number = fields.Integer(required=True, validate=Range(min=1))
    page_size = fields.Integer(required=True, validate=Range(min=1))
    level = fields.String(required=False)
    priorities = fields.List(fields.String(), required=False)
    structure_ids = fields.List(fields.String(), required=False)
    is_labs = fields.Boolean(required=False)
    labs_filter = fields.List(fields.String(), required=False)

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
    structure_ids: Optional[List[str]] = field(default_factory=list)
    is_labs: Optional[bool] = False
    labs_filter: Optional[List[str]] = None


class NumberOfPagesCommandMapping(MapperBase):
    ad_account_id = fields.String(required=True)
    level = fields.String(required=False)
    priorities = fields.List(fields.String(), required=False)
    structure_ids = fields.List(fields.String(), required=False)
    page_size = fields.Integer(required=True, validate=Range(min=1))
    is_labs = fields.Boolean(required=False)

    class Meta:
        # Include unknown fields in the deserialized output
        unknown = INCLUDE


@dataclass
class NumberOfPagesCommand:
    ad_account_id: str
    page_size: int
    level: Optional[str] = None
    priorities: Optional[List[str]] = None
    structure_ids: Optional[List[str]] = field(default_factory=list)
    is_labs: Optional[bool] = False


class ApplyRecommendationMapping(MapperBase):
    apply_button_type = fields.Integer(required=False)
    hidden_interests_data = fields.Dict(required=False)


@dataclass
class ApplyRecommendationCommand:
    apply_button_type: Optional[int] = 0
    hidden_interests_data: Optional[Dict] = None
