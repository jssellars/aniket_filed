import json
from collections import defaultdict
from copy import deepcopy
from dataclasses import asdict
from typing import Dict, List, Optional, Tuple

from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.campaign import Campaign

from Core.facebook.sdk_adapter.ad_objects.content_delivery_report import Placement
from Core.facebook.sdk_adapter.ad_objects.targeting import DevicePlatform
from Core.facebook.sdk_adapter.catalog_models import Contexts
from Core.facebook.sdk_adapter.smart_create.constants import FB_MAX_AGE
from Core.facebook.sdk_adapter.smart_create.targeting import (
    AgeGroup,
    CustomAudience,
    FlexibleTargeting,
    GenderGroup,
    Interest,
    Targeting,
)
from Core.Web.FacebookGraphAPI.GraphAPIDomain.FacebookMiscFields import (
    FacebookGender,
    Gender,
)
from Core.facebook.sdk_adapter.validations import PLATFORM_X_POSITIONS

FACEBOOK_DEFAULT_KEY = "FACEBOOK"
INSTAGRAM_DEFAULT_KEY = "INSTAGRAM"
AUDIENCE_NETWORK_DEFAULT_KEY = "AUDIENCE_NETWORK"

DEFAULT_PLACEMENT_POSITIONS = {
    FACEBOOK_DEFAULT_KEY: ["story", "feed"],
    INSTAGRAM_DEFAULT_KEY: ["stream", "story"],
    AUDIENCE_NETWORK_DEFAULT_KEY: ["classic"],
}

DEFAULT_PLACEMENTS = [
    Placement.FACEBOOK_FEED,
    Placement.FACEBOOK_STORIES,
    Placement.INSTAGRAM_FEED,
    Placement.INSTAGRAM_STORIES,
    Placement.AUDIENCE_NETWORK_NATIVE_BANNER_AND_INTERSTITIAL,
]


def build_ad_sets(
    step_one,
    step_two,
    step_three,
    step_four,
    is_using_cbo,
    is_using_conversions,
    destination_type,
):
    ad_set_template = {}
    build_base_ad_sets(
        ad_set_template,
        step_one,
        step_two,
        step_three,
        is_using_cbo,
        is_using_conversions,
        destination_type,
    )
    return split_ad_sets(ad_set_template, step_two, step_four)


def build_base_ad_sets(
    ad_set_template: Dict,
    step_one: Dict,
    step_two: Dict,
    step_three: Dict,
    is_using_cbo: bool,
    objective: str,
    destination_type: str,
):
    # TODO: this is not specified - maybe some default ?
    if AdSet.Field.tune_for_category in step_two:
        ad_set_template[AdSet.Field.tune_for_category] = step_two[AdSet.Field.tune_for_category]
    else:
        ad_set_template[AdSet.Field.tune_for_category] = AdSet.TuneForCategory.none

    ad_set_template[AdSet.Field.name] = step_two["ad_set_name"]
    ad_set_template[AdSet.Field.destination_type] = destination_type

    set_statuses(ad_set_template)
    set_date_interval(ad_set_template, step_one, step_two)
    ad_set_template[AdSet.Field.promoted_object] = get_promoted_object(
        objective, step_three.get("ads")[0], step_two.get("facebook_page_id")
    )

    opt_and_delivery = step_two["optimization_and_delivery"]
    ad_set_template[AdSet.Field.optimization_goal] = opt_and_delivery["optimization_goal"]
    ad_set_template[AdSet.Field.billing_event] = opt_and_delivery["billing_event"]

    # TODO: This might change depending on step 4 where every adset has it's budget
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


def set_date_interval(ad_set_template, step_one, step_two):
    date_interval = step_two.get("date")
    if not date_interval:
        date_interval = step_one.get("date")
    ad_set_template[AdSet.Field.start_time] = date_interval["start_date"]
    if "end_date" in date_interval and date_interval["end_date"]:
        ad_set_template[AdSet.Field.end_time] = date_interval["end_date"]


def set_statuses_dto(ad_set_template):
    # Temporary functions till we integrate CreateAdSet to Smart Create and Smart Edit
    # TODO: Paused just for testing purposes
    ad_set_template.effective_status = AdSet.EffectiveStatus.paused
    ad_set_template.status = AdSet.Status.paused


def set_date_interval_dto(ad_set_template, date_interval):
    # Temporary functions till we integrate CreateAdSet to Smart Create and Smart Edit
    ad_set_template.start_time = date_interval["start_date"]
    ad_set_template.end_time = date_interval["end_date"]


def extract_pixel_data(request: Dict) -> Dict:
    pixel_data = dict()

    pixel_id = request.get("pixel_id")
    custom_event_type = request.get("custom_event_type")

    if pixel_id and custom_event_type:
        pixel_data.update(pixel_id=pixel_id, custom_event_type=custom_event_type)

        pixel_rule = request.get("pixel_rule")
        if isinstance(pixel_rule, str):
            pixel_rule = json.loads(pixel_rule.replace("\\", ""))
            pixel_data["pixel_rule"] = pixel_rule
    else:
        # If you provide "pixel_id", then you MUST provide "custom_event_type"
        # See https://developers.facebook.com/docs/marketing-api/reference/ad-promoted-object/
        raise ValueError("Pixel ID and Custom Event Type are required for conversions")

    return pixel_data


def get_promoted_object(objective: str, adset_request: Dict = None, page_id: str = None) -> Dict:
    promoted_object = dict()

    if objective == Campaign.Objective.conversions:
        pixel_data = extract_pixel_data(adset_request)
        promoted_object.update(pixel_data)

    elif objective == Campaign.Objective.reach:
        # Reach requires a facebook page to promote
        if not page_id:
            raise ValueError("Reach objective needs a facebook page to be supplied")
        promoted_object["page_id"] = page_id

    return promoted_object


def split_ad_sets(ad_set_template, step_two, step_four):
    ad_sets = []

    is_split_age_range_selected = step_four.get("is_split_age_range_selected")
    is_split_by_gender_selected = step_four["is_split_by_gender_selected"]

    targeting_request = step_two["targeting"]
    languages = targeting_request.get("languages", [])
    if languages:
        languages = [language["key"] for language in languages]

    included_interests, excluded_interests, narrow_interests = extract_interests(targeting_request)
    included_custom_audiences, excluded_custom_audiences = extract_custom_audiences(targeting_request)

    age_groups = split_age_groups(is_split_age_range_selected, targeting_request.get("age_range"))
    gender_groups = split_genders(is_split_by_gender_selected, targeting_request.get("gender"))

    (publisher_platforms, platform_positions) = get_placement_positions(step_two.get("placements"))

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
                publisher_platforms=publisher_platforms,
                device_platforms=[x.name_sdk for x in DevicePlatform.contexts[Contexts.SMART_CREATE].items],
            )

            if platform_positions:
                for platform_position, positions in platform_positions.items():
                    targeting.__setattr__(platform_position, positions)

            ad_set_element = deepcopy(ad_set_template)
            set_split_fields_and_name(
                age_group,
                gender_group,
                targeting,
                ad_set_element,
                is_split_by_gender_selected,
                is_split_age_range_selected,
            )
            ad_sets.append(ad_set_element)

    return ad_sets


def set_split_fields_and_name(
    age_group: Optional[AgeGroup],
    gender_group: Optional[GenderGroup],
    targeting: Targeting,
    ad_set_element: Dict,
    is_split_by_gender_selected: bool,
    is_split_age_range_selected: bool,
):
    if is_split_by_gender_selected:
        targeting.genders = [gender.value for gender in gender_group.genders]
        ad_set_element[AdSet.Field.name] += " - " + " - ".join([gender.name for gender in gender_group.genders])

    if is_split_age_range_selected:
        targeting.age_min = age_group.age_min
        targeting.age_max = age_group.age_max
        ad_set_element[AdSet.Field.name] += f" - {str(age_group.age_min)}-{str(age_group.age_max)}"

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
        return [
            GenderGroup(genders=[FacebookGender.MEN]),
            GenderGroup(genders=[FacebookGender.WOMEN]),
        ]

    else:
        if gender == Gender.WOMEN:
            return [GenderGroup(genders=[FacebookGender.WOMEN])]
        elif gender == Gender.MEN:
            return [GenderGroup(genders=[FacebookGender.MEN])]

        return [GenderGroup(genders=[FacebookGender.MEN, FacebookGender.WOMEN])]


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


def get_placement_positions(placements: List[Dict]) -> Optional[Tuple[List[str], Dict]]:
    """ """
    if not placements:
        return
    publisher_platforms = []
    platform_positions = defaultdict(list)

    for placement in placements:
        # # Commented out because some enum values from facebook are not valid
        # platform_enum = Platform.as_dict()[placement["name"]]
        # platform_name = platform_enum["name"].lower()
        # publisher_platforms.append(platform_name)
        # for position in placement.get("positions", []):
        #     # Bad fix
        #     placement_enum = Placement.as_dict()[position]["items"]
        #     position_enum, = [position_enum for position_enum in placement_enum.values() if position_enum["kind"] == "Position"]
        #     position_name = position_enum["name"].lower()
        #     platform_positions[platform_name].append(position_name)

        for platform, positions in PLATFORM_X_POSITIONS.items():
            if placement["name"] != platform.name:
                continue
            publisher_platforms.append(platform.value.name_sdk.lower())
            for request_position in placement.get("positions", []):
                for key, value in positions.items():
                    if isinstance(key, str):
                        continue
                    if request_position == key.name:
                        platform_positions[f"{platform.name.lower()}_positions"].append(value)

    return publisher_platforms, platform_positions


def map_custom_audiences(custom_audiences):
    if custom_audiences:
        return [CustomAudience(id=audience_id) for audience_id in custom_audiences]

    return custom_audiences
