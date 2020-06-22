from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.DimensionColumnsBase import DimensionColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.DimensionColumnsMaster import DimensionColumnsMaster


class CampaignAgeRangeDimensionColumnsMaster(DimensionColumnsBase):
    DIMENSIONS = [
        DimensionColumnsMaster.account_currency_code,
        DimensionColumnsMaster.account_descriptive_name,
        DimensionColumnsMaster.account_time_zone,
        DimensionColumnsMaster.base_campaign_id,
        DimensionColumnsMaster.bidding_strategy_id,
        DimensionColumnsMaster.bidding_strategy_name,
        DimensionColumnsMaster.bidding_strategy_type,
        DimensionColumnsMaster.bid_modifier,
        DimensionColumnsMaster.campaign_id,
        DimensionColumnsMaster.campaign_name,
        DimensionColumnsMaster.campaign_status,
        DimensionColumnsMaster.cpc_bid,
        DimensionColumnsMaster.cpc_bid_source,
        DimensionColumnsMaster.cpm_bid,
        DimensionColumnsMaster.cpm_bid_source,
        DimensionColumnsMaster.age_range,
        DimensionColumnsMaster.criteria_destination_url,
        DimensionColumnsMaster.customer_descriptive_name,
        DimensionColumnsMaster.external_customer_id,
        DimensionColumnsMaster.final_app_urls,
        DimensionColumnsMaster.final_mobile_urls,
        DimensionColumnsMaster.final_urls,
        DimensionColumnsMaster.id,
        DimensionColumnsMaster.is_negative,
        DimensionColumnsMaster.is_restrict,
        DimensionColumnsMaster.status,
        DimensionColumnsMaster.tracking_url_template,
        DimensionColumnsMaster.url_custom_parameters,
    ]
