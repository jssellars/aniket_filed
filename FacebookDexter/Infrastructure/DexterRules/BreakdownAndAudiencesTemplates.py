from enum import Enum

from FacebookDexter.Infrastructure.DexterRules.DexterOutput import DexterRecommendationOutput
from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import RecommendationPriority

HIDDEN_INTERESTS_MESSAGE = "We suggest duplicating a new adset and targeting these new interests: {hidden_interests}"


class BreakdownRecommendationTemplate(Enum):
    AGE_GENDER_BREAKDOWN = DexterRecommendationOutput(
        (
            "Your {breakdown_group} breakdown is not performing. Please consider removing it now to lower your cost per"
            " result. "
        ),
        RecommendationPriority.MEDIUM,
        "Change Your Breakdown ",
        "You age or gender is not performing ",
        "Dexter suggests changing your age and gender breakdown to help lower your cost per result. ",
    )

    PLACEMENT_BREAKDOWN = DexterRecommendationOutput(
        (
            "Your {breakdown_group} breakdown is not performing. Please consider removing it now to lower your cost per"
            " result.  "
        ),
        RecommendationPriority.MEDIUM,
        "Change Interest Targeting ",
        "Your placement is not performing ",
        "Dexter suggests changing your placement breakdown to help lower your cost per result ",
    )


class AudienceRecommendationTemplate(Enum):
    AUDIENCE_EXHAUSTED = DexterRecommendationOutput(
        ("You’ve reached {trigger_variance:.2f}% of your estimated audience size. "),
        RecommendationPriority.MEDIUM,
        "New Interest Targeting ",
        "Your reach is high",
        "Dexter suggests creating new audiences because your reach has targeted 75% of the estimated audience size. ",
    )
