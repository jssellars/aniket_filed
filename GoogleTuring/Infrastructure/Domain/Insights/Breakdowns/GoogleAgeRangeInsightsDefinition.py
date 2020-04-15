from Core.Web.GoogleAdWordsAPI.Enums.AdWordsPerformanceReportType import AdWordsPerformanceReportType
from GoogleTuring.Infrastructure.Domain.Enums.ActionBreakdown import ActionBreakdown, ACTION_BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Domain.Enums.Breakdown import Breakdown, BREAKDOWN_TO_FIELD, BreakdownType
from GoogleTuring.Infrastructure.Domain.Enums.Level import Level, LEVEL_TO_FIELDS
from GoogleTuring.Infrastructure.Domain.SpecificFields import ENGAGEMENT_FIELDS


class GoogleAgeInsightsDefinition:
    def __init__(self):
        self.levels = [Level.AD_GROUP]
        self.breakdowns = [Breakdown.AGE_RANGE]
        self.breakdown_type = BreakdownType.AGE_BREAKDOWN
        self.action_breakdowns = [ActionBreakdown.DEFAULT]
        self.table_name = AdWordsPerformanceReportType.AGE_RANGE.value
        self.fields = {level: {breakdown: {action_breakdown: [*LEVEL_TO_FIELDS[level], *ENGAGEMENT_FIELDS, BREAKDOWN_TO_FIELD[breakdown],
                                                              ACTION_BREAKDOWN_TO_FIELD[action_breakdown]]
                                           for action_breakdown in self.action_breakdowns}
                               for breakdown in self.breakdowns}
                       for level in self.levels
                       }
