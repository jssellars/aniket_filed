from Core.Tools.Misc.Autoincrement import Autoincrement
from FacebookTuring.Api.Catalogs.Breakdowns.BreakdownsEnumeration import BreakdownsEnumeration
from FacebookTuring.Infrastructure.Models.FacebookFieldsMetadata import FieldsMetadata

id = Autoincrement(0)


class DeliveryBreakdowns:
    age = BreakdownsEnumeration(id.increment(), FieldsMetadata.age_breakdown.name, "Age")
    gender = BreakdownsEnumeration(id.increment(), FieldsMetadata.gender_breakdown.name, "Gender")
    country = BreakdownsEnumeration(id.increment(), FieldsMetadata.country.name, "Country")
    dma = BreakdownsEnumeration(id.increment(), FieldsMetadata.dma.name, "DMA Region")
    impression_device = BreakdownsEnumeration(id.increment(), FieldsMetadata.impression_device.name, "Impression device")
    publisher_platform = BreakdownsEnumeration(id.increment(), FieldsMetadata.publisher_platform.name, "Publisher platform")
    placement = BreakdownsEnumeration(id.increment(), FieldsMetadata.placement.name, "Placement")
    product_id = BreakdownsEnumeration(id.increment(), FieldsMetadata.product_id.name, "Product")
    frequency_value = BreakdownsEnumeration(id.increment(), FieldsMetadata.frequency_value.name, "Frequency value")
    hourly_stats_aggregated_by_advertiser_time_zone = BreakdownsEnumeration(id.increment(), FieldsMetadata.hourly_stats_aggregated_by_advertiser_time_zone.name, "Time of the day (ad account time zone)")
    hourly_stats_aggregated_by_audience_time_zone = BreakdownsEnumeration(id.increment(), FieldsMetadata.hourly_stats_aggregated_by_audience_time_zone.name, "Time of the day (viwer's time zone)")
    business_locations = BreakdownsEnumeration(id.increment(), FieldsMetadata.business_locations.name, "Business locations")
    platform_position = BreakdownsEnumeration(id.increment(), FieldsMetadata.platform_position.name, "Platform position")
    device_platform = BreakdownsEnumeration(id.increment(), FieldsMetadata.device_platform.name, "Device platform")
    age_gender = BreakdownsEnumeration(id.increment(), FieldsMetadata.age_gender.name, "Age and gender")
    platform_and_device = BreakdownsEnumeration(id.increment(), FieldsMetadata.platform_and_device.name, "Platform and device")
    placement_and_device = BreakdownsEnumeration(id.increment(), FieldsMetadata.placement_and_device.name, "Placement and device")
    region = BreakdownsEnumeration(id.increment(), FieldsMetadata.region.name, "Region")
