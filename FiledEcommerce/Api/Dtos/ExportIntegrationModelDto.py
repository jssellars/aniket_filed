from FiledEcommerce.Api.Models.facebook_model import FacebookProduct
from FiledEcommerce.Api.Models.filed_model import FiledProduct, FiledVariant

class ExportIntegrationModelDto:
    @classmethod
    def get(cls, platform):
        model = {
            "filed": {
                "product": list(FiledProduct.__annotations__.keys()),
                "variant": list(FiledVariant.__annotations__.keys()),
            },
            "facebook": {
                "product": list(FacebookProduct.__annotations__.keys()),
            },
        }
        return {"model": model[platform]}
