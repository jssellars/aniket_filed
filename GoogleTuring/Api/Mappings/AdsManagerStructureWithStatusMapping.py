from marshmallow import fields

from GoogleTuring.Api.Mappings.AdsManagerStructureMinimalMapping import AdsManagerStructureMinimalMapping


class AdsManagerStructuresWithStatusMapping(AdsManagerStructureMinimalMapping):
    status = fields.Integer()
