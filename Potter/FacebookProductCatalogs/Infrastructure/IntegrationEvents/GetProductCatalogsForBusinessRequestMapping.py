from marshmallow import EXCLUDE, fields

from Core.Tools.Mapper.MapperBase import MapperBase


class GetProductCatalogsForBusinessRequestMapping(MapperBase):
    class Meta:
        unknown = EXCLUDE

    business_owner_facebook_id = fields.String()
    business_facebook_id = fields.String()
    filed_user_id = fields.Integer()
