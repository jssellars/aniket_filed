# todo: check after reapply for permissions. Requires manage_pages permission to access
import typing

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Potter.FacebookAccounts.Api.Startup import startup
from Potter.FacebookAccounts.Infrastructure.GraphAPIDtos import GraphAPIPageInstagramDto
from Potter.FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIAdAccountPageInstagramMapping import \
    GraphAPIAdAccountPageInstagramMapping
from Potter.FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestPageInstagram import \
    GraphAPIRequestPageInstagram


class GraphAPIAdAccountPageInstagramHandler:

    @classmethod
    def handle(cls,
               permanent_token: typing.AnyStr,
               page_id: typing.AnyStr) -> typing.List[typing.Dict]:
        # get instagram account
        instagram_mapping = GraphAPIAdAccountPageInstagramMapping(GraphAPIPageInstagramDto)
        config = GraphAPIClientBaseConfig()
        config.request = GraphAPIRequestPageInstagram(api_version=startup.facebook_config.api_version,
                                                      access_token=permanent_token,
                                                      page_id=page_id)
        graph_api_client = GraphAPIClientBase(business_owner_permanent_token=permanent_token, config=config)
        response, _ = graph_api_client.call_facebook()
        instagram_accounts = instagram_mapping.load(response)

        return instagram_accounts.ig_accounts
