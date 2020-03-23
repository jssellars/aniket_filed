from GoogleTuring.Infrastructure.Models.Enums.ActionBreakdown import ActionBreakdown, ACTION_BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Models.Enums.Breakdown import Breakdown, BREAKDOWN_TO_FIELD, BreakdownType
from GoogleTuring.Infrastructure.Models.Enums.Level import Level, LEVEL_TO_FIELDS
from GoogleTuring.Infrastructure.Models.SpecificFields import ENGAGEMENT_FIELDS


class GoogleAgeInsightsDefinition:
    def __init__(self):
        self.levels = [Level.CAMPAIGN, Level.AD_GROUP]
        self.breakdowns = [Breakdown.AGE_RANGE]
        self.breakdown_type = BreakdownType.AGE_BREAKDOWN
        self.action_breakdowns = [ActionBreakdown.DEVICE, ActionBreakdown.DEFAULT]
        self.table_name = 'AGE_RANGE_PERFORMANCE_REPORT'
        self.fields = {level: {breakdown: {action_breakdown: [*LEVEL_TO_FIELDS[level], *ENGAGEMENT_FIELDS, BREAKDOWN_TO_FIELD[breakdown],
                                                              ACTION_BREAKDOWN_TO_FIELD[action_breakdown]]
                                           for action_breakdown in self.action_breakdowns}
                               for breakdown in self.breakdowns}
                       for level in self.levels
                       }
