from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Infrastructure.Domain.StructureModelFieldsBase import StructureModelFieldBase


class AdSetModelFields(StructureModelFieldBase):
    """Lists of fields to sync from Facebook"""

    level = "adsets"

    structure_fields = [
        FieldsMetadata.ad_account_structure_id,
        FieldsMetadata.campaign_structure_name,
        FieldsMetadata.campaign_id,
        FieldsMetadata.name,
        FieldsMetadata.id,
        FieldsMetadata.ad_labels,
        FieldsMetadata.adset_schedule,
        FieldsMetadata.asset_feed_id,
        FieldsMetadata.attribution_spec,
        FieldsMetadata.bid_adjustments,
        FieldsMetadata.bid_constraints,
        FieldsMetadata.bid_amount,
        FieldsMetadata.bid_info,
        FieldsMetadata.bid_strategy,
        FieldsMetadata.billing_event,
        FieldsMetadata.budget_remaining,
        # FieldsMetadata.campaign,
        FieldsMetadata.configured_status,
        FieldsMetadata.created_at,
        FieldsMetadata.daily_budget,
        FieldsMetadata.daily_min_spend_target,
        FieldsMetadata.daily_spend_cap,
        FieldsMetadata.destination_type,
        FieldsMetadata.effective_status,
        FieldsMetadata.end_time,
        FieldsMetadata.frequency_control_specs,
        FieldsMetadata.instagram_actor_id,
        FieldsMetadata.is_dynamic_creative,
        FieldsMetadata.issues_info,
        FieldsMetadata.lifetime_budget,
        FieldsMetadata.lifetime_imps,
        FieldsMetadata.lifetime_spend_cap,
        FieldsMetadata.lifetime_min_spend_target,
        FieldsMetadata.optimization_goal,
        FieldsMetadata.optimization_sub_event,
        FieldsMetadata.pacing_type,
        FieldsMetadata.promoted_object,
        FieldsMetadata.source_adset,
        FieldsMetadata.source_adset_id,
        FieldsMetadata.start_date,
        FieldsMetadata.status,
        FieldsMetadata.targeting,
        FieldsMetadata.time_based_ad_rotation_intervals,
        FieldsMetadata.time_based_ad_rotation_id_blocks,
        FieldsMetadata.use_new_app_click,
        FieldsMetadata.lifetime_min_spend_target,
        FieldsMetadata.ad_rules_governed,
        FieldsMetadata.targetingsentencelines,
        FieldsMetadata.amount_spent
    ]

    insights_fields = [
        FieldsMetadata.account_id,
        FieldsMetadata.account_name,
        FieldsMetadata.adset_id
    ]
