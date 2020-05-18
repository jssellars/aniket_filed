from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
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
