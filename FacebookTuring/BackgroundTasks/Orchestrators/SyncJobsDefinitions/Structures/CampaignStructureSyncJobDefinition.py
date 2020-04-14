from Orchestrators import SyncJobDefinitionBase
from FacebookTuring.Infrastructure.Models.FieldsMetadataMetadata import FieldsMetadata


class CampaignStructureSyncJobDefinition(SyncJobDefinitionBase):

    level = "campaigns"

    fields = [
        FieldsMetadata.ad_account_id,
        FieldsMetadata.account_name,
        FieldsMetadata.ad_account_structure_id,
        FieldsMetadata.ad_account_structure_name,
        FieldsMetadata.id,
        FieldsMetadata.name,
        FieldsMetadata.bid_strategy,
        FieldsMetadata.ad_labels,
        FieldsMetadata.boosted_object_id,
        FieldsMetadata.brand_lift_studies,
        FieldsMetadata.budget_rebalance_flag,
        FieldsMetadata.budget_remaining,
        FieldsMetadata.buying_type,
        FieldsMetadata.can_create_brand_lift_study,
        FieldsMetadata.configured_status,
        FieldsMetadata.created_at,
        FieldsMetadata.can_use_spend_cap,
        FieldsMetadata.daily_budget,
        FieldsMetadata.effective_status,
        FieldsMetadata.last_budget_toggling_time,
        FieldsMetadata.lifetime_budget,
        FieldsMetadata.objective_structure,
        FieldsMetadata.pacing_type,
        FieldsMetadata.recommendations,
        FieldsMetadata.promoted_object,
        FieldsMetadata.source_campaign,
        FieldsMetadata.special_ad_category,
        FieldsMetadata.source_campaign_id,
        FieldsMetadata.spend_cap,
        FieldsMetadata.start_date,
        FieldsMetadata.status,
        FieldsMetadata.end_date,
        FieldsMetadata.top_line_id,
        FieldsMetadata.updated_time,
        FieldsMetadata.ad_rules_governed,
        FieldsMetadata.copies,
        FieldsMetadata.campaign_id
    ]
