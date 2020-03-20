from GoogleTuring.Infrastructure.Models.GoogleFieldMetadata import GoogleFieldMetadata

AD_FIELDS = [
    GoogleFieldMetadata.ad_id,
    GoogleFieldMetadata.ad_name
]

AD_GROUP_FIELDS = [
    GoogleFieldMetadata.ad_group_name,
    GoogleFieldMetadata.ad_group_id,

    GoogleFieldMetadata.effective_target_roas
]

CAMPAIGN_FIELDS = [
    GoogleFieldMetadata.maximize_conversion_value_target_roas
]

BIDDING_FIELDS = [
    GoogleFieldMetadata.bidding_strategy_name,
    GoogleFieldMetadata.bidding_strategy_type
]

ENGAGEMENT_FIELDS = [
    GoogleFieldMetadata.engagement_rate,
    GoogleFieldMetadata.engagements
]



