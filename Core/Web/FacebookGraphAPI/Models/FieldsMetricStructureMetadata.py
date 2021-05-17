from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.OneToOneFieldMapper import OneToOneFieldMapper
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType
from Core.Web.FacebookGraphAPI.Models.FieldAggregationTypeEnum import FieldAggregationTypeEnum
from Core.Web.FacebookGraphAPI.Models.FieldDataTypeEnum import FieldDataTypeEnum


class FieldsMetricStructureMetadata:
    account_id = Field(name="account_id",
                       facebook_fields=[GraphAPIInsightsFields.account_id],
                       mapper=OneToOneFieldMapper(),
                       field_type=FieldType.INSIGHT,
                       data_type_id=FieldDataTypeEnum.TEXT.value,
                       aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    account_name = Field(name="account_name",
                         facebook_fields=[GraphAPIInsightsFields.account_name],
                         mapper=OneToOneFieldMapper(),
                         field_type=FieldType.INSIGHT,
                         data_type_id=FieldDataTypeEnum.TEXT.value,
                         aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    ad_id = Field(name="ad_id",
                  facebook_fields=[GraphAPIInsightsFields.ad_id],
                  mapper=OneToOneFieldMapper(),
                  field_type=FieldType.INSIGHT,
                  data_type_id=FieldDataTypeEnum.TEXT.value,
                  aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    ad_name = Field(name="ad_name",
                    facebook_fields=[GraphAPIInsightsFields.ad_name],
                    mapper=OneToOneFieldMapper(),
                    field_type=FieldType.INSIGHT,
                    data_type_id=FieldDataTypeEnum.TEXT.value,
                    aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    ad_image = Field(name="ad_image",
                    facebook_fields=[GraphAPIInsightsFields.image_url],
                    mapper=OneToOneFieldMapper(),
                    field_type=FieldType.STRUCTURE,
                    data_type_id=FieldDataTypeEnum.TEXT.value,
                    aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    adset_id = Field(name="adset_id",
                     facebook_fields=[GraphAPIInsightsFields.adset_id],
                     mapper=OneToOneFieldMapper(),
                     field_type=FieldType.INSIGHT,
                     data_type_id=FieldDataTypeEnum.TEXT.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    adset_name = Field(name="adset_name",
                       facebook_fields=[GraphAPIInsightsFields.adset_name],
                       mapper=OneToOneFieldMapper(),
                       field_type=FieldType.INSIGHT,
                       data_type_id=FieldDataTypeEnum.TEXT.value,
                       aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    campaign_id = Field(name="campaign_id",
                        facebook_fields=[GraphAPIInsightsFields.campaign_id],
                        mapper=OneToOneFieldMapper(),
                        field_type=FieldType.INSIGHT,
                        data_type_id=FieldDataTypeEnum.TEXT.value,
                        aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    campaign_name = Field(name="campaign_name",
                          facebook_fields=[GraphAPIInsightsFields.campaign_name],
                          mapper=OneToOneFieldMapper(),
                          field_type=FieldType.INSIGHT,
                          data_type_id=FieldDataTypeEnum.TEXT.value,
                          aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    objective = Field(name="objective",
                      facebook_fields=[GraphAPIInsightsFields.objective],
                      mapper=OneToOneFieldMapper(),
                      field_type=FieldType.INSIGHT,
                      data_type_id=FieldDataTypeEnum.TEXT.value,
                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    date_start = Field(name="date_start",
                       facebook_fields=[GraphAPIInsightsFields.date_start],
                       mapper=OneToOneFieldMapper(),
                       field_type=FieldType.INSIGHT,
                       data_type_id=FieldDataTypeEnum.TEXT.value,
                       aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    date_stop = Field(name="date_stop",
                      facebook_fields=[GraphAPIInsightsFields.date_stop],
                      mapper=OneToOneFieldMapper(),
                      field_type=FieldType.INSIGHT,
                      data_type_id=FieldDataTypeEnum.TEXT.value,
                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    account_status = Field(name="account_status",
                           facebook_fields=[GraphAPIInsightsFields.account_status],
                           mapper=OneToOneFieldMapper(),
                           field_type=FieldType.STRUCTURE,
                           data_type_id=FieldDataTypeEnum.NUMBER.value,
                           aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    business_id = Field(name="business_id",
                        facebook_fields=[GraphAPIInsightsFields.business_id],
                        mapper=OneToOneFieldMapper(),
                        field_type=FieldType.STRUCTURE,
                        data_type_id=FieldDataTypeEnum.TEXT.value,
                        aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    business_manager = Field(name="business_manager",
                             facebook_fields=[GraphAPIInsightsFields.business_manager],
                             mapper=OneToOneFieldMapper(),
                             field_type=FieldType.STRUCTURE,
                             data_type_id=FieldDataTypeEnum.TEXT.value,
                             aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    currency = Field(name="currency",
                     facebook_fields=[GraphAPIInsightsFields.currency],
                     mapper=OneToOneFieldMapper(),
                     field_type=FieldType.STRUCTURE,
                     data_type_id=FieldDataTypeEnum.TEXT.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
