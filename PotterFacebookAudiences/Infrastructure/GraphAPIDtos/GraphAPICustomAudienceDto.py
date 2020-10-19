import typing
from dataclasses import dataclass

from PotterFacebookAudiences.Infrastructure.GraphAPIDtos import GraphAPIAudiencesPermissionsForActionsDto
from PotterFacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesLookalikeSpecDto import \
    GraphAPIAudiencesLookalikeSpecDto


@dataclass
class OperationStatus:
    code: int = None
    description: typing.AnyStr = None


@dataclass
class DataSource:
    type: typing.AnyStr = None
    sub_type: typing.AnyStr = None
    creation_params: typing.AnyStr = None


@dataclass
class SharingStatus:
    sharing_relationship_id: int = None
    status: typing.AnyStr = None


@dataclass
class GraphAPICustomAudienceDto:
    id: typing.AnyStr = None
    name: typing.AnyStr = None
    description: typing.AnyStr = None
    account_id: typing.AnyStr = None
    approximate_count: int = None
    time_created: typing.AnyStr = None  # timestamp
    time_updated: typing.AnyStr = None  # timestamp
    time_content_updated: typing.AnyStr = None  # timestamp
    is_value_based: bool = False
    subtype: typing.AnyStr = None
    permissions_for_actions: GraphAPIAudiencesPermissionsForActionsDto = None
    lookalike_audience_ids: typing.List[typing.AnyStr] = None
    external_event_source: typing.AnyStr = None
    pixel_id: typing.AnyStr = None
    retention_days: int = None
    rule: typing.AnyStr = None
    rule_aggregation: typing.AnyStr = None
    operation_status: OperationStatus = None
    delivery_status: OperationStatus = None
    data_source: DataSource = None
    customer_file_source: typing.AnyStr = None
    opt_out_link: typing.AnyStr = None
    sharing_status: SharingStatus = None
    lookalike_spec: GraphAPIAudiencesLookalikeSpecDto = None
