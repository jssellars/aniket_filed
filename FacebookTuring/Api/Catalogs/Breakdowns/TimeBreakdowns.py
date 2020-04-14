from FacebookTuring.Api.Catalogs.Breakdowns.BreakdownsEnumeration import BreakdownsEnumeration
from FacebookTuring.Infrastructure.Models.FacebookFieldsMetadata import FieldsMetadata


class TimeBreakdowns:
    day = BreakdownsEnumeration(1, FieldsMetadata.day.name, "Day")
    week = BreakdownsEnumeration(2, FieldsMetadata.week.name, "Week")
    two_weeks = BreakdownsEnumeration(3, FieldsMetadata.two_weeks.name, "Two weeks")
    month = BreakdownsEnumeration(4, FieldsMetadata.monthly.name, "Monthly")

    @classmethod
    def to_days(cls, value):
        return getattr(cls, value).column_name
