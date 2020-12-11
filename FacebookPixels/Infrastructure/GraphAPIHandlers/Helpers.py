import typing

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase


def connect_to_graph_api_sdk(
    business_owner_facebook_id: typing.AnyStr,
    config: typing.Any,
    fixtures: typing.Any,
) -> GraphAPISdkBase:
    permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_facebook_id)

    return GraphAPISdkBase(business_owner_permanent_token=permanent_token, facebook_config=config.facebook)
