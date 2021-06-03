import json
import typing
from enum import Enum
from typing import List

from Core.Tools.QueryBuilder.QueryBuilder import QueryBuilderDimension
from Core.Tools.QueryBuilder.QueryBuilderFilter import QueryBuilderFilter
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridFacebookOperator
from Core.Web.FacebookGraphAPI.GraphAPI.SdkGetStructures import create_facebook_filter
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import FacebookParametersStrings
from Core.Web.FacebookGraphAPI.GraphAPIMappings.LevelMapping import LevelToFacebookIdKeyMapping
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ObjectiveToResultsMapper import (
    AdSetOptimizationToCostPerResult,
    AdSetOptimizationToResult,
    PixelCustomEventTypeToCostPerResult,
    PixelCustomEventTypeToResult,
)
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata


class QueryBuilderFacebookRequestParser:
    class Level:
        ACCOUNT = "account"
        CAMPAIGN = "campaign"
        ADSET = "adset"
        AD = "ad"

    class QueryBuilderColumnName(Enum):
        COLUMN = "Name"
        DIMENSION = "GroupColumnName"

    class TimeRangeEnum(Enum):
        SINCE = "since"
        UNTIL = "until"

    class TimeIntervalEnum(Enum):
        DATE_START = "date_start"
        DATE_STOP = "date_stop"
        TIME_INCREMENT = "time_increment"

    __request_structure_columns = [
        FieldsMetadata.campaign_id.name,
        FieldsMetadata.campaign_name.name,
        FieldsMetadata.adset_id.name,
        FieldsMetadata.adset_name.name,
        FieldsMetadata.ad_id.name,
        FieldsMetadata.ad_name.name,
    ]

    def __init__(self):
        super().__init__()

        self.facebook_id = None
        self.__fields = []
        self.__breakdowns = []
        self.__action_breakdowns = []
        self.time_increment = "all_days"
        self.time_range = {}
        self.__action_attribution_windows = []
        self.filtering = []
        self.__requested_columns = []
        self.level = None
        self.__structure_fields = []
        self.__remove_structure_fields = False
        self.__sort = None
        self.next_page_cursor = None
        self.page_size = 200
        self.has_delivery = True
        self.start_row = 0
        self.end_row = 200
        self.action_filtering = []
        self.__breakdown_request_field = None
        self.adset_not_null = False

    @property
    def parameters(self):
        parameters = {
            FacebookParametersStrings.level: self.level,
            FacebookParametersStrings.breakdowns: self.breakdowns,
            FacebookParametersStrings.time_increment: self.time_increment,
            FacebookParametersStrings.time_range: self.time_range,
            FacebookParametersStrings.filtering: self.filtering,
            FacebookParametersStrings.sort: self.__sort,
            FacebookParametersStrings.limit: self.page_size,
            FacebookParametersStrings.default_summary: True,
        }

        if self.next_page_cursor:
            parameters["after"] = self.next_page_cursor

        return parameters

    @property
    def fields(self):
        return list(set(self.__fields))

    @property
    def requested_columns(self):
        return list(set(self.__requested_columns))

    @property
    def breakdowns(self):
        return list(set(self.__breakdowns))

    @property
    def breakdown_request_field(self):
        return self.__breakdown_request_field

    @property
    def action_breakdowns(self):
        return list(set(self.__action_breakdowns))

    @property
    def structure_fields(self):
        if not self.__remove_structure_fields:
            self.__add_structure_meta_information()
        return list(set(self.__structure_fields))

    def __add_structure_meta_information(self):
        if self.level == self.Level.CAMPAIGN:
            self.__structure_fields += [
                FieldsMetadata.account_name.name,
                FieldsMetadata.account_id.name,
                FieldsMetadata.name.name,
                FieldsMetadata.id.name,
            ]
        elif self.level == self.Level.ADSET:
            self.__structure_fields += [
                FieldsMetadata.account_name.name,
                FieldsMetadata.account_id.name,
                FieldsMetadata.campaign_id.name,
                FieldsMetadata.campaign_name.name,
                FieldsMetadata.name.name,
                FieldsMetadata.id.name,
            ]
        elif self.level == self.Level.AD:
            self.__structure_fields += [
                FieldsMetadata.account_name.name,
                FieldsMetadata.account_id.name,
                FieldsMetadata.campaign_id.name,
                FieldsMetadata.campaign_name.name,
                FieldsMetadata.adset_id.name,
                FieldsMetadata.adset_name.name,
                FieldsMetadata.name.name,
                FieldsMetadata.id.name,
            ]

    def parse_query_columns_ag_grid(self, request_columns: List, parse_breakdowns=True):

        non_fields_types = [
            FieldType.BREAKDOWN,
            FieldType.TIME_BREAKDOWN,
            FieldType.ACTION_BREAKDOWN,
            FieldType.STRUCTURE,
        ]

        for entry in request_columns:
            mapped_entry = self.map(entry)

            if not mapped_entry:
                continue

            self.__requested_columns.append(mapped_entry)

            if mapped_entry.field_type == FieldType.ACTION_INSIGHT:
                mapper = mapped_entry.mapper
                for action_filter in mapper.filter:
                    if action_filter.field_value:
                        self.action_filtering.append(action_filter.field_value)

            if mapped_entry.field_type not in non_fields_types:
                self.__fields += mapped_entry.facebook_fields

            elif mapped_entry.field_type == FieldType.STRUCTURE:
                self.__structure_fields += mapped_entry.facebook_fields

            elif mapped_entry.field_type == FieldType.TIME_BREAKDOWN:
                self.time_increment = mapped_entry.facebook_value
                self.__fields += mapped_entry.facebook_fields

            if parse_breakdowns:
                self.__breakdowns += (
                    mapped_entry.facebook_fields if mapped_entry.field_type == FieldType.BREAKDOWN else []
                )

                self.__action_breakdowns += (
                    mapped_entry.action_breakdowns
                    if mapped_entry.action_breakdowns or mapped_entry.field_type == FieldType.ACTION_BREAKDOWN
                    else []
                )

        if FieldsMetadata.results.name in request_columns:
            self.add_result_fields_to_request(field_groups=[PixelCustomEventTypeToResult, AdSetOptimizationToResult])

        if FieldsMetadata.cost_per_result.name in request_columns:
            self.add_result_fields_to_request(
                field_groups=[
                    PixelCustomEventTypeToCostPerResult,
                    AdSetOptimizationToCostPerResult,
                ]
            )

    def add_result_fields_to_request(self, field_groups):
        for result_group in field_groups:
            for result in result_group:
                for facebook_field in result.value.facebook_fields:
                    if facebook_field not in self.__fields:
                        self.__fields += result.value.facebook_fields

    def parse_structure_columns(self, query_columns, parse_breakdowns=True, column_type=None):
        non_fields_types = [
            FieldType.BREAKDOWN,
            FieldType.TIME_BREAKDOWN,
            FieldType.ACTION_BREAKDOWN,
            FieldType.STRUCTURE,
        ]

        for entry in query_columns:
            mapped_entry = self.map(getattr(entry, column_type.value))
            if not mapped_entry:
                continue

            if mapped_entry.field_type == FieldType.CUSTOM_INSIGHTS_METRIC:
                self.parse_structure_columns(
                    [QueryBuilderDimension(Name=field.name) for field in mapped_entry.composing_fields],
                    parse_breakdowns,
                    column_type,
                )

            self.__requested_columns.append(mapped_entry)

            if mapped_entry.field_type not in non_fields_types:
                self.__fields += mapped_entry.facebook_fields

            elif mapped_entry.field_type == FieldType.STRUCTURE:
                self.__structure_fields += mapped_entry.facebook_fields

            elif mapped_entry.field_type == FieldType.TIME_BREAKDOWN:
                self.time_increment = mapped_entry.facebook_value
                self.__fields += mapped_entry.facebook_fields

            if parse_breakdowns:
                self.__breakdowns += (
                    mapped_entry.facebook_fields if mapped_entry.field_type == FieldType.BREAKDOWN else []
                )

                self.__action_breakdowns += (
                    mapped_entry.action_breakdowns
                    if mapped_entry.action_breakdowns or mapped_entry.field_type == FieldType.ACTION_BREAKDOWN
                    else []
                )

        for query_column in query_columns:
            if FieldsMetadata.results.name == query_column.Name:
                self.add_result_fields_to_request(
                    field_groups=[
                        PixelCustomEventTypeToResult,
                        AdSetOptimizationToResult,
                    ]
                )
                break

        for query_column in query_columns:
            if FieldsMetadata.cost_per_result.name == query_column.Name:
                self.add_result_fields_to_request(
                    field_groups=[
                        PixelCustomEventTypeToCostPerResult,
                        AdSetOptimizationToCostPerResult,
                    ]
                )
                break

    def parse_query_conditions(self, query_conditions):
        for entry in query_conditions:
            mapped_condition = self.map(entry.ColumnName)
            if entry.ColumnName == self.TimeIntervalEnum.DATE_START.value:
                self.time_range[self.TimeRangeEnum.SINCE.value] = entry.Value

            elif entry.ColumnName == self.TimeIntervalEnum.DATE_STOP.value:
                self.time_range[self.TimeRangeEnum.UNTIL.value] = entry.Value

            elif mapped_condition and (
                    mapped_condition.name == FieldsMetadata.account_id.name
                    or mapped_condition.name == FieldsMetadata.ad_account_structure_id.name
            ):
                self.facebook_id = entry.Value

            elif entry.ColumnName == self.TimeIntervalEnum.TIME_INCREMENT.value:
                self.time_increment = entry.Value

            else:
                facebook_filter = QueryBuilderFilter(entry)
                self.filtering.append(facebook_filter.as_dict())

    def sort_insights_by_time(self):
        if self.parameters.get("time_increment"):
            self.__sort = ["date_start"]

    def parse(self, request, parse_breakdowns=True):
        self.level = request.set_structure_columns(self.__request_structure_columns).get_level()

        self.parse_structure_columns(
            request.Columns,
            parse_breakdowns=parse_breakdowns,
            column_type=self.QueryBuilderColumnName.COLUMN,
        )
        self.parse_structure_columns(
            request.Dimensions,
            parse_breakdowns=parse_breakdowns,
            column_type=self.QueryBuilderColumnName.DIMENSION,
        )
        self.parse_query_conditions(request.Conditions)
        self.sort_insights_by_time()

    def parse_ag_grid_insights_query(self, request, level=None, parse_breakdowns=True):
        self.level = level
        self.next_page_cursor = request.next_page_cursor
        self.facebook_id = request.facebook_account_id
        self.time_range = request.time_range
        self.page_size = request.page_size
        self.has_delivery = request.has_delivery
        self.start_row = request.start_row
        self.end_row = request.end_row
        self.adset_not_null = request.adset_not_null

        request_columns = request.ag_columns[0].split(",")
        if LevelToFacebookIdKeyMapping[self.level.upper()].value not in request_columns:
            request_columns.append(LevelToFacebookIdKeyMapping[self.level.upper()].value)

        self.parse_query_columns_ag_grid(
            parse_breakdowns=parse_breakdowns,
            request_columns=request_columns,
        )
        self.parse_filter_model(request.filter_model, request.filter_objective)
        self.parse_sort_condition(request.sort_model)

    def parse_ag_grid_trend_query(self, request, level=None, parse_breakdowns=True):
        self.level = level
        self.facebook_id = request.facebook_account_id
        self.time_range = request.time_range

        request_columns = request.ag_columns[0].split(",")

        self.parse_query_columns_ag_grid(
            parse_breakdowns=parse_breakdowns,
            request_columns=request_columns,
        )
        self.parse_filter_model(request.filter_model)
        self.parse_sort_condition()

    def parse_filter_model(self, filter_model=None, filter_objective: List = None):
        if filter_model is None:
            return

        filter_objects = []

        if self.action_filtering:
            self.action_filtering = create_facebook_filter(
                "action_type", AgGridFacebookOperator.IN, self.action_filtering
            )

        for column_name, filter_val in filter_model.items():
            facebook_filter_name = self.retrieve_filter_property_name(column_name)
            if facebook_filter_name:
                filter_operator = AgGridFacebookOperator(filter_val.get("type"))
                filter_value = filter_val.get("filter")
                if (
                        filter_operator == AgGridFacebookOperator.IN_RANGE
                        or filter_operator == AgGridFacebookOperator.NOT_IN_RANGE
                ):
                    filter_value = [filter_value, filter_val.get("filterTo")]
                filter_objects.append(create_facebook_filter(facebook_filter_name, filter_operator, filter_value))

        if filter_objective:
            filter_objects.append(create_facebook_filter("objective", AgGridFacebookOperator.IN, filter_objective))

        self.filtering = filter_objects

    def parse_sort_condition(self, sort_model=None) -> None:

        if not sort_model:
            self.__sort = ["date_start"]
            return

        required_sort = sort_model[0]
        column_name = required_sort["colId"]
        facebook_filter_name = self.retrieve_filter_property_name(column_name, is_filtered=False)

        if required_sort["sort"] == "asc":
            self.__sort = facebook_filter_name + "_ascending"
        elif required_sort["sort"] == "desc":
            self.__sort = facebook_filter_name + "_descending"

    def remove_structure_fields(self):
        self.__structure_fields = []
        self.__remove_structure_fields = True

    def map(self, name: typing.AnyStr) -> Field:
        return getattr(FieldsMetadata, name, None)

    def retrieve_filter_property_name(self, column_name: str, is_filtered=True):
        if column_name in [
            FieldsMetadata.results.name,
            FieldsMetadata.cost_per_result.name,
        ]:
            return column_name

        # Facebook Graph API requires campaign.id instead of campaign_id
        if is_filtered and column_name in [
            FieldsMetadata.campaign_id.name,
            FieldsMetadata.campaign_name.name,
            FieldsMetadata.adset_id.name,
            FieldsMetadata.adset_name.name,
            FieldsMetadata.ad_id.name,
            FieldsMetadata.ad_name.name,
        ]:
            return column_name.replace("_", ".")

        facebook_property = self.map(column_name)
        facebook_property_name = ""
        if facebook_property:
            facebook_property_name = facebook_property.facebook_fields[0]

            if facebook_property.action_breakdowns:
                facebook_field = facebook_property.mapper.filter[0].field_value
                facebook_property_name += ":" + facebook_field

        return facebook_property_name

    def __create_filtering_string(self, filter_objects):
        return "[" + ",".join(filter_objects) + "]"
