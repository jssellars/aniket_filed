from marshmallow import fields

from Core.Tools.Mapper.MapperBase import MapperBase, MapperNestedField
from FacebookAccounts.Infrastructure.Domain.AdAccountAmountSpentModel import AdAccountAmountSpentModel


class GetAdAccountsAmountSpentInsightMessageResponseMapping(MapperBase):
    field_user_id = fields.Integer()
    user_id = fields.String()
    from_date = fields.String()
    to_date = fields.String()
    ad_accounts_amount_spent = MapperNestedField(AdAccountAmountSpentModel, many=True)
    errors = fields.List(fields.Dict)
