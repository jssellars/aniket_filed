from marshmallow import fields

from FacebookTuring.Api.Mappings.AdsManagerStructureMinimalMapping import AdsManagerStructureMinimalMapping


class AdsManagerStructuresWithStatusMapping(AdsManagerStructureMinimalMapping):
    status = fields.Integer()
