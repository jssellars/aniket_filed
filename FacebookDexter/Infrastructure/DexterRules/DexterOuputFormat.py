from typing import Optional

from FacebookDexter.Infrastructure.DexterRules.BreakdownAndAudiencesTemplates import (
    AudienceRecommendationTemplate,
    BreakdownRecommendationTemplate,
)
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import OverTimeTrendTemplate


def get_formatted_message(
    template: str,
    trigger_variance: Optional[float] = None,
    no_of_days: Optional[int] = None,
    underperforming_breakdowns: Optional[str] = None,
):
    if template in OverTimeTrendTemplate.__members__:
        output_enum = OverTimeTrendTemplate
    elif template in BreakdownRecommendationTemplate.__members__:
        output_enum = BreakdownRecommendationTemplate
    elif template in AudienceRecommendationTemplate.__members__:
        output_enum = AudienceRecommendationTemplate
    else:
        return

    if underperforming_breakdowns:
        underperforming_breakdowns = [
            entry.replace(",", " -").replace("_", "-").title() for entry in underperforming_breakdowns
        ]
        underperforming_breakdowns = ", ".join(underperforming_breakdowns)

    return output_enum[template].value.analysis.format(
        trigger_variance=trigger_variance, no_of_days=no_of_days, underperforming_breakdowns=underperforming_breakdowns
    )


def get_output_enum(template: str):
    if template in OverTimeTrendTemplate.__members__:
        return OverTimeTrendTemplate

    elif template in BreakdownRecommendationTemplate.__members__:
        return BreakdownRecommendationTemplate

    elif template in AudienceRecommendationTemplate.__members__:
        return AudienceRecommendationTemplate

    return None
