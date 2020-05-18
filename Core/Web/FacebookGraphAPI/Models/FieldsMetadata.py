from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import ActionFieldCondition, \
    ActionFieldConditionOperatorEnum
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldMapper import ActionFieldMapper
from Core.Web.FacebookGraphAPI.Models.Field import Field
from Core.Web.FacebookGraphAPI.Models.Field import FieldType
from Core.Web.FacebookGraphAPI.Models.FieldsBreakdownMetadata import FieldsBreakdownMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsCustomMetadata import FieldsCustomMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsMetricCustomConversionsMetadata import \
    FieldsMetricCustomConversionsMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsMetricEngagementMetadata import FieldsMetricEngagementMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsMetricPerformanceMetadata import FieldsMetricPerformanceMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsMetricStandardEventsMetadata import FieldsMetricStandardEventsMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsMetricStructureMetadata import FieldsMetricStructureMetadata
from Core.Web.FacebookGraphAPI.Models.FieldsStructureMetadata import FieldsStructureMetadata


class FieldsMetadata(FieldsStructureMetadata,
                     FieldsBreakdownMetadata,
                     FieldsCustomMetadata,
                     FieldsMetricStructureMetadata,
                     FieldsMetricPerformanceMetadata,
                     FieldsMetricEngagementMetadata,
                     FieldsMetricStandardEventsMetadata,
                     FieldsMetricCustomConversionsMetadata):
    website_purchase_roas = Field(name="website_purchase_roas",
                                  facebook_fields=[GraphAPIInsightsFields.website_purchase_roas],
                                  mapper=ActionFieldMapper(
                                      field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                         operator=ActionFieldConditionOperatorEnum.LIKE,
                                                                         field_value=GraphAPIInsightsFields.link_click)]),
                                  action_breakdowns=[GraphAPIInsightsFields.action_type],
                                  field_type=FieldType.ACTION_INSIGHT)
    purchase_roas = Field(name="purchase_roas",
                          facebook_fields=[GraphAPIInsightsFields.purchase_roas],
                          mapper=ActionFieldMapper(
                              field_filter=[ActionFieldCondition(field_name=GraphAPIInsightsFields.action_type,
                                                                 operator=ActionFieldConditionOperatorEnum.EQUALS,
                                                                 field_value=GraphAPIInsightsFields.omni_purchase)]),
                          action_breakdowns=[GraphAPIInsightsFields.action_type],
                          field_type=FieldType.ACTION_INSIGHT)
