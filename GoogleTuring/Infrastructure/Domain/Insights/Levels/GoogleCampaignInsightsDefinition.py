from GoogleTuring.Infrastructure.Domain.Enums.ActionBreakdown import ActionBreakdown, ACTION_BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum
from GoogleTuring.Infrastructure.Domain.Enums.Level import Level, LEVEL_TO_FIELDS
from GoogleTuring.Infrastructure.Domain.SpecificFields import ENGAGEMENT_FIELDS


class GoogleCampaignInsightsDefinition:
    level = Level.CAMPAIGN
    breakdowns = None
    breakdown_type = None
    action_breakdowns = [ActionBreakdown.DEFAULT]
    table_name = FiledGoogleInsightsTableEnum.CAMPAIGN.value

    fields = {action_breakdown: [
        *LEVEL_TO_FIELDS[Level.CAMPAIGN],
        *ENGAGEMENT_FIELDS,
        ACTION_BREAKDOWN_TO_FIELD[action_breakdown]
    ] for action_breakdown in action_breakdowns}
