from marshmallow import EXCLUDE, fields

from Core.Tools.Mapper.MapperBase import MapperBase


class GetProductsForCatalogRequestMapping(MapperBase):
    class Meta:
        unknown = EXCLUDE

    page_size = fields.Integer()
    business_owner_facebook_id = fields.String()
    business_facebook_id = fields.String()
    product_catalog_facebook_id = fields.String()
    filed_user_id = fields.Integer()
