import typing

from FacebookAccounts.Api.startup import config, fixtures
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountInstagramHandler import \
    GraphAPIAdAccountInstagramHandler
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountPageInstagramHandler import \
    GraphAPIAdAccountPageInstagramHandler
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountPagesHandler import GraphAPIAdAccountPagesHandler


class AdAccountInstagramQuery:

    @classmethod
    def handle(cls, business_owner_id: typing.AnyStr, account_id: typing.AnyStr) -> typing.List[typing.Dict]:
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)

        response = GraphAPIAdAccountInstagramHandler.handle(permanent_token, account_id, config)

        return response


class AdAccountPageInstagramQuery:

    @classmethod
    def handle(cls, business_owner_id: typing.AnyStr, page_id: typing.AnyStr) -> typing.List[typing.Dict]:
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)

        response = GraphAPIAdAccountPageInstagramHandler.handle(permanent_token, page_id, config)

        return response


class AdAccountPagesQuery:

    @classmethod
    def handle(cls, business_owner_id: typing.AnyStr, account_id: typing.AnyStr) -> typing.List[typing.Dict]:
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)

        response = GraphAPIAdAccountPagesHandler.handle(permanent_token, account_id, config)

        return response
