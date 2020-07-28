from Core.Tools.Misc.Autoincrement import Autoincrement
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Breakdowns.BreakdownsEnumeration import BreakdownsEnumeration

time_breakdown_id = Autoincrement(200)


class TimeBreakdowns:
    day = BreakdownsEnumeration(time_breakdown_id.increment(), FieldsMetadata.day.name, "Day")
    week = BreakdownsEnumeration(time_breakdown_id.increment(), FieldsMetadata.week.name, "Week")
    two_weeks = BreakdownsEnumeration(time_breakdown_id.increment(), FieldsMetadata.two_weeks.name, "Two weeks")
    month = BreakdownsEnumeration(time_breakdown_id.increment(), FieldsMetadata.monthly.name, "Monthly")

    @classmethod
    def to_days(cls, value):
        return getattr(cls, value).column_name
