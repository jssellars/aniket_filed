from FiledEcommerce.Api.Mappings.facebook_mapping import facebook_mapping

class ExportIntegrationMappingDto:
    mapping = {"facebook": facebook_mapping}

    @classmethod
    def get(cls, platform):
        return cls.mapping[platform]
