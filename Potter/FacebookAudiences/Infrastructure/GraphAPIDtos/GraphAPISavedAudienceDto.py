import typing
from dataclasses import dataclass

from Potter.FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesPermissionsForActionsDto import \
    GraphAPIAudiencesPermissionsForActionsDto
from Potter.FacebookAudiences.Infrastructure.GraphAPIDtos.GraphAPIAudiencesSentenceLineDto import \
    GraphAPIAudiencesSentenceLineDto


@dataclass
class AdAccount:
    account_id: typing.AnyStr = None
    id: typing.AnyStr = None


@dataclass
class GraphAPISavedAudienceDto:
    account: AdAccount = None
    approximate_count: int = None
    description: typing.AnyStr = None
    extra_info: typing.AnyStr = None
    id: typing.AnyStr = None
    name: typing.AnyStr = None
    permission_for_actions: GraphAPIAudiencesPermissionsForActionsDto = None
    run_status: typing.AnyStr = None
    targeting: typing.Dict = None
    sentence_lines: typing.List[GraphAPIAudiencesSentenceLineDto] = None
    time_created: typing.AnyStr = None
    time_updated: typing.AnyStr = None
