from FiledEcommerce.Api.ImportIntegration.bigcommerce.bigcommerce import BigCommerce
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Api.ImportIntegration.shopify.shopify import Shopify


class ImportIntegrationProvider:
    modules = {"shopify": Shopify, "bigcommerce": BigCommerce}

    @classmethod
    def get_instance(cls, integration: str) -> Ecommerce:
        return cls.modules[integration]()
