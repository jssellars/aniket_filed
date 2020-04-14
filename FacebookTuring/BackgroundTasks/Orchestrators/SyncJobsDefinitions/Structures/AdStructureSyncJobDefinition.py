from Orchestrators import SyncJobDefinitionBase
from FacebookTuring.Infrastructure.Models.FieldsMetadataMetadata import FieldsMetadata


class AdStructureSyncJobDefinition(SyncJobDefinitionBase):

    level = "ads"

    fields = [
        FieldsMetadata.ad_account_id,
        FieldsMetadata.account_name,
        FieldsMetadata.ad_account_structure_name,
        FieldsMetadata.ad_account_structure_id,
        FieldsMetadata.campaign_structure_name,
        FieldsMetadata.campaign_structure_id,
        FieldsMetadata.adset_structure_name,
        FieldsMetadata.adset_structure_id,
        FieldsMetadata.name,
        FieldsMetadata.id,
        FieldsMetadata.bid_amount,
        FieldsMetadata.campaign,
        FieldsMetadata.configured_status,
        FieldsMetadata.created_at,
        FieldsMetadata.creative,
        FieldsMetadata.effective_status,
        FieldsMetadata.last_updated_by_app_id,
        FieldsMetadata.recommendations,
        FieldsMetadata.source_ad,
        FieldsMetadata.source_ad_id,
        FieldsMetadata.targetingsentencelines,
        FieldsMetadata.ad_creatives,
        FieldsMetadata.updated_time,
        FieldsMetadata.tracking_specs,
        FieldsMetadata.status,
        FieldsMetadata.ad_id
    ]
