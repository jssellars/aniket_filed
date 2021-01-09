from enum import Enum

from FacebookDexter.Infrastructure.DexterRules.OverTimeTrendTemplates import (
    RecommendationPriority,
    InfoRecommendationTemplate,
)


class BreakdownRecommendationTemplate(Enum):
    AGE_GENDER_BREAKDOWN = (
        (
            "Your {breakdown_group} breakdown is not performing. Please consider removing it now to lower your cost per"
            " result. "
        ),
        RecommendationPriority.MEDIUM,
        "Change Your Breakdown ",
        "You age or gender is not performing ",
        "Dexter suggests changing your age and gender breakdown to help lower your cost per result. ",
    )

    PLACEMENT_BREAKDOWN = (
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
    AUDIENCE_EXHAUSTED = (
        (
            "You’ve reached {trigger_variance:.2f}% of your estimated audience size. Duplicate your audience now and"
            " target this recommended audience [audience]."
        ),
        RecommendationPriority.MEDIUM,
        "New Interest Targeting ",
        "Your reach is high",
        "Dexter suggests creating new audiences because your reach has targeted 75% of the estimated audience size. ",
    )
