import typing

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientBase import GraphAPIClientBase
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPIClientConfig import GraphAPIClientBaseConfig
from FacebookAccounts.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import GraphAPIBusinessDto
from FacebookAccounts.Infrastructure.GraphAPIDtos.GraphAPIPagesDto import GraphAPIPagesDto
from FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIAdAccountBusinessMapping import \
    GraphAPIAdAccountBusinessMapping
from FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIAdAccountPagesMapping import \
    GraphAPIAdAccountPagesMapping
from FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestBusiness import GraphAPIRequestBusiness
from FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestClientPages import \
    GraphAPIRequestClientPages
from FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestOwnedPages import GraphAPIRequestOwnedPages
from FacebookAccounts.Infrastructure.GraphAPIRequests.GraphAPIRequestPromotePages import \
    GraphAPIRequestPromotePages


class GraphAPIAdAccountPagesHandler:
    @classmethod
    def handle(cls,
        permanent_token: typing.AnyStr,
        account_id: typing.AnyStr,
        config
    ) -> typing.List[typing.Dict]:
        # get business_id for ad account
        business_mapping = GraphAPIAdAccountBusinessMapping(GraphAPIBusinessDto)
        api_config = GraphAPIClientBaseConfig()
        api_config.request = GraphAPIRequestBusiness(api_version=config.facebook.api_version,
                                                 access_token=permanent_token,
                                                 account_id=account_id)
        graph_api_client = GraphAPIClientBase(business_owner_permanent_token=permanent_token, config=api_config)
        response, _ = graph_api_client.call_facebook()
        business = business_mapping.load(response)

        # get owned pages
        pages_mapping = GraphAPIAdAccountPagesMapping(GraphAPIPagesDto)
        api_config.request = GraphAPIRequestOwnedPages(api_version=config.facebook.api_version,
                                                   access_token=permanent_token,
                                                   business_id=business.id)
        graph_api_client.config = api_config
        response, _ = graph_api_client.call_facebook()
        owned_pages = pages_mapping.load(response)

        # get client pages
        api_config.request = GraphAPIRequestClientPages(api_version=config.facebook.api_version,
                                                    access_token=permanent_token,
                                                    business_id=business.id)
        response, _ = graph_api_client.call_facebook()
        client_pages = pages_mapping.load(response)

        # get promoted pages
        api_config.request = GraphAPIRequestPromotePages(api_version=config.facebook.api_version,
                                                     access_token=permanent_token,
                                                     account_id=account_id)
        response, _ = graph_api_client.call_facebook()
        promote_pages = pages_mapping.load(response)

        pages = owned_pages.pages + client_pages.pages + promote_pages.pages

        return pages
