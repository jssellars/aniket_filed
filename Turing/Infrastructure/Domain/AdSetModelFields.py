from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata
from Turing.Infrastructure.Domain.StructureModelFieldsBase import StructureModelFieldBase


class AdSetModelFields(StructureModelFieldBase):
    """Lists of fields to sync from Facebook"""

    level = "adsets"

    structure_fields = [
        FacebookFieldsMetadata.ad_account_structure_id,
        FacebookFieldsMetadata.campaign_name,
        FacebookFieldsMetadata.campaign_id,
        FacebookFieldsMetadata.name,
        FacebookFieldsMetadata.id,
        FacebookFieldsMetadata.ad_labels,
        FacebookFieldsMetadata.adset_schedule,
        FacebookFieldsMetadata.asset_feed_id,
        FacebookFieldsMetadata.attribution_spec,
        FacebookFieldsMetadata.bid_adjustments,
        FacebookFieldsMetadata.bid_constraints,
        FacebookFieldsMetadata.bid_amount,
        FacebookFieldsMetadata.bid_info,
        FacebookFieldsMetadata.bid_strategy,
        FacebookFieldsMetadata.billing_event,
        FacebookFieldsMetadata.budget_remaining,
        FacebookFieldsMetadata.campaign,
        FacebookFieldsMetadata.configured_status,
        FacebookFieldsMetadata.created_at,
        FacebookFieldsMetadata.daily_budget,
        FacebookFieldsMetadata.daily_min_spend_target,
        FacebookFieldsMetadata.daily_spend_cap,
        FacebookFieldsMetadata.destination_type,
        FacebookFieldsMetadata.effective_status,
        FacebookFieldsMetadata.end_time,
        FacebookFieldsMetadata.frequency_control_specs,
        FacebookFieldsMetadata.instagram_actor_id,
        FacebookFieldsMetadata.is_dynamic_creative,
        FacebookFieldsMetadata.issues_info,
        FacebookFieldsMetadata.lifetime_budget,
        FacebookFieldsMetadata.lifetime_imps,
        FacebookFieldsMetadata.lifetime_spend_cap,
        FacebookFieldsMetadata.lifetime_min_spend_target,
        FacebookFieldsMetadata.name,
        FacebookFieldsMetadata.optimization_goal,
        FacebookFieldsMetadata.optimization_sub_event,
        FacebookFieldsMetadata.pacing_type,
        FacebookFieldsMetadata.promoted_object,
        FacebookFieldsMetadata.source_adset,
        FacebookFieldsMetadata.source_adset_id,
        FacebookFieldsMetadata.start_date,
        FacebookFieldsMetadata.status,
        FacebookFieldsMetadata.targeting,
        FacebookFieldsMetadata.time_based_ad_rotation_intervals,
        FacebookFieldsMetadata.time_based_ad_rotation_id_blocks,
        FacebookFieldsMetadata.use_new_app_click,
        FacebookFieldsMetadata.lifetime_min_spend_target,
        FacebookFieldsMetadata.ad_rules_governed,
        FacebookFieldsMetadata.targetingsentencelines,
        FacebookFieldsMetadata.amount_spent,
    ]

    insights_fields = [
        FacebookFieldsMetadata.ad_account_id,
        FacebookFieldsMetadata.account_name,
        FacebookFieldsMetadata.adset_id
    ]