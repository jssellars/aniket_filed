from datetime import datetime
from enum import Enum

from Cython.Utils import OrderedSet

from Core.Tools.QueryBuilder.QueryBuilderGoogleFilter import QueryBuilderGoogleFilter
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
        self.time_increment = 0
        self.__time_range = {}
        self.filtering = []
        self.__report = None
        self.__level = None

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
        return next(filter(lambda x: x.name == name if isinstance(x, GoogleField) else None,
                           GoogleFieldsMetadata.__dict__.values()), None)

    @staticmethod
    def map_condition_field(name):
        return next(filter(lambda x: x.name == name if isinstance(x, GoogleField) else None,
                           GoogleConditionFieldsMetadata.__dict__.values()), None)
