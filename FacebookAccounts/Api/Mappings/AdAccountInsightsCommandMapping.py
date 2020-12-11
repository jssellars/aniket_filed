from marshmallow import fields

from Core.mapper import MapperBase


class AdAccountInsightsCommandMapping(MapperBase):
    from_date = fields.String(required=True)
    to_date = fields.String(required=True)
