import typing

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from FacebookAccounts.Api.Startup import startup
from FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountPageInstagramHandler import \
    GraphAPIAdAccountPageInstagramHandler


class AdAccountPageInstagramQuery:

    @classmethod
    def handle(cls, business_owner_id: typing.AnyStr, page_id: typing.AnyStr) -> typing.List[typing.Dict]:
        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)

        response = GraphAPIAdAccountPageInstagramHandler.handle(permanent_token, page_id)

        return response
