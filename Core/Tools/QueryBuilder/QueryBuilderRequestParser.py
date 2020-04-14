from enum import Enum

from Core.Tools.QueryBuilder.QueryBuilderFilter import QueryBuilderFilter
from FacebookTuring.Infrastructure.Mappings.LevelMapping import Level
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata


class QueryBuilderRequestParser:

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

    @property
    def parameters(self):
        parameters = {
            "level": self.level,
            "breakdowns": self.breakdowns,
            "action_breakdowns": self.action_breakdowns,
            "action_attribution_windows": self.__action_attribution_windows,
            "time_increment": self.time_increment,
            "time_range": self.time_range,
            "filtering": self.filtering
        }

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
    def action_breakdowns(self):
        return list(set(self.__action_breakdowns))

    @property
    def structure_fields(self):
        if not self.__remove_structure_fields:
            self.add_structure_meta_information()
        return list(set(self.__structure_fields))

    def add_structure_meta_information(self):
        if self.level == Level.CAMPAIGN.value:
            self.__structure_fields += [FieldsMetadata.account_name.name,
                                        FieldsMetadata.ad_account_id.name,
                                        FieldsMetadata.name.name,
                                        FieldsMetadata.id.name]
        elif self.level == Level.ADSET.value:
            self.__structure_fields += [FieldsMetadata.account_name.name,
                                        FieldsMetadata.ad_account_id.name,
                                        FieldsMetadata.campaign_id.name,
                                        FieldsMetadata.campaign_name.name,
                                        FieldsMetadata.name.name,
                                        FieldsMetadata.id.name]
        elif self.level == Level.AD.value:
            self.__structure_fields += [FieldsMetadata.account_name.name,
                                        FieldsMetadata.ad_account_id.name,
                                        FieldsMetadata.campaign_id.name,
                                        FieldsMetadata.campaign_name.name,
                                        FieldsMetadata.adset_id.name,
                                        FieldsMetadata.adset_name.name,
                                        FieldsMetadata.name.name,
                                        FieldsMetadata.id.name]

    def parse_query_columns(self, query_columns, parse_breakdowns=True, column_type=None):
        non_fields_types = [FieldType.BREAKDOWN,
                            FieldType.TIME_BREAKDOWN,
                            FieldType.ACTION_BREAKDOWN,
                            FieldType.STRUCTURE]

        for entry in query_columns:
            mapped_entry = self.map(getattr(entry, column_type.value))
            if mapped_entry:
                self.__requested_columns.append(mapped_entry)

            if mapped_entry and mapped_entry.field_type not in non_fields_types:
                self.__fields += mapped_entry.fields

            elif mapped_entry and mapped_entry.field_type == FieldType.STRUCTURE:
                self.__structure_fields += mapped_entry.fields

            elif mapped_entry and mapped_entry.field_type == FieldType.TIME_BREAKDOWN:
                self.time_increment = mapped_entry.action_field_name_value
                self.__fields += mapped_entry.fields

            if mapped_entry and parse_breakdowns:
                self.__breakdowns += mapped_entry.breakdowns if mapped_entry.breakdowns else []

                self.__action_breakdowns += mapped_entry.action_breakdowns if mapped_entry.action_breakdowns else []

    def parse_query_conditions(self, query_conditions):
        for entry in query_conditions:
            mapped_condition = self.map(entry.ColumnName)
            if entry.ColumnName == self.TimeIntervalEnum.DATE_START.value:
                self.time_range[self.TimeRangeEnum.SINCE.value] = entry.Value

            elif entry.ColumnName == self.TimeIntervalEnum.DATE_STOP.value:
                self.time_range[self.TimeRangeEnum.UNTIL.value] = entry.Value

            elif mapped_condition and (mapped_condition.name == FieldsMetadata.ad_account_id.name or mapped_condition.name == FieldsMetadata.ad_account_structure_id.name):
                self.facebook_id = entry.Value

            elif entry.ColumnName == self.TimeIntervalEnum.TIME_INCREMENT.value:
                self.time_increment = entry.Value

            else:
                facebook_filter = QueryBuilderFilter(entry)
                self.filtering.append(facebook_filter.as_dict())

    def from_query(self, request, parse_breakdowns=True):
        self.level = request.get_level()
        self.parse_query_columns(request.Columns, parse_breakdowns=parse_breakdowns, column_type=self.QueryBuilderColumnName.COLUMN)
        self.parse_query_columns(request.Dimensions, parse_breakdowns=parse_breakdowns, column_type=self.QueryBuilderColumnName.DIMENSION)
        self.parse_query_conditions(request.Conditions)

    def remove_structure_fields(self):
        self.__structure_fields = []
        self.__remove_structure_fields = True

    def map(self, name):
        return next(filter(lambda x: x.name == name if isinstance(x, Field) else None, FieldsMetadata.__dict__.values()), None)
