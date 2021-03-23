from enum import Enum

from facebook_business.adobjects.ad import Ad


class FacebookEditField:
    class Ad(Enum):
        ad_name = Ad.Field.name
        ad_labels = Ad.Field.adlabels
        audience_id = Ad.Field.audience_id
        bid_amount = Ad.Field.bid_amount
        ad_creative = Ad.Field.creative
        display_sequence = Ad.Field.display_sequence
        draft_ad_group_id = Ad.Field.draft_adgroup_id
        engagement_audience = Ad.Field.engagement_audience
        execution_options = Ad.Field.execution_options
        status = Ad.Field.status
        tracking_specs = Ad.Field.tracking_specs
