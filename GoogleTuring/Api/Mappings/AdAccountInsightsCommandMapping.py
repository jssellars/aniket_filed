from marshmallow import fields

from Core.Tools.Mapper.MapperBase import MapperBase


class AdAccountInsightsCommandMapping(MapperBase):
    business_owner_google_id = fields.String()
    from_date = fields.String(required=True)
    to_date = fields.String(required=True)
