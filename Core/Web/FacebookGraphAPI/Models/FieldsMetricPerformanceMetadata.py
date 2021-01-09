from Core.Tools.Misc.AgGridConstants import PositiveEffectTrendDirection
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import ActionFieldCondition, \
    ActionFieldConditionOperatorEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldMapper import ActionFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.CostPerActionFieldMapper import CostPerActionFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.OneToOneFieldMapper import OneToOneFieldMapper
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType
from Core.Web.FacebookGraphAPI.Models.FieldAggregationTypeEnum import FieldAggregationTypeEnum
from Core.Web.FacebookGraphAPI.Models.FieldDataTypeEnum import FieldDataTypeEnum


class FieldsMetricPerformanceMetadata:
    # todo: unavailable on FB: "(#100) impressions_gross is not valid for fields param. please check
    #  https://developers.facebook.com/docs/marketing-api/reference/ads-insights/ for all valid values",
    # gross_impressions = Field(name="impressions_gross",
    #                           facebook_fields=[GraphAPIInsightsFields.impressions_gross],
    #                           mapper=OneToOneFieldMapper(),
    #                           field_type=FieldType.INSIGHT)
    # todo: unavailable on FB: "(#100) impressions_auto_refresh is not valid for fields param. please check
    #  https://developers.facebook.com/docs/marketing-api/reference/ads-insights/ for all valid values",
    # auto_refresh_impressions = Field(name="impressions_auto_refresh",
    #                                  facebook_fields=[GraphAPIInsightsFields.impressions_auto_refresh],
    #                                  mapper=OneToOneFieldMapper(),
    #                                  field_type=FieldType.INSIGHT)
    result_rate = Field(name="conversion_rate_ranking",
                        facebook_fields=[GraphAPIInsightsFields.conversion_rate_ranking],
                        mapper=OneToOneFieldMapper(),
                        field_type=FieldType.INSIGHT)
    reach = Field(name="reach",
                  facebook_fields=[GraphAPIInsightsFields.reach],
                  mapper=OneToOneFieldMapper(),
                  field_type=FieldType.INSIGHT,
                  positive_effect_trend_direction=PositiveEffectTrendDirection.INCREASING)
    frequency = Field(name="frequency",
                      facebook_fields=[GraphAPIInsightsFields.frequency],
                      mapper=OneToOneFieldMapper(),
                      field_type=FieldType.INSIGHT,
                      positive_effect_trend_direction=PositiveEffectTrendDirection.DECREASING)
    impressions = Field(name="impressions",
                        facebook_fields=[GraphAPIInsightsFields.impressions],
                        mapper=OneToOneFieldMapper(),
                        field_type=FieldType.INSIGHT,
                        positive_effect_trend_direction=PositiveEffectTrendDirection.INCREASING)
    amount_spent = Field(name="amount_spent",
                         facebook_fields=[GraphAPIInsightsFields.spend],
                         mapper=OneToOneFieldMapper(),
                         field_type=FieldType.INSIGHT,
                         positive_effect_trend_direction=PositiveEffectTrendDirection.DECREASING)
    clicks_all = Field(name="clicks_all",
                       facebook_fields=[GraphAPIInsightsFields.clicks],
                       mapper=OneToOneFieldMapper(),
                       field_type=FieldType.INSIGHT)
    cpc_all = Field(name="cpc_all",
                    facebook_fields=[GraphAPIInsightsFields.cpc],
                    mapper=OneToOneFieldMapper(),
                    field_type=FieldType.INSIGHT)
    ctr_all = Field(name="ctr_all",
                    facebook_fields=[GraphAPIInsightsFields.ctr],
                    mapper=OneToOneFieldMapper(),
                    field_type=FieldType.INSIGHT)
    quality_ranking = Field(name="quality_ranking",
                            facebook_fields=[GraphAPIInsightsFields.quality_ranking],
                            mapper=OneToOneFieldMapper(),
                            field_type=FieldType.INSIGHT,
                            data_type_id=FieldDataTypeEnum.TEXT.value,
                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    engagement_rate_ranking = Field(name="engagement_rate_ranking",
                                    facebook_fields=[GraphAPIInsightsFields.engagement_rate_ranking],
                                    mapper=OneToOneFieldMapper(),
                                    field_type=FieldType.INSIGHT,
                                    data_type_id=FieldDataTypeEnum.TEXT.value,
                                    aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    conversion_rate_ranking = Field(name="conversion_rate_ranking",
                                    facebook_fields=[GraphAPIInsightsFields.conversion_rate_ranking],
                                    mapper=OneToOneFieldMapper(),
                                    field_type=FieldType.INSIGHT,
                                    data_type_id=FieldDataTypeEnum.TEXT.value,
                                    aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    cost_per_1000_people_reached = Field(name="cost_per_1000_people_reached",
                                         facebook_fields=[GraphAPIInsightsFields.cpp],
                                         mapper=OneToOneFieldMapper(),
                                         field_type=FieldType.INSIGHT)
    cpm = Field(name="cpm",
                facebook_fields=[GraphAPIInsightsFields.cpm],
                mapper=OneToOneFieldMapper(),
                field_type=FieldType.INSIGHT,
                positive_effect_trend_direction=PositiveEffectTrendDirection.DECREASING)
    results = Field(name="results",
                    facebook_fields=[GraphAPIInsightsFields.actions,
                                     GraphAPIInsightsFields.objective],
                    mapper=ActionFieldMapper(
                        field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                           operator=ActionFieldConditionOperatorEnum.LIKE,
                                                           field_value_map=None)]),
                    action_breakdowns=[GraphAPIInsightsFields.action_type],
                    field_type=FieldType.ACTION_INSIGHT)
    cost_per_result = Field(name="cost_per_result",
                            facebook_fields=[GraphAPIInsightsFields.actions,
                                             GraphAPIInsightsFields.objective,
                                             GraphAPIInsightsFields.spend],
                            mapper=CostPerActionFieldMapper(
                                field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                   operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                   field_value_map=None)]),
                            action_breakdowns=[GraphAPIInsightsFields.action_type],
                            field_type=FieldType.ACTION_INSIGHT,
                            is_dexter_custom_metric=True)

    # Dexter only used fields
    result_type = Field(
        name="result_type",
    )

    landing_page_conversion_rate = Field(
        name="landing_page_conversion_rate",
        is_dexter_custom_metric=True
    )

    conversion_rate = Field(
        name="conversion_rate",
        is_dexter_custom_metric=True
    )
