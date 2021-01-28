from copy import deepcopy
from typing import List

from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.reachfrequencyprediction import ReachFrequencyPrediction

from Core.facebook.sdk_adapter.ad_objects.campaign import Objective, BidStrategy
from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform
from Core.facebook.sdk_adapter.catalog_models import Contexts
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.smart_create.structures import CampaignSplit
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.smart_create.targeting import Location


def build_campaigns(step_one, step_two, step_four) -> List[CampaignSplit]:
    campaign_template = {}

    build_base_campaign(campaign_template, step_one)

    budget_opt = None
    if "campaign_budget_optimization" in step_one:
        budget_opt = step_one["campaign_budget_optimization"]
    elif "budget_optimization" in step_two:
        budget_opt = step_two["budget_optimization"]

    if budget_opt:
        set_budget_optimization(campaign_template, budget_opt)

    return split_campaigns(campaign_template, step_four, step_two)


def build_base_campaign(campaign_template, step_one):
    # TODO: Paused just for testing purposes
    campaign_template[Campaign.Field.status] = Campaign.Status.paused
    campaign_template[Campaign.Field.effective_status] = Campaign.EffectiveStatus.paused

    campaign_template[Campaign.Field.name] = step_one["name"]
    campaign_template[Campaign.Field.objective] = Objective[step_one["objective"]].value.name_sdk

    campaign_template[Campaign.Field.buying_type] = step_one.get(
        "buying_type", ReachFrequencyPrediction.BuyingType.auction
    )

    # Set special ad categories (only one selected)
    special_ad_categories = []
    if "special_ad_category" in step_one:
        special_ad_categories.append(step_one["special_ad_category"])

    campaign_template[Campaign.Field.special_ad_categories] = special_ad_categories


def set_budget_optimization(campaign_template, budget_opt):
    amount = int(budget_opt["amount"]) * 100
    if budget_opt["budget_allocated_type_id"] == 0:
        campaign_template[Campaign.Field.lifetime_budget] = amount
    else:
        campaign_template[Campaign.Field.daily_budget] = amount

    campaign_template[Campaign.Field.bid_strategy] = BidStrategy[budget_opt["bid_strategy"]].value.name_sdk
    campaign_template[Campaign.Field.pacing_type] = [budget_opt["delivery_type"]]


def split_campaigns(campaign_template, step_four, step_two) -> List[CampaignSplit]:
    def format_campaign_name(*name_parts):
        return " - ".join(name_parts)

    campaigns = []
    split_by_location = step_four["is_split_by_location"]
    split_by_device = step_four["is_split_by_devices"]
    locations = step_two["targeting"]["locations"]
    campaign_budget_allocation = step_four.get("budget_allocation", {}).get("campaigns_budget")

    all_locations = [Location(**location) for location in locations]

    if split_by_location and split_by_device:
        for location in locations:
            for device in DevicePlatform.contexts[Contexts.SMART_CREATE].items:
                campaign = deepcopy(campaign_template)
                campaign[Campaign.Field.name] = format_campaign_name(
                    campaign_template[Campaign.Field.name],
                    location["selected_location_string"],
                    device.name_sdk.title(),
                )
                allocate_campaign_budget(campaign, campaign_budget_allocation, location, device)
                campaigns.append(
                    CampaignSplit(
                        campaign,
                        device=device.name_sdk,
                        location=Location(**location),
                    )
                )
    elif split_by_location and not split_by_device:
        for location in locations:
            campaign = deepcopy(campaign_template)
            campaign[Campaign.Field.name] = format_campaign_name(
                campaign_template[Campaign.Field.name], location["selected_location_string"]
            )
            allocate_campaign_budget(campaign, campaign_budget_allocation, location=location)
            campaigns.append(CampaignSplit(campaign, location=Location(**location)))
    elif not split_by_location and split_by_device:
        for device in DevicePlatform.contexts[Contexts.SMART_CREATE].items:
            campaign = deepcopy(campaign_template)
            campaign[Campaign.Field.name] = format_campaign_name(
                campaign_template[Campaign.Field.name], device.name_sdk.title()
            )
            allocate_campaign_budget(campaign, campaign_budget_allocation, device=device)
            campaigns.append(CampaignSplit(campaign, all_locations=all_locations, device=device.name_sdk))
    else:
        campaigns.append(CampaignSplit(deepcopy(campaign_template), all_locations=all_locations))

    return campaigns


def get_budget_allocated_type(campaign):
    return Campaign.Field.lifetime_budget if Campaign.Field.lifetime_budget in campaign else Campaign.Field.daily_budget


def allocate_campaign_budget(campaign, campaign_budget_allocation, location=None, device=None):
    if not campaign_budget_allocation:
        return

    location = location.get("key")
    try:
        device = device.name_sdk
    except AttributeError:
        device = None

    budget_allocated_type = get_budget_allocated_type(campaign)
    for allocation in campaign_budget_allocation:

        is_location_match = location == allocation.get("location")
        is_device_match = device == allocation.get("device")

        if "location" in allocation and "device" in allocation:
            if is_location_match and is_device_match:
                campaign[budget_allocated_type] = allocation.get("budget") * 100
                return
        elif "location" in allocation:
            if is_location_match:
                campaign[budget_allocated_type] = allocation.get("budget") * 100
                return
        elif "device" in allocation:
            if is_device_match:
                campaign[budget_allocated_type] = allocation.get("budget") * 100
                return
