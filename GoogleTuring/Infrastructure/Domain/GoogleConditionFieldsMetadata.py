from GoogleTuring.Infrastructure.Domain.ConversionFunctions import id_to_string
from GoogleTuring.Infrastructure.Domain.GoogleField import GoogleField
from GoogleTuring.Infrastructure.Domain.GoogleFieldType import GoogleFieldType
from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata


class GoogleConditionFieldsMetadata:
    account_id = GoogleField(name="account_id", field_name=GoogleFieldsMetadata.external_customer_id.field_name,
                             field_type=GoogleFieldType.ATTRIBUTE,
                             conversion_function=id_to_string)

    campaign_id = GoogleField(name="campaign.id", field_name=GoogleFieldsMetadata.campaign_id.field_name,
                              field_type=GoogleFieldType.ATTRIBUTE,
                              conversion_function=id_to_string)

    ad_id = GoogleField(name="ad.id", field_name=GoogleFieldsMetadata.ad_id.field_name,
                        field_type=GoogleFieldType.ATTRIBUTE,
                        conversion_function=id_to_string)

    ad_group_id = GoogleField(name="adgroup.id", field_name=GoogleFieldsMetadata.ad_group_id.field_name,
                              field_type=GoogleFieldType.ATTRIBUTE,
                              conversion_function=id_to_string)

    keywords_id = GoogleField(name="keywords.id", field_name=GoogleFieldsMetadata.keywords_id.field_name,
                              field_type=GoogleFieldType.ATTRIBUTE,
                              conversion_function=id_to_string)
