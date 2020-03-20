from facebook_business.adobjects.business import Business
from facebook_business.adobjects.user import User

from Core.Web.FacebookGraphAPI.GraphAPI.GraphAPISdkBase import GraphAPISdkBase
from Potter.FacebookAccounts.Infrastructure.Domain.AdAccountModel import AdAccountModel
from Potter.FacebookAccounts.Infrastructure.Domain.BusinessModel import BusinessModel
from Potter.FacebookAccounts.Infrastructure.GraphAPIDtos.GraphAPIBusinessDto import GraphAPIBusinessDto
from Potter.FacebookAccounts.Infrastructure.GraphAPIHandlers.GraphAPIAdAccountFields import GraphAPIBusinessRequestField, GraphAPIAdAccountField
from Potter.FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIBusinessMapping import GraphAPIBusinessMapping
from Potter.FacebookAccounts.Infrastructure.GraphAPIMappings.GraphAPIToAdAccountMapping import GraphAPIToAdAccountMapping


class GraphAPIAdAccountHandler(GraphAPISdkBase):

    def __init__(self, business_owner_permanent_token, facebook_config):
        super(GraphAPIAdAccountHandler, self).__init__(facebook_config, business_owner_permanent_token)

    def get_business_owner_details(self, business_owner_facebook_id):
        businesses = User(fbid=business_owner_facebook_id).get_businesses(fields=GraphAPIBusinessRequestField.get_values())
        mapping = GraphAPIBusinessMapping(target=GraphAPIBusinessDto)
        businesses = mapping.load(businesses, many=True)

        businesses_details = []
        for business in businesses:
            business_dto = BusinessModel()
            business_dto.id = business.id
            business_dto.name = business.name
            business_dto.ad_accounts.extend(self.get_owned_accounts(business.id))
            business_dto.ad_accounts.extend(self.get_client_accounts(business.id))
            businesses_details.append(business_dto)

        return businesses_details

    def get_client_accounts(self, facebook_id):
        accounts = Business(fbid=facebook_id).get_client_ad_accounts(fields=GraphAPIAdAccountField.get_values())
        mapping = GraphAPIToAdAccountMapping(AdAccountModel)
        return mapping.load(accounts, many=True)

    def get_owned_accounts(self, facebook_id):
        accounts = Business(fbid=facebook_id).get_owned_ad_accounts(fields=GraphAPIAdAccountField.get_values())
        mapping = GraphAPIToAdAccountMapping(AdAccountModel)
        return mapping.load(accounts, many=True)
