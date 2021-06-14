from FiledEcommerce.Api.Models.bigcommerce_model import BigCommerceProduct, BigCommerceVariant
from FiledEcommerce.Api.Models.csv_model import CsvVariant, CsvProduct
from FiledEcommerce.Api.Models.filed_model import FiledProduct, FiledVariant
from FiledEcommerce.Api.Models.magento_model import MagentoProduct, MagentoProductVariant
from FiledEcommerce.Api.Models.shopify_model import ShopifyProduct, ShopifyVariant
from FiledEcommerce.Api.Models.woocommerce_model import WoocommerceProduct, WoocommerceVariant


class ImportIntegrationModelDto:
    @classmethod
    def get(cls, platform):
        model = {
            "filed": {
                "product": list(FiledProduct.__annotations__.keys()),
                "variant": list(FiledVariant.__annotations__.keys()),
            },
            "bigcommerce": {
                "product": list(BigCommerceProduct.__annotations__.keys()),
                "variant": list(BigCommerceVariant.__annotations__.keys()),
            },
            "shopify": {
                "product": list(ShopifyProduct.__annotations__.keys()),
                "variant": list(ShopifyVariant.__annotations__.keys()),
            },
            "magento": {
                "product": list(MagentoProduct.__annotations__.keys()),
                "variant": list(MagentoProductVariant.__annotations__.keys()),
            },
            "woocommerce": {
                "product": list(WoocommerceProduct.__annotations__.keys()),
                "variant": list(WoocommerceVariant.__annotations__.keys()),
            },
            "csv": {
                "product": list(CsvProduct.__annotations__.keys()),
                "variant": list(CsvVariant.__annotations__.keys()),
            },
        }
        return {"model": model[platform]}
