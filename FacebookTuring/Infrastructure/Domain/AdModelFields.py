from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Infrastructure.Domain.MiscFieldsEnum import MiscFieldsEnum
from FacebookTuring.Infrastructure.Domain.StructureModelFieldsBase import StructureModelFieldBase


class AdModelFields(StructureModelFieldBase):
    """Lists of fields to sync from Facebook"""

    level = "ads"

    structure_fields = [
        FieldsMetadata.account_id,
        FieldsMetadata.campaign_structure_name,
        FieldsMetadata.campaign_id,
        FieldsMetadata.adset_structure_name,
        FieldsMetadata.adset_id,
        FieldsMetadata.name,
        FieldsMetadata.id,
        FieldsMetadata.bid_amount,
        # FieldsMetadata.campaign,
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
        FieldsMetadata.status
    ]

    insights_fields = [
        FieldsMetadata.account_name,
        FieldsMetadata.ad_id
    ]

    required_structure_fields = [
        #base structure fields
        FieldsMetadata.account_id,
        FieldsMetadata.campaign_name,
        FieldsMetadata.campaign_id,
        FieldsMetadata.adset_name,
        FieldsMetadata.adset_id,
        FieldsMetadata.ad_name,
        FieldsMetadata.ad_id,
        MiscFieldsEnum.last_updated_at,
        MiscFieldsEnum.actions,
        FieldsMetadata.status,
        GraphAPIInsightsFields.created_time,
        FieldsMetadata.start_date,
        MiscFieldsEnum.end_time,
        MiscFieldsEnum.date_added,
        #details structure fields
        FieldsMetadata.daily_budget,
        FieldsMetadata.lifetime_budget,
        FieldsMetadata.headline,
        FieldsMetadata.body,
        FieldsMetadata.destination,
        FieldsMetadata.link,
        FieldsMetadata.page_name,
        FieldsMetadata.bid_strategy,
        FieldsMetadata.last_significant_edit,
    ]
