from dataclasses import dataclass
from typing import AnyStr, Dict, List

from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata


@dataclass
class OrchestratorRunConfig:
    permanent_token: AnyStr = None
    account_id: AnyStr = None
    level: AnyStr = None
    fields: List[AnyStr] = None
    params: Dict = None
    structure_fields: List[AnyStr] = None
    requested_fields: List[FieldsMetadata] = None
    check_has_data: bool = True
    structures_sync: bool = False