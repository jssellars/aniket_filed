from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import (
    ActionFieldCondition,
    ActionFieldConditionOperatorEnum,
)
from Core.Web.FacebookGraphAPI.GraphAPIMappings.CostPerActionFieldMapper import CostPerActionFieldMapper
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
        field_type=FieldType.CUSTOM_INSIGHTS_METRIC,
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
        composing_fields=[
            FieldsMetricStandardEventsMetadata.purchases_total,
            FieldsMetricPerformanceMetadata.clicks_all,
        ],
        field_type=FieldType.CUSTOM_INSIGHTS_METRIC,
        mapper=DexterCustomMetricMapper(),
    )
    cost_per_result = Field(
        name="cost_per_result",
        facebook_fields=[
            GraphAPIInsightsFields.actions,
            GraphAPIInsightsFields.objective,
            GraphAPIInsightsFields.spend,
        ],
        mapper=CostPerActionFieldMapper(
            field_filter=[
                ActionFieldCondition(
                    field_name=GraphAPIInsightsFields.action_type,
                    operator=ActionFieldConditionOperatorEnum.LIKE,
                    field_value_map=None,
                )
            ]
        ),
        action_breakdowns=[GraphAPIInsightsFields.action_type],
        field_type=FieldType.ACTION_INSIGHT,
        is_dexter_custom_metric=True,
        composing_fields=[FieldsMetricPerformanceMetadata.amount_spent, FieldsMetricPerformanceMetadata.results],
    )
