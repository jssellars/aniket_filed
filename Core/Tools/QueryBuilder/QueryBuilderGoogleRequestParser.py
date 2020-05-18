from enum import Enum

from Cython.Utils import OrderedSet

from Core.Tools.QueryBuilder.QueryBuilderFilter import QueryBuilderFilter
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
        self.time_increment = "all_days"
        self.__time_range = {}
        self.filtering = []
        self.__report = None

    @property
    def report(self):
        return self.__report

    @property
    def google_fields(self):
        return list(OrderedSet(self.__google_fields))

    @property
    def google_id(self):
        return self.__google_id

    @property
    def time_range(self):
        return self.__time_range

    def __parse_query_conditions(self, query_conditions):
        for entry in query_conditions:
            mapped_condition = self.map(entry.ColumnName)
            if entry.ColumnName == self.TimeIntervalEnum.DATE_START.value:
                self.__time_range[self.TimeRangeEnum.SINCE] = entry.Value

            elif entry.ColumnName == self.TimeIntervalEnum.DATE_STOP.value:
                self.__time_range[self.TimeRangeEnum.UNTIL] = entry.Value

            elif mapped_condition and mapped_condition == GoogleFieldsMetadata.external_customer_id:
                self.__google_id = entry.Value

            elif entry.ColumnName == self.TimeIntervalEnum.TIME_INCREMENT.value:
                self.time_increment = entry.Value

            else:
                google_filter = QueryBuilderFilter(entry)
                self.filtering.append(google_filter.as_dict())

    def __parse_query_columns(self, query_columns, column_type=None):
        for entry in query_columns:
            mapped_entry = self.map(getattr(entry, column_type.value))
            if mapped_entry:
                self.__google_fields.append(mapped_entry)

    def from_query(self, request):
        self.__report = request.get_report()
        self.__parse_query_columns(request.Dimensions, column_type=self.QueryBuilderColumnName.DIMENSION)
        self.__parse_query_columns(request.Columns, column_type=self.QueryBuilderColumnName.COLUMN)
        self.__parse_query_conditions(request.Conditions)

    @staticmethod
    def map(name):
        return next(filter(lambda x: x.field_name == name if isinstance(x, GoogleField) else None,
                           GoogleFieldsMetadata.__dict__.values()), None)
