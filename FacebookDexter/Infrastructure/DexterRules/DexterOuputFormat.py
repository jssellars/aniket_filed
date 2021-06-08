from typing import Optional

from FacebookDexter.Infrastructure.DexterRules.BreakdownAndAudiencesTemplates import (
    AudienceRecommendationTemplate,
    BreakdownRecommendationTemplate,
)
from FacebookDexter.Infrastructure.DexterRules.DexterLabsTemplate import DexterLabsTemplate
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import OverTimeTrendTemplate


def get_formatted_message(
    template: str,
    trigger_variance: Optional[float] = None,
    no_of_days: Optional[int] = None,
    underperforming_breakdowns: Optional[str] = None,
    pixel_id: Optional[str] = None,
    structure_name: Optional[str] = None,
):
    if template in OverTimeTrendTemplate.__members__:
        output_enum = OverTimeTrendTemplate
    elif template in BreakdownRecommendationTemplate.__members__:
        output_enum = BreakdownRecommendationTemplate
    elif template in AudienceRecommendationTemplate.__members__:
        output_enum = AudienceRecommendationTemplate
    elif template in DexterLabsTemplate.__members__:
        output_enum = DexterLabsTemplate
    else:
        return

    if underperforming_breakdowns:
        underperforming_breakdowns = [
            entry.replace(",", " -").replace("_", "-").title() for entry in underperforming_breakdowns
        ]
        underperforming_breakdowns = ", ".join(underperforming_breakdowns)

    return output_enum[template].value.analysis.format(
        trigger_variance=trigger_variance,
        no_of_days=no_of_days,
        underperforming_breakdowns=underperforming_breakdowns,
        pixel_id=pixel_id,
        campaign_name=structure_name,
    )


def get_output_enum(template: str):
    if template in OverTimeTrendTemplate.__members__:
        return OverTimeTrendTemplate

    elif template in BreakdownRecommendationTemplate.__members__:
        return BreakdownRecommendationTemplate

    elif template in AudienceRecommendationTemplate.__members__:
        return AudienceRecommendationTemplate

    elif template in DexterLabsTemplate.__members__:
        return DexterLabsTemplate

    return None
