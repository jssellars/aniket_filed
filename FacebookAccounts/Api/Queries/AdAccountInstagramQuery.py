import typing

from FacebookAccounts.Api.startup import config, fixtures
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountInstagramHandler import \
    GraphAPIAdAccountInstagramHandler


class AdAccountInstagramQuery:

    @classmethod
    def handle(cls, business_owner_id: typing.AnyStr, account_id: typing.AnyStr) -> typing.List[typing.Dict]:
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)

        response = GraphAPIAdAccountInstagramHandler.handle(permanent_token, account_id, config)

        return response
