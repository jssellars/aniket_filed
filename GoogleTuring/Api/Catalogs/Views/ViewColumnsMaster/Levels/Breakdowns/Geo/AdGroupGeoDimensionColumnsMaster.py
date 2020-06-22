from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.DimensionColumnsBase import DimensionColumnsBase
from GoogleTuring.Api.Catalogs.Views.ViewColumnsMaster.DimensionColumnsMaster import DimensionColumnsMaster


class AdGroupGeoDimensionColumnsMaster(DimensionColumnsBase):
    DIMENSIONS = [
        DimensionColumnsMaster.account_currency_code,
        DimensionColumnsMaster.account_descriptive_name,
        DimensionColumnsMaster.account_time_zone,
        DimensionColumnsMaster.campaign_id,
        DimensionColumnsMaster.campaign_name,
        DimensionColumnsMaster.campaign_status,
        DimensionColumnsMaster.city_name,
        DimensionColumnsMaster.country_name,
        DimensionColumnsMaster.customer_descriptive_name,
        DimensionColumnsMaster.external_customer_id,
        DimensionColumnsMaster.is_targeting_location,
        DimensionColumnsMaster.metro_criteria_id,
        DimensionColumnsMaster.most_specific_criteria_id,
        DimensionColumnsMaster.region_name,
    ]
