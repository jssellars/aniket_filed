from enum import Enum

from FacebookDexter.Infrastructure.DexterApplyActions.ApplyTypes import ApplyActionType
from FacebookDexter.Infrastructure.DexterRules.DexterOutput import DexterRecommendationOutput, RecommendationPriority


class DexterLabsTemplate(Enum):
    LOOKALIKE_AUDIENCE = DexterRecommendationOutput(
        analysis="Creating an audience similar to your most active customers",
        priority=RecommendationPriority.HIGH,
        title="Create a Lookalike Audience",
        subtext="",
        quote=(
            "Dexter recommends creating a lookalike audience of customers (using pixel {pixel_id}) who have purchased "
            "from you recently and targeting them in this campaign."
        ),
        apply_action_type=ApplyActionType.CREATE_LOOKALIKE,
    )
    HIDDEN_INTERESTS = DexterRecommendationOutput(
        analysis="Interests that aren’t available in Facebook Ads Manager",
        priority=RecommendationPriority.HIGH,
        title="Change Hidden Interest Targeting",
        subtext="",
        quote="Dexter recommends experimenting with these hidden interests as they may result in cheaper conversions.",
        apply_action_type=ApplyActionType.HIDDEN_INTERESTS_DUPLICATE_ADSET,
    )
    NO_PURCHASE_30_DAYS_AUDIENCE = DexterRecommendationOutput(
        analysis="Targeting an audience that reached your checkout but didn’t complete the purchase",
        priority=RecommendationPriority.HIGH,
        title="Create a Retarget Audience",
        subtext="",
        quote="Dexter recommends retargeting this audience because they are more likely to convert.",
        apply_action_type=ApplyActionType.CREATE_RETARGETING,
    )
