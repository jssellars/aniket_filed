from marshmallow import EXCLUDE, fields

from Core.mapper import MapperBase


class GetProductSetsForCatalogRequestMapping(MapperBase):
    class Meta:
        unknown = EXCLUDE

    business_owner_facebook_id = fields.String()
    business_facebook_id = fields.String()
    product_catalog_facebook_id = fields.String()
    filed_user_id = fields.Integer()
