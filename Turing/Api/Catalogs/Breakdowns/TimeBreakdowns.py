from Turing.Api.Catalogs.Breakdowns.BreakdownsEnumeration import BreakdownsEnumeration
from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata


class TimeBreakdowns:
    day = BreakdownsEnumeration(1, FacebookFieldsMetadata.day.name, "Day")
    week = BreakdownsEnumeration(2, FacebookFieldsMetadata.week.name, "Week")
    two_weeks = BreakdownsEnumeration(3, FacebookFieldsMetadata.two_weeks.name, "Two weeks")
    month = BreakdownsEnumeration(4, FacebookFieldsMetadata.monthly.name, "Monthly")

    @classmethod
    def to_days(cls, value):
        return getattr(cls, value).column_name
