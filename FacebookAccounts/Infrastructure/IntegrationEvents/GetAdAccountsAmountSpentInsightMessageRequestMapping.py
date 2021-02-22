from marshmallow import fields, EXCLUDE

from Core.mapper import MapperBase


class GetAdAccountsAmountSpentInsightMessageRequestMapping(MapperBase):
    class Meta:
        unknown = EXCLUDE

    filed_user_id = fields.Integer()
    business_owner_facebook_id = fields.String()
    ad_account_ids = fields.List(fields.String())
    dates = fields.List(fields.Date())
