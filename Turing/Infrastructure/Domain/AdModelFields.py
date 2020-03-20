from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata
from Turing.Infrastructure.Domain.StructureModelFieldsBase import StructureModelFieldBase


class AdModelFields(StructureModelFieldBase):
    """Lists of fields to sync from Facebook"""

    level = "ads"

    structure_fields = [
        FacebookFieldsMetadata.ad_account_id,
        FacebookFieldsMetadata.campaign_name,
        FacebookFieldsMetadata.campaign_id,
        FacebookFieldsMetadata.adset_name,
        FacebookFieldsMetadata.adset_id,
        FacebookFieldsMetadata.name,
        FacebookFieldsMetadata.id,
        FacebookFieldsMetadata.bid_amount,
        FacebookFieldsMetadata.campaign,
        FacebookFieldsMetadata.configured_status,
        FacebookFieldsMetadata.created_at,
        FacebookFieldsMetadata.creative,
        FacebookFieldsMetadata.effective_status,
        FacebookFieldsMetadata.last_updated_by_app_id,
        FacebookFieldsMetadata.recommendations,
        FacebookFieldsMetadata.source_ad,
        FacebookFieldsMetadata.source_ad_id,
        FacebookFieldsMetadata.targetingsentencelines,
        FacebookFieldsMetadata.ad_creatives,
        FacebookFieldsMetadata.updated_time,
        FacebookFieldsMetadata.tracking_specs,
        FacebookFieldsMetadata.status
    ]

    insights_fields = [
        FacebookFieldsMetadata.account_name,
        FacebookFieldsMetadata.ad_id
    ]