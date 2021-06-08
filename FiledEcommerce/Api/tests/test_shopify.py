import json

import humps

from FiledEcommerce.Api.integrations.shopify.shopify import ShopifyStoreClient
from shopify_mapping import shopify_mapping

with open("products_data.json", "r", encoding="utf8") as test_file:
    data = json.loads(test_file.read())


def test_shopify_map_to_filed():
    mapped_data = ShopifyStoreClient.mapper(humps.decamelize(data), humps.decamelize(shopify_mapping["mapping"]))

    # json_mapped_data = json.dumps(mapped_data)
    assert type(mapped_data) == dict


def test_shopify_read_creds_from_db():
    # (userId 105) Only userId with PlatformId of 2
    creds = ShopifyStoreClient.read_credentials_from_db("105")
    assert type(creds) == tuple
