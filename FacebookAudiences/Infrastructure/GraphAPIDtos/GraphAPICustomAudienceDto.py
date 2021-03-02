from dataclasses import dataclass
from typing import List

from FacebookAudiences.Infrastructure.GraphAPIDtos import GraphAPIAudiencesPermissionsForActionsDto
from FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesLookalikeSpecDto import (
    GraphAPIAudiencesLookalikeSpecDto,
)


@dataclass
class OperationStatus:
    code: int = None
    description: str = None


@dataclass
class DataSource:
    type: str = None
    sub_type: str = None
    creation_params: str = None


@dataclass
class SharingStatus:
    sharing_relationship_id: int = None
    status: str = None


@dataclass
class GraphAPICustomAudienceDto:
    id: str = None
    name: str = None
    description: str = None
    account_id: str = None
    approximate_count: int = None
    time_created: str = None  # timestamp
    time_updated: str = None  # timestamp
    time_content_updated: str = None  # timestamp
    is_value_based: bool = False
    subtype: str = None
    permissions_for_actions: GraphAPIAudiencesPermissionsForActionsDto = None
    lookalike_audience_ids: List[str] = None
    external_event_source: str = None
    pixel_id: str = None
    retention_days: int = None
    rule: str = None
    rule_aggregation: str = None
    operation_status: OperationStatus = None
    delivery_status: OperationStatus = None
    data_source: DataSource = None
    customer_file_source: str = None
    opt_out_link: str = None
    sharing_status: SharingStatus = None
    lookalike_spec: GraphAPIAudiencesLookalikeSpecDto = None
