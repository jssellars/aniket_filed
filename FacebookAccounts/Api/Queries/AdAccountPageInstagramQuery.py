import typing

from FacebookAccounts.Api.startup import config, fixtures
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountPageInstagramHandler import \
    GraphAPIAdAccountPageInstagramHandler


class AdAccountPageInstagramQuery:

    @classmethod
    def handle(cls, business_owner_id: typing.AnyStr, page_id: typing.AnyStr) -> typing.List[typing.Dict]:
        permanent_token = fixtures.business_owner_repository.get_permanent_token(business_owner_id)

        response = GraphAPIAdAccountPageInstagramHandler.handle(permanent_token, page_id, config)

        return response
