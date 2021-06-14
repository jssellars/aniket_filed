import json

import humps

from FiledEcommerce.Api.ImportIntegration.shopify.shopify import Shopify
from FiledEcommerce.Api.Mappings.shopify_mapping import shopify_mapping


def test_shopify_map_to_filed():
    products = Shopify.get_products({"user_filed_id": "105"})
    mapped_data = Shopify.mapper(next(products), humps.decamelize(shopify_mapping["mapping"]))

    with open("shopify_mapped_products.json", "w") as test_file:
        json.dump(mapped_data, test_file)


def test_shopify_read_creds_from_db():
    # (userId 105) Only userId with PlatformId of 2
    creds = Shopify.read_credentials_from_db("105")
    assert type(creds) == tuple


def test_shopify_get_products():
    products = [product for product in Shopify.get_products({"user_filed_id": "105"})]
    with open("shopify_products.json", "w") as test_file:
        json.dump(products, test_file)
