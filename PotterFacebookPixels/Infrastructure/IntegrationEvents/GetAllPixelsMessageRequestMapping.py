from marshmallow import fields, EXCLUDE

from Core.Tools.Mapper.MapperBase import MapperBase


class GetAllPixelsMessageRequestMapping(MapperBase):
    business_owner_facebook_id = fields.String()
    ad_account_id = fields.String()

    class Meta:
        unknown = EXCLUDE
