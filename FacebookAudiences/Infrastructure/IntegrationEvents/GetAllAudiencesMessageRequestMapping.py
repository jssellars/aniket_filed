from Core.mapper import MapperBase
from marshmallow import EXCLUDE, fields


class GetAllAudiencesMessageRequestMapping(MapperBase):
    business_owner_facebook_id = fields.String()
    business_id = fields.String()
    ad_account_id = fields.String()

    class Meta:
        unknown = EXCLUDE
