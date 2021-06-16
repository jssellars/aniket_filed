from enum import Enum

from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import ApplyActionType
from FacebookDexter.Infrastructure.DexterRules.DexterOutput import DexterRecommendationOutput, RecommendationPriority


class DexterLabsTemplate(Enum):
    LOOKALIKE_AUDIENCE = DexterRecommendationOutput(
        analysis="We have identified a lookalike audience based on your most active users using (pixel {pixel_id})",
        priority=RecommendationPriority.HIGH,
        title="Create a lookalike audience",
        subtext="Consider building a lookalike audience based of your most active users.",
        quote="Dexter suggests creating a lookalike audience to get even more results",
        apply_action_type=ApplyActionType.CREATE_LOOKALIKE,
    )
    HIDDEN_INTERESTS = DexterRecommendationOutput(
        analysis="",
        priority=RecommendationPriority.HIGH,
        title="Hidden Interests",
        subtext="Change Interests",
        quote="Dexter suggests changing interests",
        apply_action_type=ApplyActionType.HIDDEN_INTERESTS_DUPLICATE_ADSET,
    )
    NO_PURCHASE_30_DAYS_AUDIENCE = DexterRecommendationOutput(
        "We have identified an audience likely to convert that you can build an Adset for.",
        RecommendationPriority.HIGH,
        "Create a retarget audience",
        "We have identified an audience likely to convert that you can build an Adset for.",
        "Dexter suggests building a new Adset to target this audience.",
        apply_action_type=ApplyActionType.CREATE_RETARGETING,
    )
