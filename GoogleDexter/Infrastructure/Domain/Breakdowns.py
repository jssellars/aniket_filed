from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownBaseEnum, ActionBreakdownBaseEnum, BreakdownBase


class GoogleBreakdownEnum(BreakdownBaseEnum):
    NONE = BreakdownBase(name="none", display_name="")
    AGE = BreakdownBase(name="age_range", display_name="Age")
    GENDER = BreakdownBase(name="gender", display_name="Gender")
    # PLACEMENT = BreakdownBase(name="placement", display_name="Placement")
    # DEVICE = BreakdownBase(name="impression_device", display_name="Device")
    # PLATFORM = BreakdownBase(name="platform_position", display_name="Publisher platform")


class GoogleActionBreakdownEnum(ActionBreakdownBaseEnum):
    NONE = BreakdownBase(name="none", display_name="")
