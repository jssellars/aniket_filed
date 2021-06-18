from enum import Enum

from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import ApplyActionType
from FacebookDexter.Infrastructure.DexterRules.DexterOutput import DexterRecommendationOutput
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import RecommendationPriority

HIDDEN_INTERESTS_MESSAGE = "We suggest duplicating a new adset and targeting these new interests: {hidden_interests}"


class BreakdownRecommendationTemplate(Enum):
    AGE_GENDER_BREAKDOWN = DexterRecommendationOutput(
        (
            "Your {underperforming_breakdowns} breakdown is not performing as well as the other breakdowns."
        ),
        RecommendationPriority.MEDIUM,
        "Change Your Breakdown ",
        "An age-gender breakdown is not performing",
        "Dexter recommends removing the underperforming age-gender breakdown. Click apply and I’ll do this for you!",
        apply_action_type=ApplyActionType.AGE_GENDER_BREAKDOWN_SPLIT,
    )

    PLACEMENT_BREAKDOWN = DexterRecommendationOutput(
        (
            "Your following breakdowns are not performing: {underperforming_breakdowns}. Please consider removing them"
            " now to lower your cost per result. "
        ),
        RecommendationPriority.MEDIUM,
        "Change Interest Targeting ",
        "Your placement is not performing ",
        "Dexter suggests changing your placement breakdown to help lower your cost per result ",
    )


class AudienceRecommendationTemplate(Enum):
    AUDIENCE_EXHAUSTED = DexterRecommendationOutput(
        "You’ve reached {trigger_variance:.2f}% of your estimated audience size.",
        RecommendationPriority.MEDIUM,
        "New Interest Targeting ",
        "Your reach is high",
        "Dexter suggests creating new audiences because your reach has targeted 75% of the estimated audience size. ",
    )
