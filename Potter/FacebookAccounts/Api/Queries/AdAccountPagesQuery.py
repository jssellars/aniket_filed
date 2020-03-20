import typing

import humps

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Potter.FacebookAccounts.Api.Startup import startup
from Potter.FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountPagesHandler import GraphAPIAdAccountPagesHandler


class AdAccountPagesQuery:

    @classmethod
    def handle(cls, business_owner_id: typing.AnyStr, account_id: typing.AnyStr) -> typing.List[typing.Dict]:

        permanent_token = BusinessOwnerRepository(startup.session).get_permanent_token(business_owner_id)

        response = GraphAPIAdAccountPagesHandler.handle(permanent_token, account_id)

        return response
