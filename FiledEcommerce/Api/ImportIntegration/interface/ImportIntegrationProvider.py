from FiledEcommerce.Api.ImportIntegration.bigcommerce.bigcommerce import BigCommerce
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Api.ImportIntegration.shopify.shopify import Shopify
from FiledEcommerce.Api.ImportIntegration.magento.magento import Magento

class ImportIntegrationProvider:
    modules = {"shopify": Shopify, "bigcommerce": BigCommerce, "magento": Magento}

    @classmethod
    def get_instance(cls, integration: str) -> Ecommerce:
        return cls.modules[integration]()
