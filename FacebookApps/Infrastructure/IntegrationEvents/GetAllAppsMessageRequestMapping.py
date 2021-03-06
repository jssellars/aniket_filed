from marshmallow import fields, EXCLUDE

from Core.mapper import MapperBase


class GetAllAppsMessageRequestMapping(MapperBase):
    business_owner_facebook_id = fields.String()
    ad_account_id = fields.String()

    class Meta:
        unknown = EXCLUDE
