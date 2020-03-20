from Turing.Api.Catalogs.Breakdowns.ActionBreakdowns import ActionBreakdowns
from Turing.Api.Catalogs.Breakdowns.DeliveryBreakdowns import DeliveryBreakdowns


class BreakdownsCombinationsEnumeration:

    def __init__(self, delivery_breakdown_id, action_breakdown_id):
        self.delivery_breakdown_id = delivery_breakdown_id
        self.action_breakdown_id = action_breakdown_id


class BreakdownsCombinations:

    combinations = [
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.age.id, ActionBreakdowns.destination.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.age.id, ActionBreakdowns.video_type.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.age.id, ActionBreakdowns.carouse_card_id.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.gender.id, ActionBreakdowns.destination.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.gender.id, ActionBreakdowns.video_type.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.gender.id, ActionBreakdowns.carouse_card_id.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.age_gender.id, ActionBreakdowns.destination.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.age_gender.id, ActionBreakdowns.video_type.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.age_gender.id, ActionBreakdowns.carouse_card_id.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.country.id, ActionBreakdowns.destination.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.country.id, ActionBreakdowns.video_type.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.country.id, ActionBreakdowns.carouse_card_id.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.region.id, ActionBreakdowns.destination.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.region.id, ActionBreakdowns.video_type.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.dma.id, ActionBreakdowns.destination.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.dma.id, ActionBreakdowns.video_type.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.impression_device.id, ActionBreakdowns.device.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.device_platform.id, ActionBreakdowns.device.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.platform_and_device.id, ActionBreakdowns.device.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.platform_and_device.id, ActionBreakdowns.destination.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.platform_and_device.id, ActionBreakdowns.video_type.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.placement.id, ActionBreakdowns.device.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.placement.id, ActionBreakdowns.destination.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.placement.id, ActionBreakdowns.video_type.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.placement.id, ActionBreakdowns.carouse_card_id.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.placement_and_device.id, ActionBreakdowns.device.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.placement_and_device.id, ActionBreakdowns.destination.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.placement_and_device.id, ActionBreakdowns.video_type.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.placement_and_device.id, ActionBreakdowns.carouse_card_id.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.product_id.id, ActionBreakdowns.destination.id),
        BreakdownsCombinationsEnumeration(DeliveryBreakdowns.product_id.id, ActionBreakdowns.video_type.id)
    ]