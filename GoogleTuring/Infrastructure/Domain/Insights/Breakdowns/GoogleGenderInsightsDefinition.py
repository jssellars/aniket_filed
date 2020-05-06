from GoogleTuring.Infrastructure.Domain.Enums.FiledGoogleInsightsTableEnum import FiledGoogleInsightsTableEnum
from GoogleTuring.Infrastructure.Domain.Enums.ActionBreakdown import ActionBreakdown, ACTION_BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Domain.Enums.Breakdown import Breakdown, BreakdownType, BREAKDOWN_TO_FIELD
from GoogleTuring.Infrastructure.Domain.Enums.Level import Level, LEVEL_TO_FIELDS
from GoogleTuring.Infrastructure.Domain.SpecificFields import ENGAGEMENT_FIELDS


class GoogleGenderInsightsDefinition:
    def __init__(self):
        self.levels = [Level.AD_GROUP]
        self.breakdowns = [Breakdown.GENDER]
        self.breakdown_type = BreakdownType.GENDER_BREAKDOWN
        self.action_breakdowns = [ActionBreakdown.DEFAULT]
        self.table_name = FiledGoogleInsightsTableEnum.GENDER.value
        self.fields = {level: {breakdown: {action_breakdown: [*LEVEL_TO_FIELDS[level], *ENGAGEMENT_FIELDS, BREAKDOWN_TO_FIELD[breakdown],
                                                              ACTION_BREAKDOWN_TO_FIELD[action_breakdown]]
                                           for action_breakdown in self.action_breakdowns}
                               for breakdown in self.breakdowns}
                       for level in self.levels
                       }
