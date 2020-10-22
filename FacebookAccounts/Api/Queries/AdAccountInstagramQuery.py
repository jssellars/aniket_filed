import typing

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from FacebookAccounts.Api.Startup import startup
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountInstagramHandler import \
    GraphAPIAdAccountInstagramHandler


class AdAccountInstagramQuery:

    @classmethod
    def handle(cls, business_owner_id: typing.AnyStr, account_id: typing.AnyStr) -> typing.List[typing.Dict]:
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)

        response = GraphAPIAdAccountInstagramHandler.handle(permanent_token, account_id)

        return response
