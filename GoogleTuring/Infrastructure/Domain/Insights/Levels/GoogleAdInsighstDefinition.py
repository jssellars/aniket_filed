from GoogleTuring.Infrastructure.Domain.Enums.ActionBreakdown import ActionBreakdown, ACTION_BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum
from GoogleTuring.Infrastructure.Domain.Enums.Level import Level
from GoogleTuring.Infrastructure.Domain.GoogleBaseFields import BASE_FIELDS
from GoogleTuring.Infrastructure.Domain.SpecificFields import ENGAGEMENT_FIELDS, AD_FIELDS


class GoogleAdInsightsDefinition:
    level = Level.AD
    breakdowns = None
    breakdown_type = None
    action_breakdowns = [ActionBreakdown.DEFAULT]
    table_name = FiledGoogleInsightsTableEnum.AD.value

    fields = {action_breakdown: [
        *BASE_FIELDS,
        *ENGAGEMENT_FIELDS,
        *AD_FIELDS,
        ACTION_BREAKDOWN_TO_FIELD[action_breakdown]
    ] for action_breakdown in action_breakdowns}
