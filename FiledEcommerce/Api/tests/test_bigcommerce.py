import json

import humps

from FiledEcommerce.Api.ImportIntegration.bigcommerce.bigcommerce import BigCommerce
from FiledEcommerce.Api.Mappings.bigcommerce_mapping import bigcommerce_mapping


def test_get_products():
    # UserId: 105 also has platformId of 4 (BigCommerce)
    products = [product for product in BigCommerce.get_products({"user_filed_id": "105"})]

    with open("bigcommerce_products.json", "w") as test_file:
        json.dump(products, test_file)


def test_bigcommerce_mapper():
    products = BigCommerce.get_products({"user_filed_id": "105"})
    mapped_data = BigCommerce.mapper(next(products), humps.depascalize(bigcommerce_mapping["mapping"]))

    with open("bigcommerce_mapped_products.json", "w") as test_file:
        json.dump(mapped_data, test_file)
