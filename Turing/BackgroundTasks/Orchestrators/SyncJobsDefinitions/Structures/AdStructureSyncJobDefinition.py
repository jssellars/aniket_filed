from Orchestrators import SyncJobDefinitionBase
from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata


class AdStructureSyncJobDefinition(SyncJobDefinitionBase):

    level = "ads"

    fields = [
        FacebookFieldsMetadata.ad_account_id,
        FacebookFieldsMetadata.account_name,
        FacebookFieldsMetadata.ad_account_structure_name,
        FacebookFieldsMetadata.ad_account_structure_id,
        FacebookFieldsMetadata.campaign_structure_name,
        FacebookFieldsMetadata.campaign_structure_id,
        FacebookFieldsMetadata.adset_structure_name,
        FacebookFieldsMetadata.adset_structure_id,
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
        FacebookFieldsMetadata.status,
        FacebookFieldsMetadata.ad_id
    ]
