import json
from copy import deepcopy
from dataclasses import asdict
from typing import Dict, List, Optional, Tuple

from facebook_business.adobjects.adset import AdSet

from Core.facebook.sdk_adapter.ad_objects.content_delivery_report import Placement, Platform, Position
from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform
from Core.facebook.sdk_adapter.catalog_models import Contexts
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.smart_create.constants import (
    FB_MAX_AGE,
)
from FacebookCampaignsBuilder.Infrastructure.GraphAPIHandlers.smart_create.targeting import (
    AgeGroup,
    CustomAudience,
    FacebookGender,
    FlexibleTargeting,
    Gender,
    GenderGroup,
    Interest,
    Targeting,
)

DEFAULT_PLACEMENT_POSITIONS = {
    "FACEBOOK": ["story", "feed"],
    "INSTAGRAM": ["stream", "story"],
    "APP_NETWORK": ["classic"],
}

DEFAULT_PLACEMENTS = [
    Placement.FACEBOOK_FEED,
    Placement.FACEBOOK_STORIES,
    Placement.INSTAGRAM_FEED,
    Placement.INSTAGRAM_STORIES,
    Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
]


def build_ad_sets(step_two, step_three, step_four, is_using_cbo, is_using_conversions, destination_type):
    ad_set_template = {}
    build_base_ad_sets(
        ad_set_template, step_two, step_three, is_using_cbo, is_using_conversions, destination_type
    )
    return split_ad_sets(ad_set_template, step_two, step_four)


def build_base_ad_sets(ad_set_template, step_two, step_three, is_using_cbo, is_using_conversions, destination_type):
    # TODO: this is not specified - maybe some default ?
    if AdSet.Field.tune_for_category in step_two:
        ad_set_template[AdSet.Field.tune_for_category] = step_two[AdSet.Field.tune_for_category]
    else:
        ad_set_template[AdSet.Field.tune_for_category] = AdSet.TuneForCategory.none

    ad_set_template[AdSet.Field.name] = step_two["ad_set_name"]
    ad_set_template[AdSet.Field.destination_type] = destination_type

    set_statuses(ad_set_template)
    set_date_interval(ad_set_template, step_two)
    set_promoted_object(ad_set_template, is_using_conversions, step_three, step_two)

    opt_and_delivery = step_two["optimization_and_delivery"]
    ad_set_template[AdSet.Field.optimization_goal] = opt_and_delivery["optimization_goal"]
    ad_set_template[AdSet.Field.billing_event] = opt_and_delivery["billing_event"]

    # TODO: This might change depening on step 4 where every adset has it's budget
    if not is_using_cbo:
        budget_opt = step_two["budget_optimization"]
        amount = int(budget_opt["amount"]) * 100
        if budget_opt["budget_allocated_type_id"] == 0:
            ad_set_template[AdSet.Field.lifetime_budget] = amount
        else:
            ad_set_template[AdSet.Field.daily_budget] = amount

        ad_set_template[AdSet.Field.bid_strategy] = budget_opt["bid_strategy"]
        ad_set_template[AdSet.Field.pacing_type] = [budget_opt["delivery_type"]]


def set_statuses(ad_set_template):
    # TODO: Paused just for testing purposes
    ad_set_template[AdSet.Field.effective_status] = AdSet.EffectiveStatus.paused
    ad_set_template[AdSet.Field.status] = AdSet.Status.paused


def set_date_interval(ad_set_template, step_two):
    date_interval = step_two["date"]
    ad_set_template[AdSet.Field.start_time] = date_interval["start_date"]
    if "end_date" in date_interval and date_interval["end_date"]:
        ad_set_template[AdSet.Field.end_time] = date_interval["end_date"]


def set_promoted_object(ad_set_template, is_using_conversions, step_three, step_two):
    if is_using_conversions:
        promoted_object = dict(pixel_id=step_three["pixel_id"])

        # TODO: check if this is necessary
        if "custom_event_type" in step_three:
            promoted_object["custom_event_type"] = step_three["custom_event_type"]

        if "pixel_rule" in step_three and step_three["pixel_rule"]:
            pixel_rule = step_three["pixel_rule"]
            if isinstance(pixel_rule, str):
                pixel_rule = json.loads(pixel_rule).replace("\\", "")

            promoted_object["pixel_rule"] = pixel_rule

        ad_set_template[AdSet.Field.promoted_object] = promoted_object
    else:
        ad_set_template[AdSet.Field.promoted_object] = dict(page_id=step_two["facebook_page_id"])


def split_ad_sets(ad_set_template, step_two, step_four):
    ad_sets = []

    split_age_range_selected = step_four.get("split_age_range_selected")
    is_split_by_gender_selected = step_four["is_split_by_gender_selected"]

    targeting_request = step_two["targeting"]
    languages = targeting_request.get("languages", [])
    if languages:
        languages = [language["key"] for language in languages]

    included_interests, excluded_interests, narrow_interests = extract_interests(targeting_request)
    included_custom_audiences, excluded_custom_audiences = extract_custom_audiences(targeting_request)

    age_groups = split_age_groups(split_age_range_selected, targeting_request.get("age_range"))
    gender_groups = split_genders(is_split_by_gender_selected, targeting_request.get("gender"))

    (
        facebook_positions,
        instragram_positions,
        audience_network_positions,
        publisher_platforms,
    ) = add_placement_positions(step_two)

    for age_group in age_groups:
        for gender_group in gender_groups:
            flexible_spec = [FlexibleTargeting(included_interests)]

            # TODO: check if this is valid, maybe we should include the narrow interests into the
            #  included interests
            if narrow_interests:
                flexible_spec.append(FlexibleTargeting(narrow_interests))

            targeting = Targeting(
                flexible_spec,
                custom_audiences=included_custom_audiences,
                excluded_custom_audiences=excluded_custom_audiences,
                exclusions=FlexibleTargeting(interests=excluded_interests),
                locales=languages,
                facebook_positions=facebook_positions,
                instagram_positions=instragram_positions,
                audience_network_positions=audience_network_positions,
                publisher_platforms=publisher_platforms,
                device_platforms=[x.name_sdk for x in DevicePlatform.contexts[Contexts.SMART_CREATE].items],
            )

            ad_set_element = deepcopy(ad_set_template)
            set_split_fields_and_name(age_group, gender_group, targeting, ad_set_element)
            ad_sets.append(ad_set_element)

    return ad_sets


def set_split_fields_and_name(
        age_group: Optional[AgeGroup],
        gender_group: Optional[GenderGroup],
        targeting: Targeting,
        ad_set_element: Dict,
):
    if age_group:
        targeting.age_min = age_group.age_min
        targeting.age_max = age_group.age_max
        ad_set_element[AdSet.Field.name] += f" - {str(age_group.age_min)}-{str(age_group.age_max)}"

    if gender_group:
        targeting.genders = [gender.value for gender in gender_group.genders]
        ad_set_element[AdSet.Field.name] += " - " + " - ".join([gender.name for gender in gender_group.genders])

    ad_set_element["targeting"] = asdict(targeting)


def split_age_groups(split_age_range_selected: int, age_range: Dict) -> List[Optional[AgeGroup]]:
    if not age_range:
        return [None]

    if split_age_range_selected:
        return _split_age_groups(age_range, split_age_range_selected)
    else:
        return [AgeGroup(age_min=age_range["min_age"], age_max=age_range["max_age"])]


def _split_age_groups(age_range: Dict, split_age_range_selected: int) -> List[Optional[AgeGroup]]:
    age_groups = []
    age_min = age_range["min_age"]
    age_max = age_range["max_age"]

    for min_age in range(age_min, age_max, split_age_range_selected):
        max_age = min_age + split_age_range_selected
        if max_age > FB_MAX_AGE:
            max_age = FB_MAX_AGE

        age_groups.append(AgeGroup(age_min=min_age, age_max=max_age))

    if age_groups[-1].age_max > age_max:
        age_groups[-1].age_max = age_max

    return age_groups


def split_genders(is_split_by_gender_selected: bool, gender: int) -> List[Optional[GenderGroup]]:
    if gender is None:
        return [None]

    gender = Gender(gender)
    if is_split_by_gender_selected and gender == Gender.ALL:
        return [GenderGroup(genders=[FacebookGender.MALE]), GenderGroup(genders=[FacebookGender.FEMALE])]

    else:
        if gender == Gender.WOMEN:
            return [GenderGroup(genders=[FacebookGender.FEMALE])]
        elif gender == Gender.MEN:
            return [GenderGroup(genders=[FacebookGender.MALE])]

        return [GenderGroup(genders=[FacebookGender.MALE, FacebookGender.FEMALE])]


def extract_interests(targeting):
    included_interests = targeting.get("interests", [])
    excluded_interests = targeting.get("excluded_interests", [])
    narrow_interests = targeting.get("narrow_interests", [])

    included_interests = map_interests(included_interests)
    excluded_interests = map_interests(excluded_interests)
    narrow_interests = map_interests(narrow_interests)

    return included_interests, excluded_interests, narrow_interests


def map_interests(interests):
    if interests:
        return [Interest(id=interest["id"], name=interest["name"]) for interest in interests]
    return interests


def extract_custom_audiences(targeting):

    audience_type = targeting.get("type", None)

    if audience_type == 2:
        included_custom_audiences = targeting.get("custom_audiences", [])
        included_custom_audiences = map_custom_audiences(included_custom_audiences)
        return included_custom_audiences, []

    included_custom_audiences = targeting.get("included_custom_audiences", [])
    excluded_custom_audiences = targeting.get("exclude_custom_audiences", [])

    included_custom_audiences = map_custom_audiences(included_custom_audiences)
    excluded_custom_audiences = map_custom_audiences(excluded_custom_audiences)

    return included_custom_audiences, excluded_custom_audiences


def add_placement_positions(step_two: Dict) -> Tuple[List, List, List, List]:
    facebook_positions = []
    instragram_positions = []
    audience_network_positions = []
    publisher_platforms = []

    if "placements" in step_two and step_two["placements"]:
        for placement in step_two["placements"]:
            if placement["platform_key"] == "FACEBOOK":
                facebook_positions = DEFAULT_PLACEMENT_POSITIONS[placement["platform_key"]]
                publisher_platforms.append(Platform.FACEBOOK.value.name_sdk.lower())

            if placement["platform_key"] == "INSTAGRAM":
                instragram_positions = DEFAULT_PLACEMENT_POSITIONS[placement["platform_key"]]
                publisher_platforms.append(Platform.INSTAGRAM.value.name_sdk.lower())

            if placement["platform_key"] == "APP_NETWORK":
                audience_network_positions = DEFAULT_PLACEMENT_POSITIONS[placement["platform_key"]]
                publisher_platforms.append(Platform.AUDIENCE_NETWORK.value.name_sdk.lower())

    return facebook_positions, instragram_positions, audience_network_positions, publisher_platforms


def map_custom_audiences(custom_audiences):
    if custom_audiences:
        return [CustomAudience(id=audience_id) for audience_id in custom_audiences]

    return custom_audiences
