from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownBaseEnum, BreakdownBase, ActionBreakdownBaseEnum


class FacebookBreakdownEnum(BreakdownBaseEnum):
    NONE = BreakdownBase(name="none", display_name="")
    AGE = BreakdownBase(name="age_breakdown", display_name="Age")
    GENDER = BreakdownBase(name="gender_breakdown", display_name="Gender")
    PLACEMENT = BreakdownBase(name="placement", display_name="Placement")
    DEVICE = BreakdownBase(name="impression_device", display_name="Device")
    PLATFORM = BreakdownBase(name="platform_position", display_name="Publisher platform")
    HOUR = BreakdownBase(name="hourly_stats_aggregated_by_advertiser_time_zone", display_name="Time of day")

class FacebookActionBreakdownEnum(ActionBreakdownBaseEnum):
    NONE = BreakdownBase(name="none", display_name="")