from enum import Enum

from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.BreakdownValueFieldMapper import BreakdownValueFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.TimeBreakdownValueFieldMapper import TimeBreakdownValueFieldMapper
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType
from Core.Web.FacebookGraphAPI.Models.FieldAggregationTypeEnum import FieldAggregationTypeEnum
from Core.Web.FacebookGraphAPI.Models.FieldDataTypeEnum import FieldDataTypeEnum


class TimeBreakdownFieldValueEnum(Enum):
    daily = 1
    weekly = 7
    biweekly = 14
    monthly = "monthly"


class FieldsBreakdownMetadata:
    # ======= DELIVERY BREAKDOWNS ====== #
    breakdown_none = Field(name="none",
                           facebook_fields=[],
                           field_type=FieldType.BREAKDOWN)
    age_breakdown = Field(name="age_breakdown",
                          facebook_fields=[GraphAPIInsightsFields.age],
                          mapper=BreakdownValueFieldMapper(),
                          field_type=FieldType.BREAKDOWN,
                          data_type_id=FieldDataTypeEnum.TEXT.value,
                          aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    gender_breakdown = Field(name="gender_breakdown",
                             facebook_fields=[GraphAPIInsightsFields.gender],
                             mapper=BreakdownValueFieldMapper(),
                             field_type=FieldType.BREAKDOWN,
                             data_type_id=FieldDataTypeEnum.TEXT.value,
                             aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    country = Field(name="country",
                    facebook_fields=[GraphAPIInsightsFields.country],
                    mapper=BreakdownValueFieldMapper(),
                    field_type=FieldType.BREAKDOWN,
                    data_type_id=FieldDataTypeEnum.TEXT.value,
                    aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    dma = Field(name="dma",
                facebook_fields=[GraphAPIInsightsFields.dma],
                mapper=BreakdownValueFieldMapper(),
                field_type=FieldType.BREAKDOWN,
                data_type_id=FieldDataTypeEnum.TEXT.value,
                aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    impression_device = Field(name="impression_device",
                              facebook_fields=[GraphAPIInsightsFields.impression_device],
                              mapper=BreakdownValueFieldMapper(),
                              field_type=FieldType.BREAKDOWN,
                              data_type_id=FieldDataTypeEnum.TEXT.value,
                              aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    publisher_platform = Field(name="publisher_platform",
                               facebook_fields=[GraphAPIInsightsFields.publisher_platform],
                               mapper=BreakdownValueFieldMapper(),
                               field_type=FieldType.BREAKDOWN,
                               data_type_id=FieldDataTypeEnum.TEXT.value,
                               aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    placement = Field(name="placement",
                      facebook_fields=[GraphAPIInsightsFields.publisher_platform,
                                       GraphAPIInsightsFields.platform_position,
                                       GraphAPIInsightsFields.device_platform],
                      mapper=BreakdownValueFieldMapper(),
                      field_type=FieldType.BREAKDOWN,
                      data_type_id=FieldDataTypeEnum.TEXT.value,
                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    product_id = Field(name="product_id",
                       facebook_fields=[GraphAPIInsightsFields.product_id],
                       mapper=BreakdownValueFieldMapper(),
                       field_type=FieldType.BREAKDOWN,
                       data_type_id=FieldDataTypeEnum.TEXT.value,
                       aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    frequency_value = Field(name="frequency_value",
                            facebook_fields=[GraphAPIInsightsFields.frequency_value],
                            mapper=BreakdownValueFieldMapper(),
                            field_type=FieldType.BREAKDOWN,
                            data_type_id=FieldDataTypeEnum.TEXT.value,
                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    hourly_stats_aggregated_by_advertiser_time_zone = Field(name="hourly_stats_aggregated_by_advertiser_time_zone",
                                                            facebook_fields=[
                                                                GraphAPIInsightsFields.hourly_stats_aggregated_by_advertiser_time_zone],
                                                            mapper=BreakdownValueFieldMapper(),
                                                            field_type=FieldType.BREAKDOWN,
                                                            data_type_id=FieldDataTypeEnum.TEXT.value,
                                                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    hourly_stats_aggregated_by_audience_time_zone = Field(name="hourly_stats_aggregated_by_audience_time_zone",
                                                          facebook_fields=[
                                                              GraphAPIInsightsFields.hourly_stats_aggregated_by_audience_time_zone],
                                                          mapper=BreakdownValueFieldMapper(),
                                                          field_type=FieldType.BREAKDOWN,
                                                          data_type_id=FieldDataTypeEnum.TEXT.value,
                                                          aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    business_locations = Field(name="place_page_id",
                               facebook_fields=[GraphAPIInsightsFields.place_page_id],
                               mapper=BreakdownValueFieldMapper(),
                               field_type=FieldType.BREAKDOWN,
                               data_type_id=FieldDataTypeEnum.TEXT.value,
                               aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    platform_position = Field(name="platform_position",
                              facebook_fields=[GraphAPIInsightsFields.platform_position],
                              mapper=BreakdownValueFieldMapper(),
                              field_type=FieldType.BREAKDOWN,
                              data_type_id=FieldDataTypeEnum.TEXT.value,
                              aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    device_platform = Field(name="device_platform",
                            facebook_fields=[GraphAPIInsightsFields.device_platform],
                            mapper=BreakdownValueFieldMapper(),
                            field_type=FieldType.BREAKDOWN,
                            data_type_id=FieldDataTypeEnum.TEXT.value,
                            aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    age_gender = Field(name="age_gender",
                       facebook_fields=[GraphAPIInsightsFields.age,
                                        GraphAPIInsightsFields.gender],
                       mapper=BreakdownValueFieldMapper(),
                       field_type=FieldType.BREAKDOWN,
                       data_type_id=FieldDataTypeEnum.TEXT.value,
                       aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    platform_and_device = Field(name="platform_and_device",
                                facebook_fields=[GraphAPIInsightsFields.publisher_platform,
                                                 GraphAPIInsightsFields.impression_device],
                                mapper=BreakdownValueFieldMapper(),
                                field_type=FieldType.BREAKDOWN,
                                data_type_id=FieldDataTypeEnum.TEXT.value,
                                aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    placement_and_device = Field(name="placement_and_device",
                                 facebook_fields=[GraphAPIInsightsFields.publisher_platform,
                                                  GraphAPIInsightsFields.platform_position,
                                                  GraphAPIInsightsFields.device_platform,
                                                  GraphAPIInsightsFields.impression_device],
                                 mapper=BreakdownValueFieldMapper(),
                                 field_type=FieldType.BREAKDOWN,
                                 data_type_id=FieldDataTypeEnum.TEXT.value,
                                 aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    region = Field(name="region",
                   facebook_fields=[GraphAPIInsightsFields.region],
                   mapper=BreakdownValueFieldMapper(),
                   field_type=FieldType.BREAKDOWN,
                   data_type_id=FieldDataTypeEnum.TEXT.value,
                   aggregation_type_id=FieldAggregationTypeEnum.NULL.value)

    # ====== ACTION BREAKDOWN ====== #
    action_none = Field(name="none",
                        facebook_fields=[],
                        action_breakdowns=[],
                        field_type=FieldType.ACTION_BREAKDOWN)
    action_type = Field(name="action_type",
                        facebook_fields=[GraphAPIInsightsFields.action_type],
                        action_breakdowns=[GraphAPIInsightsFields.action_type],
                        field_type=FieldType.ACTION_BREAKDOWN,
                        data_type_id=FieldDataTypeEnum.TEXT.value,
                        aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    device = Field(name="action_device",
                   facebook_fields=[GraphAPIInsightsFields.action_device],
                   action_breakdowns=[GraphAPIInsightsFields.action_device],
                   field_type=FieldType.ACTION_BREAKDOWN,
                   data_type_id=FieldDataTypeEnum.TEXT.value,
                   aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    canvas_component = Field(name="action_canvas_component_name",
                             facebook_fields=[GraphAPIInsightsFields.action_canvas_component_name],
                             action_breakdowns=[GraphAPIInsightsFields.action_canvas_component_name],
                             field_type=FieldType.ACTION_BREAKDOWN,
                             data_type_id=FieldDataTypeEnum.TEXT.value,
                             aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    carousel_card_id = Field(name="action_carousel_card_id",
                             facebook_fields=[GraphAPIInsightsFields.action_carousel_card_id],
                             action_breakdowns=[GraphAPIInsightsFields.action_carousel_card_id],
                             field_type=FieldType.ACTION_BREAKDOWN,
                             data_type_id=FieldDataTypeEnum.TEXT.value,
                             aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    carousel_card_name = Field(name="action_carousel_card_name",
                               facebook_fields=[GraphAPIInsightsFields.action_carousel_card_name],
                               action_breakdowns=[GraphAPIInsightsFields.action_carousel_card_name],
                               field_type=FieldType.ACTION_BREAKDOWN,
                               data_type_id=FieldDataTypeEnum.TEXT.value,
                               aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    destination_breakdown = Field(name="action_destination",
                                  facebook_fields=[GraphAPIInsightsFields.action_destination],
                                  action_breakdowns=[GraphAPIInsightsFields.action_destination],
                                  field_type=FieldType.ACTION_BREAKDOWN,
                                  data_type_id=FieldDataTypeEnum.TEXT.value,
                                  aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    reaction = Field(name="action_reaction",
                     facebook_fields=[GraphAPIInsightsFields.action_reaction],
                     action_breakdowns=[GraphAPIInsightsFields.action_reaction],
                     field_type=FieldType.ACTION_BREAKDOWN,
                     data_type_id=FieldDataTypeEnum.TEXT.value,
                     aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    target = Field(name="action_target_id",
                   facebook_fields=[GraphAPIInsightsFields.action_target_id],
                   action_breakdowns=[GraphAPIInsightsFields.action_target_id],
                   field_type=FieldType.ACTION_BREAKDOWN,
                   data_type_id=FieldDataTypeEnum.TEXT.value,
                   aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    video_sound = Field(name="action_video_sound",
                        facebook_fields=[GraphAPIInsightsFields.action_video_sound],
                        action_breakdowns=[GraphAPIInsightsFields.action_video_sound],
                        field_type=FieldType.ACTION_BREAKDOWN,
                        data_type_id=FieldDataTypeEnum.TEXT.value,
                        aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    video_type = Field(name="action_video_type",
                       facebook_fields=[GraphAPIInsightsFields.action_video_type],
                       action_breakdowns=[GraphAPIInsightsFields.action_video_type],
                       field_type=FieldType.ACTION_BREAKDOWN,
                       data_type_id=FieldDataTypeEnum.TEXT.value,
                       aggregation_type_id=FieldAggregationTypeEnum.NULL.value)

    # ====== TIME BREAKDOWN ====== #
    day = Field(name="day",
                facebook_fields=[GraphAPIInsightsFields.date_start,
                                 GraphAPIInsightsFields.date_stop],
                facebook_value=TimeBreakdownFieldValueEnum.daily.value,
                mapper=TimeBreakdownValueFieldMapper(),
                field_type=FieldType.TIME_BREAKDOWN,
                data_type_id=FieldDataTypeEnum.TEXT.value,
                aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    week = Field(name="week",
                 facebook_fields=[GraphAPIInsightsFields.date_start,
                                  GraphAPIInsightsFields.date_stop],
                 facebook_value=TimeBreakdownFieldValueEnum.weekly.value,
                 mapper=TimeBreakdownValueFieldMapper(),
                 field_type=FieldType.TIME_BREAKDOWN,
                 data_type_id=FieldDataTypeEnum.TEXT.value,
                 aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    two_weeks = Field(name="two_weeks",
                      facebook_fields=[GraphAPIInsightsFields.date_start,
                                       GraphAPIInsightsFields.date_stop],
                      facebook_value=TimeBreakdownFieldValueEnum.biweekly.value,
                      mapper=TimeBreakdownValueFieldMapper(),
                      field_type=FieldType.TIME_BREAKDOWN,
                      data_type_id=FieldDataTypeEnum.TEXT.value,
                      aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
    monthly = Field(name="monthly",
                    facebook_fields=[GraphAPIInsightsFields.date_start,
                                     GraphAPIInsightsFields.date_stop],
                    facebook_value=TimeBreakdownFieldValueEnum.monthly.value,
                    mapper=TimeBreakdownValueFieldMapper(),
                    field_type=FieldType.TIME_BREAKDOWN,
                    data_type_id=FieldDataTypeEnum.TEXT.value,
                    aggregation_type_id=FieldAggregationTypeEnum.NULL.value)
