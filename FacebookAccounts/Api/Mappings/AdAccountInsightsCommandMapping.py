from marshmallow import fields

from Core.Tools.Mapper.MapperBase import MapperBase


class AdAccountInsightsCommandMapping(MapperBase):
    from_date = fields.String(required=True)
    to_date = fields.String(required=True)
