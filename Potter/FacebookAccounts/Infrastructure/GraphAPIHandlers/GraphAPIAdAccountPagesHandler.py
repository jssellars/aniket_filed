import typing

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from Potter.FacebookAccounts.Api.Startup import startup
from Potter.FacebookAccounts.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import GraphAPIBusinessDto
from Potter.FacebookAccounts.Infrastructure.GraphAPIDtos.GraphAPIPagesDto import GraphAPIPagesDto
from Potter.FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIAdAccountBusinessMapping import GraphAPIAdAccountBusinessMapping
from Potter.FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIAdAccountPagesMapping import GraphAPIAdAccountPagesMapping
from Potter.FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestBusiness import GraphAPIRequestBusiness
from Potter.FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestClientPages import GraphAPIRequestClientPages
from Potter.FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestOwnedPages import GraphAPIRequestOwnedPages


class GraphAPIAdAccountPagesHandler:

    @classmethod
    def handle(cls,
               permanent_token: typing.AnyStr,
               account_id: typing.AnyStr) -> typing.List[typing.Dict]:

        #  get business_id for ad account
        business_mapping = GraphAPIAdAccountBusinessMapping(GraphAPIBusinessDto)
        config = GraphAPIClientBaseConfig()
        config.request = GraphAPIRequestBusiness(api_version=startup.facebook_config.api_version,
                                                 access_token=permanent_token,
                                                 account_id=account_id)
        graph_api_client = GraphAPIClientBase(business_owner_permanent_token=permanent_token, config=config)
        response, _ = graph_api_client.call_facebook()
        business = business_mapping.load(response)

        # get owned pages
        pages_mapping = GraphAPIAdAccountPagesMapping(GraphAPIPagesDto)
        config.request = GraphAPIRequestOwnedPages(api_version=startup.facebook_config.api_version,
                                                   access_token=permanent_token,
                                                   business_id=business.id)
        graph_api_client.config = config
        response, _ = graph_api_client.call_facebook()
        owned_pages = pages_mapping.load(response)

        # get client pages
        config.request = GraphAPIRequestClientPages(api_version=startup.facebook_config.api_version,
                                                    access_token=permanent_token,
                                                    business_id=business.id)
        response, _ = graph_api_client.call_facebook()
        client_pages = pages_mapping.load(response)

        pages = owned_pages.pages + client_pages.pages

        return pages
