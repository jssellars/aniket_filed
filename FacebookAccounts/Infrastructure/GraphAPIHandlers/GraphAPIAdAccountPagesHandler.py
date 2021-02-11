import typing
from itertools import chain

from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.business import Business
from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from FacebookAccounts.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import GraphAPIBusinessDto
from FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIAdAccountBusinessMapping import \
    GraphAPIAdAccountBusinessMapping


class GraphAPIAdAccountPagesHandler:
    @classmethod
    def handle(
        cls,
        permanent_token: typing.AnyStr,
        account_id: typing.AnyStr,
        config
    ) -> typing.List[typing.Dict]:

        _ = GraphAPISdkBase(config.facebook, permanent_token)

        # get business_id for ad account
        business_mapping = GraphAPIAdAccountBusinessMapping(GraphAPIBusinessDto)

        account = AdAccount(account_id)
        response = account.api_get(fields=["business"])

        business = business_mapping.load(response)

        return cls.get_all_pages(account_id=account_id, business_id=business.id)

    @classmethod
    def get_all_pages(cls, account_id: typing.AnyStr, business_id: typing.AnyStr):

        account = AdAccount(account_id)
        business = Business(business_id)

        # get owned pages
        owned_pages = business.get_owned_pages()

        # get client pages
        client_pages = business.get_client_pages()

        # get promoted pages
        promote_pages = account.get_promote_pages()

        all_pages = chain(owned_pages, client_pages, promote_pages)

        # Map and remove duplicates
        ids = set()
        pages = []
        for page in all_pages:
            if not page["id"] in ids:
                ids.add(page["id"])
                page["facebook_id"] = page.pop("id")
                pages.append(page)

        return pages
