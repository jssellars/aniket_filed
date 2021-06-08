from FiledEcommerce.Api.ImportIntegration.bigcommerce.bigcommerce import BigCommerce
from FiledEcommerce.Api.ImportIntegration.csv.importcsv import ImportCsv
from FiledEcommerce.Api.ImportIntegration.interface.ecommerce import Ecommerce
from FiledEcommerce.Api.ImportIntegration.magento.magento import Magento
from FiledEcommerce.Api.ImportIntegration.shopify.shopify import Shopify
from FiledEcommerce.Api.ImportIntegration.woocommerce.woocommerce import WooCommerce


class ImportIntegrationProvider:
    modules = {
        "shopify": Shopify,
        "bigcommerce": BigCommerce,
        "magento": Magento,
        "woocommerce": WooCommerce,
        "csv": ImportCsv,
    }

    @classmethod
    def get_instance(cls, integration: str) -> Ecommerce:
        return cls.modules[integration]()
