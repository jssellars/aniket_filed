from dataclasses import dataclass
from typing import List

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIRequestBase import GraphAPIRequestBase


@dataclass
class GraphAPIClientBaseConfig:
    verb: str = 'get'
    request: GraphAPIRequestBase = None
    fields: List[str] = None
    params: dict = None
    required_field: str = None
    async_trials: int = None
    try_partial_requests: bool = False