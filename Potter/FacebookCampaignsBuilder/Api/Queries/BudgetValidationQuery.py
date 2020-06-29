import typing

from Core.Web.BusinessOwnerRepository.BusinessOwnerRepository import BusinessOwnerRepository
from Potter.FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.GraphAPIBudgetValidationHandler import \
    GraphAPIBudgetValidationHandler


class BudgetValidationQuery:

    @classmethod
    def get(cls,
            session=None,
            business_owner_id: typing.AnyStr = None,
            account_id: typing.AnyStr = None):
        permanent_token = (BusinessOwnerRepository(session).
                           get_permanent_token(business_owner_facebook_id=business_owner_id))

        response = GraphAPIBudgetValidationHandler.handle(account_id=account_id, access_token=permanent_token)
        return response
