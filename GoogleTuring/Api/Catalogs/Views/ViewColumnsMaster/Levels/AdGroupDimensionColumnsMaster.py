from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.DimensionColumnsBase import DimensionColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.DimensionColumnsMaster import DimensionColumnsMaster


class AdGroupDimensionColumnsMaster(DimensionColumnsBase):
    DIMENSIONS = [
        DimensionColumnsMaster.account_currency_code,
        DimensionColumnsMaster.account_descriptive_name,
        DimensionColumnsMaster.account_time_zone,
        DimensionColumnsMaster.ad_group_desktop_bid_modifier,
        DimensionColumnsMaster.ad_group_id,
        DimensionColumnsMaster.ad_group_mobile_bid_modifier,
        DimensionColumnsMaster.ad_group_name,
        DimensionColumnsMaster.ad_group_status,
        DimensionColumnsMaster.ad_group_tablet_bid_modifier,
        DimensionColumnsMaster.ad_group_type,
        DimensionColumnsMaster.ad_rotation_mode,
        DimensionColumnsMaster.base_ad_group_id,
        DimensionColumnsMaster.base_campaign_id,
        DimensionColumnsMaster.bidding_strategy_id,
        DimensionColumnsMaster.bidding_strategy_name,
        DimensionColumnsMaster.bidding_strategy_source,
        DimensionColumnsMaster.bidding_strategy_type,
        DimensionColumnsMaster.campaign_id,
        DimensionColumnsMaster.campaign_name,
        DimensionColumnsMaster.campaign_status,
        DimensionColumnsMaster.content_bid_criterion_type_group,
        DimensionColumnsMaster.conversion_adjustment,
        DimensionColumnsMaster.cpc_bid,
        DimensionColumnsMaster.cpm_bid,
        DimensionColumnsMaster.cpv_bid,
        DimensionColumnsMaster.customer_descriptive_name,
        DimensionColumnsMaster.effective_target_roas,
        DimensionColumnsMaster.effective_target_roas_source,
        DimensionColumnsMaster.enhanced_cpc_enabled,
        DimensionColumnsMaster.external_customer_id,
        DimensionColumnsMaster.final_url_suffix,
        DimensionColumnsMaster.label_ids,
        DimensionColumnsMaster.labels,
        DimensionColumnsMaster.target_cpa,
        DimensionColumnsMaster.target_cpa_bid_source,
        DimensionColumnsMaster.tracking_url_template,
        DimensionColumnsMaster.url_custom_parameters,
    ]