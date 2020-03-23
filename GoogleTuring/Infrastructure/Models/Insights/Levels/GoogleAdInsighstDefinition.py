from GoogleTuring.Infrastructure.Models.GoogleBaseFields import BASE_FIELDS
from GoogleTuring.Infrastructure.Models.Enums.ActionBreakdown import ActionBreakdown, ACTION_BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Models.Enums.Level import Level
from GoogleTuring.Infrastructure.Models.SpecificFields import ENGAGEMENT_FIELDS, AD_FIELDS


class GoogleAdInsightsDefinition:
    level = Level.AD
    breakdowns = None
    breakdown_type = None
    action_breakdowns = [ActionBreakdown.DEVICE, ActionBreakdown.DEFAULT]
    table_name = 'AD_PERFORMANCE_REPORT'

    fields = {action_breakdown: [
        *BASE_FIELDS,
        *ENGAGEMENT_FIELDS,
        *AD_FIELDS,
        ACTION_BREAKDOWN_TO_FIELD[action_breakdown]
    ] for action_breakdown in action_breakdowns}
