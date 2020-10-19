from Core.Tools.Misc.Enumeration import Enumeration
from Core.Tools.Misc.ObjectSerializers import object_to_attribute_values_list


class PixelsInsightsCatalogDto(Enumeration):
    browser_type = Enumeration(1, "browser_type", "Browser type")
    custom_data_field = Enumeration(2, "custom_data_field", "Custom data field")
    device_os = Enumeration(3, "device_os", "Device OS")
    device_type = Enumeration(4, "device_type", "Device type")
    event = Enumeration(5, "event", "Event")
    event_detection_method = Enumeration(6, "event_detection_method", "Event detection method")
    event_processing_results = Enumeration(7, "event_processing_results", "Event processing results")
    event_source = Enumeration(8, "event_source", "Event source")
    event_total_counts = Enumeration(9, "event_total_counts", "Event total counts")
    event_value_count = Enumeration(10, "event_value_count", "Event value count")
    had_pii = Enumeration(11, "had_pii", "Had PII")
    host = Enumeration(12, "host", "Host")
    match_keys = Enumeration(13, "match_keys", "Match keys")
    pixel_fire = Enumeration(14, "pixel_fire", "Pixel fire")
    url = Enumeration(15, "url", "URL")
    url_by_rule = Enumeration(16, "url_by_rule", "URL by rule")


class CustomConversionsInsightsCatalogDto(Enumeration):
    count = Enumeration(1, "count", "Count")
    device_type = Enumeration(2, "device_type", "Device type")
    host = Enumeration(3, "host", "Host")
    pixel_fire = Enumeration(4, "pixel_fire", "Pixel fire")
    unmatched_count = Enumeration(5, "unmatched_count", "Unmatched count")
    unmatched_usd_amount = Enumeration(6, "unmatched_usd_amount", "Unmatched USD amount")
    url = Enumeration(7, "url", "URL")
    url_amount = Enumeration(8, "usd_amount", "USD amount")


class PixelsInsightsCatalogsDto:
    pixels = object_to_attribute_values_list(PixelsInsightsCatalogDto())
    custom_conversions = object_to_attribute_values_list(CustomConversionsInsightsCatalogDto())
