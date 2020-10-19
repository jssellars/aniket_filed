from dataclasses import dataclass


@dataclass
class GraphAPIAudiencesPermissionsForActionsDto:
    can_edit: bool = False
    can_see_insight: bool = False
    can_share: bool = False
    subtype_supports_lookalike: bool = False
    supports_recipient_lookalike: bool = False
