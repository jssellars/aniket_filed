from FiledEcommerce.Api.Mappings.bigcommerce_mapping import bigcommerce_mapping
from FiledEcommerce.Api.Mappings.shopify_mapping import shopify_mapping


class ImportIntegrationMappingDto:

    mapping = {"shopify": shopify_mapping, "bigcommerce": bigcommerce_mapping}

    @classmethod
    def get(cls, platform):
        return cls.mapping[platform]
