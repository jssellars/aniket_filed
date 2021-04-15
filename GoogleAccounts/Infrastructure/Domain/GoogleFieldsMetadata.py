from GoogleAccounts.Infrastructure.Domain.GoogleField import GoogleField
from GoogleAccounts.Infrastructure.Domain.GoogleFieldType import GoogleFieldType, GoogleResourceType


class GoogleFieldsMetadata:
    id = GoogleField(
        name="id", field_name="id", field_type=GoogleFieldType.ATTRIBUTE, resource_type=GoogleResourceType.CUSTOMER
    )

    descriptive_name = GoogleField(
        name="name",
        field_name="descriptive_name",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER,
    )

    currency_code = GoogleField(
        name="currency",
        field_name="currency_code",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER,
    )

    clicks = GoogleField(name="clicks", field_name="clicks", field_type=GoogleFieldType.METRIC)

    impressions = GoogleField(name="impressions", field_name="impressions", field_type=GoogleFieldType.METRIC)

    average_cpc = GoogleField(name="average_cpc", field_name="average_cpc", field_type=GoogleFieldType.METRIC)

    ctr = GoogleField(name="ctr", field_name="ctr", field_type=GoogleFieldType.METRIC)

    average_cost = GoogleField(name="average_cost", field_name="average_cost", field_type=GoogleFieldType.METRIC)

    average_cpm = GoogleField(name="average_cpm", field_name="average_cpm", field_type=GoogleFieldType.METRIC)

    conversions = GoogleField(name="conversions", field_name="conversions", field_type=GoogleFieldType.METRIC)

    conversion_rate = GoogleField(
        name="conversion_rate", field_name="conversion_rate", field_type=GoogleFieldType.METRIC
    )

    cost_per_conversion = GoogleField(
        name="cost_per_conversion", field_name="cost_per_conversion", field_type=GoogleFieldType.METRIC
    )

    date = GoogleField(name="date", field_name="date", field_type=GoogleFieldType.SEGMENT)

    level = GoogleField(
        name="level",
        field_name="level",
        field_type=GoogleFieldType.ATTRIBUTE,
        resource_type=GoogleResourceType.CUSTOMER_CLIENT,
    )
