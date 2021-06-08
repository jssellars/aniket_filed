from enum import Enum

from FacebookDexter.Infrastructure.DexterRules.DexterOutput import DexterRecommendationOutput, RecommendationPriority


class DexterLabsTemplate(Enum):
    LOOKALIKE_AUDIENCE = DexterRecommendationOutput(
        "We have identified a lookalike audience based on your most active users using (pixel {pixel_id}) for campaign: {campaign_name}",
        RecommendationPriority.HIGH,
        "Create a lookalike audience",
        "Consider building a lookalike audience based of your most active users.",
        "Dexter suggests creating a lookalike audience to get even more results",
    )
