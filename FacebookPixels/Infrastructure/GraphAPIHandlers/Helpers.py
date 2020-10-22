import typing

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase


def connect_to_graph_api_sdk(business_owner_facebook_id: typing.AnyStr,
                             startup: typing.AnyStr) -> GraphAPISdkBase:
    permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_facebook_id)
    client = GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=startup.facebook_config)
    return client
