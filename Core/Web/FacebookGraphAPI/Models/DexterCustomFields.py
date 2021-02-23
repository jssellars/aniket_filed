from Core.Web.FacebookGraphAPI.GraphAPIMappings.DexterCustomMetricMapper import DexterCustomMetricMapper
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType
from Core.Web.FacebookGraphAPI.Models.FieldsCustomMetadata import FieldsCustomMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsMetricEngagementMetadata import FieldsMetricEngagementMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsMetricPerformanceMetadata import FieldsMetricPerformanceMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsMetricStandardEventsMetadata import FieldsMetricStandardEventsMetadata


class DexterCustomFields:

    # Dexter only used fields
    result_type = Field(
        name="result_type",
    )

    landing_page_conversion_rate = Field(
        name="landing_page_conversion_rate",
        is_dexter_custom_metric=True,
        composing_fields=[FieldsCustomMetadata.conversions, FieldsMetricEngagementMetadata.unique_clicks_all],
        field_type=FieldType.CUSTOM_INSIGHTS_METRIC,
        mapper=DexterCustomMetricMapper(),
    )

    conversion_rate = Field(
        name="conversion_rate",
        is_dexter_custom_metric=True,
        composing_fields=[FieldsMetricStandardEventsMetadata.purchases_total, FieldsMetricPerformanceMetadata.clicks_all],
        field_type=FieldType.CUSTOM_INSIGHTS_METRIC,
        mapper=DexterCustomMetricMapper(),
    )


