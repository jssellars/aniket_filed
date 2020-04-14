from FacebookTuring.Infrastructure.Models.FieldsMetadataMetadata import FieldsMetadata
from Orchestrators.SyncJobsDefinitions.SyncJobDefinitionBase import SyncJobDefinitionBase


class CampaignInsightsSyncJobDefinition(SyncJobDefinitionBase):

    level = "campaign"

    fields = [
        FieldsMetadata.ad_account_id,
        FieldsMetadata.account_name,
        FieldsMetadata.campaign_name,
        FieldsMetadata.campaign_id,
        FieldsMetadata.date_start,
        FieldsMetadata.date_stop,
        FieldsMetadata.all_cpc,
        FieldsMetadata.cpm,
        FieldsMetadata.all_cpp,
        FieldsMetadata.amount_spent,
        FieldsMetadata.reach,
        FieldsMetadata.link_click,
        FieldsMetadata.impressions,
        FieldsMetadata.all_ctr,
        FieldsMetadata.results,
        FieldsMetadata.conversions,
        FieldsMetadata.objective,
        FieldsMetadata.all_clicks,
        FieldsMetadata.frequency,
        FieldsMetadata.website_purchase_roas,
        FieldsMetadata.purchase_roas,
        FieldsMetadata.estimated_ad_recall_lift,
        FieldsMetadata.estimated_ad_recall_rate,
        FieldsMetadata.conversion_rate_ranking,
        FieldsMetadata.engagement_rate_ranking,
        FieldsMetadata.quality_ranking,
        FieldsMetadata.bid_amount,
        FieldsMetadata.bid_strategy,
        FieldsMetadata.bid_info,
        FieldsMetadata.bid_cap
    ]

    breakdowns = [
        FieldsMetadata.age_gender,
        FieldsMetadata.age_breakdown,
        FieldsMetadata.gender_breakdown,
        FieldsMetadata.country,
        FieldsMetadata.impression_device,
        FieldsMetadata.placement,
        FieldsMetadata.placement_and_device
    ]

    action_breakdowns = [
        FieldsMetadata.destination_breakdown,
        FieldsMetadata.device,
        FieldsMetadata.reaction
    ]

    time_breakdowns = [
        FieldsMetadata.day
    ]


