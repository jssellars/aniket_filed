from marshmallow import EXCLUDE, fields

from Core.mapper import MapperBase


class AdsManagerFilteredStructuresCommandMapping(MapperBase):
    class Meta:
        unknown: EXCLUDE

    ad_account_id = fields.String()
    campaign_ids = fields.List(fields.String)
    adset_ids = fields.List(fields.String)
    statuses = fields.List(fields.Integer)
