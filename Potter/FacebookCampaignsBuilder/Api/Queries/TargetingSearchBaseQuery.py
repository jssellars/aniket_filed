import typing

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase


class TargetingSearchBaseQuery:

    def __init__(self, session=None, business_owner_id: typing.AnyStr = None, facebook_config=None):
        self._permanent_token = (BusinessOwnerRepository(session).
                                 get_permanent_token(business_owner_facebook_id=business_owner_id))
        self._graph_api_sdk = GraphAPISdkBase(facebook_config=facebook_config,
                                              business_owner_permanent_token=self._permanent_token)
