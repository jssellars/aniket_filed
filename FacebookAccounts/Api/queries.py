import typing

from facebook_business.adobjects.page import Page

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Core.Web.FacebookGraphAPI.Tools import Tools
from FacebookAccounts.Api.startup import config, fixtures
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountPagesHandler import GraphAPIAdAccountPagesHandler


class AdAccountPageInstagramQuery:

    @classmethod
    def handle(cls, business_owner_id: typing.AnyStr, page_id: typing.AnyStr) -> typing.List[typing.Dict]:
        permanent_token = fixtures.business_owner_repository.get_permanent_token_by_page_id(business_owner_id, page_id)

        _ = GraphAPISdkBase(config.facebook, permanent_token)
        page = Page(page_id)
        response = page.get_instagram_accounts(fields=["username"])

        return [Tools.convert_to_json(data) for data in response]


class AdAccountPagesQuery:

    @classmethod
    def handle(cls, business_owner_id: typing.AnyStr, account_id: typing.AnyStr) -> typing.List[typing.Dict]:
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)

        response = GraphAPIAdAccountPagesHandler.handle(permanent_token, account_id, config)

        return response
