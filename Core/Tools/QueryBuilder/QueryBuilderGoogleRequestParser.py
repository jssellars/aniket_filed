from datetime import datetime
from enum import Enum

from Cython.Utils import OrderedSet

from Core.Tools.QueryBuilder.QueryBuilder import QueryBuilderSortEnum
from Core.Tools.QueryBuilder.QueryBuilderGoogleMappers import (
    QueryBuilderGoogleFilter,
    QueryBuilderGoogleFilters,
    QueryBuilderGoogleSort,
)
from Core.Tools.QueryBuilder.QueryBuilderLogicalOperator import AgGridGoogleOperator
from Core.Web.GoogleAdsAPI.Models.GoogleFieldsMetadata import GoogleFieldsMetadata as GoogleFieldsMetadataAdsAPI
from Core.Web.GoogleAdsAPI.Models.GoogleSegmentFieldsMetadata import GoogleSegmentFieldsMetadata
from GoogleTuring.Infrastructure.Constants import DEFAULT_DATETIME
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import PERFORMANCE_REPORT_TO_INFO
from GoogleTuring.Infrastructure.Domain.GoogleConditionFieldsMetadata import GoogleConditionFieldsMetadata
from GoogleTuring.Infrastructure.Domain.GoogleField import GoogleField
from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata


class QueryBuilderGoogleRequestParser:
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

    def __init__(self):
        super().__init__()
        self.__google_fields = []
        self.__google_id = None
        self.__manager_id = None
        self.time_increment = 0
        self.__time_range = {}
        self.filtering = []
        self.filters = []
        self.sorting = None
        self.g_fields = []
        self.__report = None
        self.__level = None
        self.breakdown_column = None
        self.__next_page_cursor = None
        self.__page_size = None

    @property
    def report(self):
        return self.__report

    @property
    def level(self):
        return self.__level

    @property
    def google_fields(self):
        return list(OrderedSet(self.__google_fields))

    @property
    def google_id(self):
        return self.__google_id

    @property
    def manager_id(self):
        return self.__manager_id

    @property
    def next_page_cursor(self):
        return self.__next_page_cursor

    @property
    def page_size(self):
        return self.__page_size

    @property
    def start_date(self):
        return datetime.strptime(self.__time_range[self.TimeRangeEnum.SINCE], DEFAULT_DATETIME)

    @property
    def end_date(self):
        return datetime.strptime(self.__time_range[self.TimeRangeEnum.UNTIL], DEFAULT_DATETIME)

    def __parse_query_conditions(self, query_conditions):
        for entry in query_conditions:
            mapped_field = self.map_condition_field(entry.ColumnName)
            if entry.ColumnName == self.TimeIntervalEnum.DATE_START.value:
                self.__time_range[self.TimeRangeEnum.SINCE] = entry.Value

            elif entry.ColumnName == self.TimeIntervalEnum.DATE_STOP.value:
                self.__time_range[self.TimeRangeEnum.UNTIL] = entry.Value

            elif mapped_field and mapped_field == GoogleConditionFieldsMetadata.account_id:
                self.__google_id = entry.Value

            elif entry.ColumnName == self.TimeIntervalEnum.TIME_INCREMENT.value:
                self.time_increment = entry.Value

            elif mapped_field:
                google_filter = QueryBuilderGoogleFilter(mapped_field, entry)
                self.filtering.append(google_filter)

    def __parse_query_columns(self, query_columns, column_type=None):
        for entry in query_columns:
            mapped_entry = self.map(getattr(entry, column_type.value))
            if mapped_entry:
                self.__google_fields.append(mapped_entry)

    def from_query(self, request):
        self.__report, self.__level = PERFORMANCE_REPORT_TO_INFO[request.TableName]
        self.__parse_query_columns(request.Dimensions, column_type=self.QueryBuilderColumnName.DIMENSION)
        self.__parse_query_columns(request.Columns, column_type=self.QueryBuilderColumnName.COLUMN)
        self.__parse_query_conditions(request.Conditions)

    @staticmethod
    def map(name):
        return next(
            filter(
                lambda x: x.name == name if isinstance(x, GoogleField) else None, GoogleFieldsMetadata.__dict__.values()
            ),
            None,
        )

    @staticmethod
    def map_condition_field(name):
        return next(
            filter(
                lambda x: x.name == name if isinstance(x, GoogleField) else None,
                GoogleConditionFieldsMetadata.__dict__.values(),
            ),
            None,
        )

    def create_google_filter(self, google_filter_name, filter_operator, filter_value):
        q = google_filter_name + filter_operator + filter_value
        return q

    def __parse_filter_model(self, filter_model, filter_objects):
        for column_name, filter_val in filter_model.items():
            google_filter_name = column_name
            filter_operator = getattr(AgGridGoogleOperator, filter_val.get("type"))
            filter_value = filter_val["filter"]
            filter_objects.append(QueryBuilderGoogleFilters(google_filter_name, filter_operator, filter_value))

    def __parse_time_range(self, time_range, where_conditions):
        where_field = (
            GoogleSegmentFieldsMetadata.date.field_type.value + "." + GoogleSegmentFieldsMetadata.date.field_name
        )
        where_conditions.append(
            QueryBuilderGoogleFilters(
                where_field, AgGridGoogleOperator.BETWEEN, [time_range["since"], time_range["until"]]
            )
        )

    def __parse_where_conditions(self, filter_model, time_range):
        where_conditions = []
        self.__parse_filter_model(filter_model, where_conditions)
        self.__parse_time_range(time_range, where_conditions)
        self.filters = where_conditions

    def __parse_sort_model(self, sort_model):
        if sort_model:
            self.sorting = QueryBuilderGoogleSort(sort_model.get("field"), sort_model.get("ascending"))

    def parse_ag_grid_insights_query(self, request, level=None):
        self.__google_id = request.google_account_id
        self.__manager_id = request.google_manager_id
        self.__level = level
        self.__google_fields = request.ag_columns
        self.__next_page_cursor = request.next_page_cursor
        self.__page_size = request.page_size
        self.__parse_where_conditions(request.filter_model, request.time_range)
        self.__parse_sort_model(request.sort_model)

    def map__(self, name):
        return getattr(GoogleFieldsMetadataAdsAPI, name, None)

    def parse_structure_columns(self, query_columns, column_type=None):
        for entry in query_columns:
            mapped_entry = self.map__(getattr(entry, column_type.value))
            if not mapped_entry:
                continue

            self.g_fields.append(mapped_entry)

    def parse_query_conditions(self, query_conditions):
        for entry in query_conditions:
            mapped_condition = self.map__(entry.ColumnName)
            if entry.ColumnName == self.TimeIntervalEnum.DATE_START.value:
                self.__time_range[self.TimeRangeEnum.SINCE.value] = entry.Value

            elif entry.ColumnName == self.TimeIntervalEnum.DATE_STOP.value:
                self.__time_range[self.TimeRangeEnum.UNTIL.value] = entry.Value

            elif mapped_condition and (mapped_condition.name == GoogleFieldsMetadataAdsAPI.google_account_id.name):
                self.__google_id = entry.Value

            elif mapped_condition and (mapped_condition.name == GoogleFieldsMetadataAdsAPI.google_manager_id.name):
                self.__manager_id = entry.Value

            elif entry.ColumnName == self.TimeIntervalEnum.TIME_INCREMENT.value:
                self.time_increment = entry.Value

        where_conditions = []
        self.__parse_time_range(self.__time_range, where_conditions)
        self.filters = where_conditions

    def parse_report_query(self, request):
        self.__level = request.TableName

        self.parse_structure_columns(
            request.Columns,
            column_type=self.QueryBuilderColumnName.COLUMN,
        )
        self.parse_structure_columns(
            request.Dimensions,
            column_type=self.QueryBuilderColumnName.DIMENSION,
        )
        self.parse_query_conditions(request.Conditions)

        self.breakdown_column = request.Google_breakdown

        if request.Sort:
            mapped_entry = self.map__(request.Sort.Dimension)
            is_ascending = True if request.Sort.Order == QueryBuilderSortEnum.ASCENDING else False
            self.__parse_sort_model(
                {"field": mapped_entry.field_type.value + "." + mapped_entry.field_name, "ascending": is_ascending}
            )
        else:
            sort_model = {"field": "segments.date", "ascending": True}
            self.__parse_sort_model(sort_model)
