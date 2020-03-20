from Orchestrators import SyncJobDefinitionBase
from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata


class CampaignStructureSyncJobDefinition(SyncJobDefinitionBase):

    level = "campaigns"

    fields = [
        FacebookFieldsMetadata.ad_account_id,
        FacebookFieldsMetadata.account_name,
        FacebookFieldsMetadata.ad_account_structure_id,
        FacebookFieldsMetadata.ad_account_structure_name,
        FacebookFieldsMetadata.id,
        FacebookFieldsMetadata.name,
        FacebookFieldsMetadata.bid_strategy,
        FacebookFieldsMetadata.ad_labels,
        FacebookFieldsMetadata.boosted_object_id,
        FacebookFieldsMetadata.brand_lift_studies,
        FacebookFieldsMetadata.budget_rebalance_flag,
        FacebookFieldsMetadata.budget_remaining,
        FacebookFieldsMetadata.buying_type,
        FacebookFieldsMetadata.can_create_brand_lift_study,
        FacebookFieldsMetadata.configured_status,
        FacebookFieldsMetadata.created_at,
        FacebookFieldsMetadata.can_use_spend_cap,
        FacebookFieldsMetadata.daily_budget,
        FacebookFieldsMetadata.effective_status,
        FacebookFieldsMetadata.last_budget_toggling_time,
        FacebookFieldsMetadata.lifetime_budget,
        FacebookFieldsMetadata.objective_structure,
        FacebookFieldsMetadata.pacing_type,
        FacebookFieldsMetadata.recommendations,
        FacebookFieldsMetadata.promoted_object,
        FacebookFieldsMetadata.source_campaign,
        FacebookFieldsMetadata.special_ad_category,
        FacebookFieldsMetadata.source_campaign_id,
        FacebookFieldsMetadata.spend_cap,
        FacebookFieldsMetadata.start_date,
        FacebookFieldsMetadata.status,
        FacebookFieldsMetadata.end_date,
        FacebookFieldsMetadata.top_line_id,
        FacebookFieldsMetadata.updated_time,
        FacebookFieldsMetadata.ad_rules_governed,
        FacebookFieldsMetadata.copies,
        FacebookFieldsMetadata.campaign_id
    ]
