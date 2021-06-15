from FiledEcommerce.Api.ExportIntegration.facebook.facebook import Facebook
from FiledEcommerce.Api.ExportIntegration.interface.ecommerce import Ecommerce


class ExportIntegrationProvider:
    modules = {
        "facebook": Facebook,
    }

    @classmethod
    def get_instance(cls, integration: str) -> Ecommerce:
        return cls.modules[integration]()
