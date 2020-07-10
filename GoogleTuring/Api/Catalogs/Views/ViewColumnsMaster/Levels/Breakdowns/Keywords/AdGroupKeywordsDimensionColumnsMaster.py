from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.DimensionColumnsBase import DimensionColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.DimensionColumnsMaster import DimensionColumnsMaster


class AdGroupKeywordsDimensionColumnsMaster(DimensionColumnsBase):
    DIMENSIONS = [
        DimensionColumnsMaster.account_currency_code,
        DimensionColumnsMaster.account_descriptive_name,
        DimensionColumnsMaster.account_time_zone,
        DimensionColumnsMaster.ad_group_id,
        DimensionColumnsMaster.ad_group_name,
        DimensionColumnsMaster.ad_group_status,
        DimensionColumnsMaster.approval_status,
        DimensionColumnsMaster.base_ad_group_id,
        DimensionColumnsMaster.base_campaign_id,
        DimensionColumnsMaster.bidding_strategy_id,
        DimensionColumnsMaster.bidding_strategy_name,
        DimensionColumnsMaster.bidding_strategy_source,
        DimensionColumnsMaster.bidding_strategy_type,
        DimensionColumnsMaster.campaign_id,
        DimensionColumnsMaster.campaign_name,
        DimensionColumnsMaster.campaign_status,
        DimensionColumnsMaster.conversion_adjustment,
        DimensionColumnsMaster.max_cpc,
        DimensionColumnsMaster.cpc_bid_source,
        DimensionColumnsMaster.cpm_bid,
        DimensionColumnsMaster.creative_quality_score,
        DimensionColumnsMaster.keywords,
        DimensionColumnsMaster.criteria_destination_url,
        DimensionColumnsMaster.customer_descriptive_name,
        DimensionColumnsMaster.enhanced_cpc_enabled,
        DimensionColumnsMaster.estimated_add_clicks_at_first_position_cpc,
        DimensionColumnsMaster.estimated_add_cost_at_first_position_cpc,
        DimensionColumnsMaster.external_customer_id,
        DimensionColumnsMaster.final_app_urls,
        DimensionColumnsMaster.final_mobile_urls,
        DimensionColumnsMaster.final_urls,
        DimensionColumnsMaster.final_url_suffix,
        DimensionColumnsMaster.first_page_cpc,
        DimensionColumnsMaster.first_position_cpc,
        DimensionColumnsMaster.has_quality_score,
        DimensionColumnsMaster.id,
        DimensionColumnsMaster.is_negative,
        DimensionColumnsMaster.keyword_match_type,
        DimensionColumnsMaster.label_ids,
        DimensionColumnsMaster.labels,
        DimensionColumnsMaster.post_click_quality_score,
        DimensionColumnsMaster.quality_score,
        DimensionColumnsMaster.search_predicted_ctr,
        DimensionColumnsMaster.status,
        DimensionColumnsMaster.system_serving_status,
        DimensionColumnsMaster.top_of_page_cpc,
        DimensionColumnsMaster.tracking_url_template,
        DimensionColumnsMaster.url_custom_parameters,
        DimensionColumnsMaster.vertical_id,
    ]