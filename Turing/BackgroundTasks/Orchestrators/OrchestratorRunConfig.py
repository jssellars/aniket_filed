from dataclasses import dataclass
from typing import AnyStr, Dict, List

from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata


@dataclass
class OrchestratorRunConfig:
    permanent_token: AnyStr = None
    account_id: AnyStr = None
    level: AnyStr = None
    fields: List[AnyStr] = None
    params: Dict = None
    structure_fields: List[AnyStr] = None
    requested_fields: List[FacebookFieldsMetadata] = None
    check_has_data: bool = True
    structures_sync: bool = False