from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata
from Orchestrators.SyncJobsDefinitions.SyncJobDefinitionBase import SyncJobDefinitionBase


class AdInsightsSyncJobDefinition(SyncJobDefinitionBase):

    level = "ad"

    fields = [
        FacebookFieldsMetadata.ad_account_id,
        FacebookFieldsMetadata.account_name,
        FacebookFieldsMetadata.campaign_name,
        FacebookFieldsMetadata.campaign_id,
        FacebookFieldsMetadata.adset_name,
        FacebookFieldsMetadata.adset_id,
        FacebookFieldsMetadata.ad_name,
        FacebookFieldsMetadata.ad_id,
        FacebookFieldsMetadata.date_start,
        FacebookFieldsMetadata.date_stop,
        FacebookFieldsMetadata.all_cpc,
        FacebookFieldsMetadata.cpm,
        FacebookFieldsMetadata.all_cpp,
        FacebookFieldsMetadata.amount_spent,
        FacebookFieldsMetadata.reach,
        FacebookFieldsMetadata.link_click,
        FacebookFieldsMetadata.impressions,
        FacebookFieldsMetadata.all_ctr,
        FacebookFieldsMetadata.results,
        FacebookFieldsMetadata.conversions,
        FacebookFieldsMetadata.objective,
        FacebookFieldsMetadata.all_clicks,
        FacebookFieldsMetadata.frequency,
        FacebookFieldsMetadata.website_purchase_roas,
        FacebookFieldsMetadata.purchase_roas,
        FacebookFieldsMetadata.estimated_ad_recall_lift,
        FacebookFieldsMetadata.estimated_ad_recall_rate,
        FacebookFieldsMetadata.conversion_rate_ranking,
        FacebookFieldsMetadata.engagement_rate_ranking,
        FacebookFieldsMetadata.quality_ranking,
        FacebookFieldsMetadata.bid_amount,
        FacebookFieldsMetadata.bid_strategy,
        FacebookFieldsMetadata.bid_info,
        FacebookFieldsMetadata.bid_cap
    ]

    breakdowns = [
        FacebookFieldsMetadata.age_breakdown,
        FacebookFieldsMetadata.gender_breakdown,
        FacebookFieldsMetadata.age_gender,
        FacebookFieldsMetadata.country,
        FacebookFieldsMetadata.impression_device,
        FacebookFieldsMetadata.placement,
        FacebookFieldsMetadata.placement_and_device
    ]

    action_breakdowns = [
        FacebookFieldsMetadata.destination_breakdown,
        FacebookFieldsMetadata.device,
        FacebookFieldsMetadata.reaction
    ]

    time_breakdowns = [
        FacebookFieldsMetadata.day
    ]


