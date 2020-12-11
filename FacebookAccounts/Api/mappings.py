from marshmallow import fields

from Core.mapper import MapperBase


class AdAccountInsightsCommandMapping(MapperBase):
    from_date = fields.String(required=True)
    to_date = fields.String(required=True)


class BusinessOwnerCreateCommandMapping(MapperBase):
    facebook_id = fields.String(required=True)
    name = fields.String()
    email = fields.String()
    temporary_token = fields.String(required=True)
    requested_permissions = fields.List(fields.String(), required=True)
    filed_user_id = fields.Integer(required=True)


class BusinessOwnerUpdateCommandMapping(MapperBase):
    facebook_id = fields.String(required=True)
