import typing
from dataclasses import dataclass

from Core.Metadata.Columns.ViewColumns.ViewColumn import ViewColumn


@dataclass
class InsightsReportModel:
    breakdowns: typing.Any = None  # add breakdowns_combinations: BreakdownsCombinations to the Dto
    table_name: str = None  # level = campaign, adset/adgroup, ad
    report_breakdowns: typing.List[str] = None  # only for Google -- defines the Google Report Type where the data are found
    columns: typing.List[ViewColumn] = None  # master view for the report
