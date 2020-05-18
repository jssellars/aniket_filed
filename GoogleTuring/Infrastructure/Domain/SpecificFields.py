from GoogleTuring.Infrastructure.Domain.GoogleFieldsMetadata import GoogleFieldsMetadata

AD_FIELDS = [
    GoogleFieldsMetadata.ad_id,
    GoogleFieldsMetadata.ad_name
]

AD_GROUP_FIELDS = [
    GoogleFieldsMetadata.ad_group_name,
    GoogleFieldsMetadata.ad_group_id,

    # GoogleFieldMetadata.effective_target_roas
]

CAMPAIGN_FIELDS = [
    GoogleFieldsMetadata.maximize_conversion_value_target_roas
]

BIDDING_FIELDS = [
    GoogleFieldsMetadata.bidding_strategy_name,
    GoogleFieldsMetadata.bidding_strategy_type
]

ENGAGEMENT_FIELDS = [
    # GoogleFieldMetadata.engagement_rate,
    GoogleFieldsMetadata.engagements
]
