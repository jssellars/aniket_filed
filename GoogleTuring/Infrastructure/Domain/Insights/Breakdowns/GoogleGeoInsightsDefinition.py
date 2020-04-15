from Core.Web.GoogleAdWordsAPI.Enums.AdWordsPerformanceReportType import AdWordsPerformanceReportType
from GoogleTuring.Infrastructure.Domain.Enums.ActionBreakdown import ActionBreakdown, ACTION_BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Domain.Enums.Breakdown import Breakdown, BreakdownType, BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Domain.Enums.Level import Level, LEVEL_TO_FIELDS


class GoogleGeoInsightsDefinition:
    def __init__(self):
        self.levels = [Level.CAMPAIGN, Level.AD_GROUP]
        self.breakdowns = [Breakdown.REGION, Breakdown.CITY]
        self.breakdown_type = BreakdownType.GEO_BREAKDOWN
        self.table_name = AdWordsPerformanceReportType.GEO.value
        self.action_breakdowns = [ActionBreakdown.DEVICE, ActionBreakdown.DEFAULT]

        self.fields = {
            level: {breakdown: {action_breakdown: [*LEVEL_TO_FIELDS[level], BREAKDOWN_TO_FIELD[Breakdown.COUNTRY], BREAKDOWN_TO_FIELD[breakdown],
                                                   ACTION_BREAKDOWN_TO_FIELD[action_breakdown]]
                                for action_breakdown in self.action_breakdowns}
                    for breakdown in self.breakdowns}
            for level in self.levels
        }
