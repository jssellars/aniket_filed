from FiledEcommerce.Api.Models.bigcommerce_model import BigCommerceProduct, BigCommerceVariant
from FiledEcommerce.Api.Models.filed_model import FiledProduct, FiledVariant
from FiledEcommerce.Api.Models.shopify_model import ShopifyProduct, ShopifyVariant


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
        }
        return {"model": model[platform]}
