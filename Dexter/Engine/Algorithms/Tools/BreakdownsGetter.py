from Algorithms.Models.Types import TypesWrapper


def create_all_level_breakdown_combinations():
    all_data_types = []

    # TODO: make it global

    breakdowns = [
        "age_breakdown", "gender_breakdown", "country", "dma", "impression_device", "publisher_platform",
        "placement", "product_id", "frequency_value", "hourly_stats_aggregated_by_advertiser_time_zone",
        "hourly_stats_aggregated_by_audience_time_zone", "place_page_id", "platform_position",
        "device_platform", "age_gender", "platform_and_device", "placement_and_device", "region", "none"
    ]

    action_breakdowns = [
        "action_device", "action_canvas_component_name", "action_carousel_card_id", "action_carousel_card_name",
        "action_destination", "action_reaction", "action_target_id", "action_video_sound", "action_video_type", "none"
    ]

    for level in [TypesWrapper.LevelNames.Ad.value, TypesWrapper.LevelNames.AdSet.value, TypesWrapper.LevelNames.Campaign.value]:
        for breakdown in breakdowns:
            for action_breakdown in action_breakdowns:
                combination = TypesWrapper.OptimizationTuple(level, breakdown, action_breakdown)
                all_data_types.append(combination)
    return all_data_types
