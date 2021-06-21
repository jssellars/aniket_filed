import json

import humps

from FiledEcommerce.Api.ImportIntegration.magento.magento import Magento
from FiledEcommerce.Api.Mappings.magento_mapping import magento_mapping


def test_get_products():
    # UserId: 105 also has platformId of 5 (Magento)
    products = [product for product in Magento.get_products({"user_filed_id": "105"})]

    with open("magento_products.json", "w") as test_file:
        json.dump(products, test_file)


def test_magento_mapper():
    products = Magento.get_products({"user_filed_id": "105"})
    mapped_data = []
    for product in products:
        mapped_data.append(Magento.mapper(product, humps.depascalize(magento_mapping["mapping"])))

    with open("magento_mapped_products.json", "w") as test_file:
        json.dump(mapped_data, test_file)
