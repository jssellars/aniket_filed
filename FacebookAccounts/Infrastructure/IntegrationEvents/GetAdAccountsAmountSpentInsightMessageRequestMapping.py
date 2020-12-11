from marshmallow import fields, EXCLUDE

from Core.mapper import MapperBase, MapperNestedField
from FacebookAccounts.Infrastructure.IntegrationEvents.GetAdAccountsAmountSpentInsightMessageRequest import \
    AdAccountDetails


class GetAdAccountsAmountSpentInsightMessageRequestMapping(MapperBase):
    class Meta:
        unknown = EXCLUDE

    filed_user_id = fields.Integer()
    user_id = fields.String()
    from_date = fields.String()
    to_date = fields.String()
    ad_accounts_details = MapperNestedField(target=AdAccountDetails, many=True)
