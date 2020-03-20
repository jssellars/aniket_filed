from Core.Tools.Misc.Autoincrement import Autoincrement
from Turing.Api.Catalogs.Breakdowns.BreakdownsEnumeration import BreakdownsEnumeration
from Turing.Infrastructure.Models.FacebookFieldsMetadata import FacebookFieldsMetadata

id = Autoincrement(0)


class DeliveryBreakdowns:
    age = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.age_breakdown.name, "Age")
    gender = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.gender_breakdown.name, "Gender")
    country = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.country.name, "Country")
    dma = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.dma.name, "DMA Region")
    impression_device = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.impression_device.name, "Impression device")
    publisher_platform = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.publisher_platform.name, "Publisher platform")
    placement = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.placement.name, "Placement")
    product_id = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.product_id.name, "Product")
    frequency_value = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.frequency_value.name, "Frequency value")
    hourly_stats_aggregated_by_advertiser_time_zone = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.hourly_stats_aggregated_by_advertiser_time_zone.name, "Time of the day (ad account time zone)")
    hourly_stats_aggregated_by_audience_time_zone = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.hourly_stats_aggregated_by_audience_time_zone.name, "Time of the day (viwer's time zone)")
    business_locations = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.business_locations.name, "Business locations")
    platform_position = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.platform_position.name, "Platform position")
    device_platform = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.device_platform.name, "Device platform")
    age_gender = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.age_gender.name, "Age and gender")
    platform_and_device = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.platform_and_device.name, "Platform and device")
    placement_and_device = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.placement_and_device.name, "Placement and device")
    region = BreakdownsEnumeration(id.increment(), FacebookFieldsMetadata.region.name, "Region")
