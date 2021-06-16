from enum import Enum

from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import ApplyActionType
from FacebookDexter.Infrastructure.DexterRules.DexterOutput import DexterRecommendationOutput, RecommendationPriority


class DexterLabsTemplate(Enum):
    LOOKALIKE_AUDIENCE = DexterRecommendationOutput(
        analysis=(
            "We have identified a lookalike audience based on customers who have purchased from you recently using "
            "pixel ({pixel_id})"
        ),
        priority=RecommendationPriority.HIGH,
        title="Create a lookalike audience",
        subtext="Consider building a lookalike audience based of your most active users.",
        quote="Dexter recommends creating a lookalike audience of customers who have purchased from you recently.",
        apply_action_type=ApplyActionType.CREATE_LOOKALIKE,
    )
    HIDDEN_INTERESTS = DexterRecommendationOutput(
        analysis="Try using Hidden Interests to achieve cheaper conversions.",
        priority=RecommendationPriority.HIGH,
        title="Change Hidden Interest Targeting",
        subtext="Interests that aren’t available in Facebook Ads Manager.",
        quote="Dexter recommends experimenting with these hidden interests as they may result in cheaper conversions.",
        apply_action_type=ApplyActionType.HIDDEN_INTERESTS_DUPLICATE_ADSET,
    )
    NO_PURCHASE_30_DAYS_AUDIENCE = DexterRecommendationOutput(
        analysis="We have identified an audience likely to convert that you can build an Adset for.",
        priority=RecommendationPriority.HIGH,
        title="Create a retarget audience",
        subtext="Targeting an audience that reached your checkout but didn’t complete the purchase.",
        quote="Dexter recommends retargeting this audience because they are more likely to convert.",
        apply_action_type=ApplyActionType.CREATE_RETARGETING,
    )
