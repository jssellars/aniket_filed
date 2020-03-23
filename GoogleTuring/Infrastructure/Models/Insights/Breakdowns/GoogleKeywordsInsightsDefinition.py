from GoogleTuring.Infrastructure.Models.Enums.ActionBreakdown import ACTION_BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Models.Enums.Breakdown import Breakdown, BreakdownType, BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Models.Enums.Level import Level, LEVEL_TO_FIELDS
from GoogleTuring.Infrastructure.Models.SpecificFields import ENGAGEMENT_FIELDS


class GoogleKeywordsInsightsDefinition:
    def __init__(self):
        self.levels = [Level.CAMPAIGN, Level.AD_GROUP]
        self.breakdowns = [Breakdown.KEYWORDS]
        self.breakdown_type = BreakdownType.KEYWORDS_BREAKDOWN
        self.action_breakdowns = []
        self.table_name = 'KEYWORDS_PERFORMANCE_REPORT'
        self.fields = {level: {breakdown: {action_breakdown: [*LEVEL_TO_FIELDS[level], *ENGAGEMENT_FIELDS, BREAKDOWN_TO_FIELD[breakdown],
                                                              ACTION_BREAKDOWN_TO_FIELD[action_breakdown]]
                                           for action_breakdown in self.action_breakdowns}
                               for breakdown in self.breakdowns}
                       for level in self.levels
                       }
