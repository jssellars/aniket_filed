from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Infrastructure.Domain.StructureModelFieldsBase import StructureModelFieldBase


class CampaignModelFields(StructureModelFieldBase):
    """Lists of fields to sync from Facebook"""

    level = "campaigns"

    structure_fields = [
        FieldsMetadata.ad_account_structure_id,
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
        FieldsMetadata.copies
    ]

    insights_fields = [
        FieldsMetadata.account_name,
        FieldsMetadata.account_id,
        FieldsMetadata.campaign_id,
        FieldsMetadata.campaign_name
    ]
