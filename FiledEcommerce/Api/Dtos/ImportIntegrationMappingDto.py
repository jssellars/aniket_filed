from FiledEcommerce.Api.Mappings.bigcommerce_mapping import bigcommerce_mapping
from FiledEcommerce.Api.Mappings.magento_mapping import magento_mapping
from FiledEcommerce.Api.Mappings.shopify_mapping import shopify_mapping
from FiledEcommerce.Api.Mappings.woocommerce_mapping import woocommerce_mapping


class ImportIntegrationMappingDto:
    mapping = {"shopify": shopify_mapping, "bigcommerce": bigcommerce_mapping, "magento": magento_mapping,
               "woocommerce": woocommerce_mapping}

    @classmethod
    def get(cls, platform):
        return cls.mapping[platform]
