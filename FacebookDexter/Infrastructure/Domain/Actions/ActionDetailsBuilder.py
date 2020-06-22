import typing
from copy import deepcopy

from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import ActionEnum, GenderEnum, PlacementEnum, \
    ImpressionDeviceEnum, BudgetTypeEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownEnum, ActionBreakdownEnum, BreakdownMetadata
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Metrics.MetricCalculator import MetricCalculator
from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum

DEFAULT_BUDGET_CHANGE = 0.25


class ActionDetailsBuilder:
    USE_ALTERNATIVE_TEMPLATE = True
    AGE_RANGE_GROUPS = 6
    __PUBLISHER_PLATFORMS = ["facebook", "instagram", "messenger", "audience_network"]
    __DEVICE_PLATFORMS = ["mobile", "desktop"]
    __PLACEMENT_POSITIONS = ["feed", "right_hand_column", "instant_article", "marketplace", "video_feeds", "story", "search",
                             "stream", "story", "explore",
                             "classic", "instream_video", "rewarded_video",
                             "messenger_home", "sponsored_messages", "story"]

    def __init__(self,
                 facebook_id=None,
                 repository=None,
                 time_interval=None,
                 date_stop=None,
                 debug=None):
        self.__facebook_id = facebook_id
        self.__repository = repository
        self.__time_interval = time_interval
        self.__date_stop = date_stop
        self.__debug = debug

        self.__builder = {
            (ActionEnum.INCREASE_BUDGET, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.increase_budget,
            (ActionEnum.DECREASE_BUDGET, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.decrease_budget,
            (ActionEnum.PAUSE, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.pause_structure,
            (ActionEnum.REMOVE, BreakdownEnum.AGE, ActionBreakdownEnum.NONE): self.split_age,
            (ActionEnum.REMOVE, BreakdownEnum.GENDER, ActionBreakdownEnum.NONE): self.remove_gender,
            (ActionEnum.REMOVE, BreakdownEnum.PLACEMENT, ActionBreakdownEnum.NONE): self.remove_placement,
            (ActionEnum.REMOVE, BreakdownEnum.DEVICE, ActionBreakdownEnum.NONE): self.remove_device_platform,
            (ActionEnum.REMOVE, BreakdownEnum.PLATFORM, ActionBreakdownEnum.NONE): self.remove_publisher_platform,
            (ActionEnum.DUPLICATE, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.duplicate_ad,
            (ActionEnum.NONE, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.no_action_details,
            (ActionEnum.NONE, BreakdownEnum.AGE, ActionBreakdownEnum.NONE): self.no_action_details,
            (ActionEnum.NONE, BreakdownEnum.GENDER, ActionBreakdownEnum.NONE): self.no_action_details,
            (ActionEnum.NONE, BreakdownEnum.PLACEMENT, ActionBreakdownEnum.NONE): self.no_action_details,
            (ActionEnum.NONE, BreakdownEnum.DEVICE, ActionBreakdownEnum.NONE): self.no_action_details,
            (ActionEnum.NONE, BreakdownEnum.PLATFORM, ActionBreakdownEnum.NONE): self.no_action_details
        }

    def build(self,
              action: ActionEnum = None,
              breakdown: BreakdownEnum = BreakdownEnum.NONE,
              action_breakdown: ActionBreakdownEnum = ActionBreakdownEnum.NONE,
              structure_details: typing.Dict = None,
              value: typing.List[typing.AnyStr] = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        # todo: add all for all placement values and compare
        builder = self.__builder.get((action, breakdown, action_breakdown))
        if builder:
            return builder(structure_details, value)
        return None

    def remove_gender(self,
                      structure_details: typing.Dict = None,
                      value: typing.List[typing.AnyStr] = None) -> \
            typing.Tuple[typing.Union[typing.Dict, typing.NoReturn], bool]:
        targeting = deepcopy(structure_details["targeting"])
        all_genders = [GenderEnum.MALE.value[0], GenderEnum.FEMALE.value[0], GenderEnum.UNKNOWN.value[0]]
        available_genders = targeting.get('genders')
        if available_genders is None:
            available_genders = [GenderEnum.MALE.value[0], GenderEnum.FEMALE.value[0]]
        if value == available_genders or value == all_genders:
            action_details, _ = self.pause_structure()
            return action_details, self.USE_ALTERNATIVE_TEMPLATE

        for entry in value:
            if entry == GenderEnum.MALE.value[0] and entry != available_genders:
                targeting["genders"] = [GenderEnum.FEMALE.value[1]]
            elif entry == GenderEnum.FEMALE.value[0] and entry != available_genders:
                targeting["genders"] = [GenderEnum.MALE.value[1]]
            elif entry == GenderEnum.UNKNOWN.value[0]:
                targeting["genders"] = [GenderEnum.MALE.value[1], GenderEnum.FEMALE.value[1]]
            else:
                raise ValueError(f"Unknown gender {entry}")

        # construct action details
        action_details = {
            "details": {
                "targeting": targeting
            }
        }

        return action_details, not self.USE_ALTERNATIVE_TEMPLATE

    def remove_placement(self,
                         structure_details: typing.Dict = None,
                         value: typing.List[typing.AnyStr] = None) -> \
            typing.Tuple[typing.Union[typing.Dict, typing.NoReturn], bool]:
        targeting = structure_details.get('targeting', None)
        if not targeting:
            return {}, not self.USE_ALTERNATIVE_TEMPLATE

        available_publisher_platforms = set(targeting.get(PlacementEnum.PUBLISHER_PLATFORMS.value, self.__PUBLISHER_PLATFORMS))
        available_placement_positions = set()

        for placement_position_enum in PlacementEnum.PLACEMENT_POSITIONS.value:
            if placement_position_enum.value in targeting:
                for placement_position in targeting[placement_position_enum.value]:
                    available_placement_positions.add(placement_position)

        if len(available_placement_positions) == 0:
            available_placement_positions = set(self.__PLACEMENT_POSITIONS)

        available_device_platforms = set(targeting.get(PlacementEnum.DEVICE_PLATFORMS.value, self.__DEVICE_PLATFORMS))
        publisher_platform_values, placement_position_values, device_platform_values = set(), set(), set()

        for entry in value:
            publisher_platform_value, placement_position_value, device_platform_value = entry.split(", ")
            device_platform_value = device_platform_value.split("_")[0]
            publisher_platform_values.add(publisher_platform_value)
            placement_position_values.add(placement_position_value)
            device_platform_values.add(device_platform_value)

        if publisher_platform_values == available_publisher_platforms or \
                placement_position_values == available_placement_positions or \
                device_platform_values == available_device_platforms:
            action_details, _ = self.pause_structure()
            return action_details, self.USE_ALTERNATIVE_TEMPLATE

        # remove publisher platform
        if PlacementEnum.PUBLISHER_PLATFORMS.value in targeting:
            for publisher_platform_value in publisher_platform_values:
                if publisher_platform_value in targeting[PlacementEnum.PUBLISHER_PLATFORMS.value]:
                    targeting[PlacementEnum.PUBLISHER_PLATFORMS.value].remove(publisher_platform_value)
        else:
            targeting[PlacementEnum.PUBLISHER_PLATFORMS.value] = available_publisher_platforms - publisher_platform_values

        # remove placement
        for placement_position_enum in PlacementEnum.PLACEMENT_POSITIONS.value:
            if placement_position_enum.value in targeting:
                for placement_position_value in placement_position_values:
                    if placement_position_value in targeting[placement_position_enum.value]:
                        targeting[placement_position_enum.value].remove(placement_position_value)
            else:
                targeting[placement_position_enum.value] = available_placement_positions - placement_position_values

        # remove device platform
        if PlacementEnum.DEVICE_PLATFORMS.value in targeting:
            for device_platform_value in device_platform_values:
                if device_platform_value in targeting[PlacementEnum.DEVICE_PLATFORMS.value]:
                    targeting[PlacementEnum.DEVICE_PLATFORMS.value].remove(device_platform_value)
        else:
            targeting[PlacementEnum.DEVICE_PLATFORMS.value] = available_device_platforms - device_platform_values

        # construct action details
        action_details = {
            "details": {
                "targeting": targeting
            }
        }

        return action_details, not self.USE_ALTERNATIVE_TEMPLATE

    def remove_device_platform(self,
                               structure_details: typing.Dict = None,
                               value: typing.List[typing.AnyStr] = None) -> \
            typing.Tuple[typing.Union[typing.Dict, typing.NoReturn], bool]:
        targeting = structure_details["targeting"]
        if not targeting:
            return {}, not self.USE_ALTERNATIVE_TEMPLATE

        available_device_platforms = set(targeting.get(PlacementEnum.DEVICE_PLATFORMS.value, self.__DEVICE_PLATFORMS))
        device_platform_values = set()

        for entry in value:
            device_platform_values.add(entry)

        if PlacementEnum.DEVICE_PLATFORMS.value in targeting:
            for device_platform_value in device_platform_values:
                if device_platform_value in targeting[PlacementEnum.DEVICE_PLATFORMS.value]:
                    targeting[PlacementEnum.DEVICE_PLATFORMS.value].remove(device_platform_value)
        else:
            targeting[PlacementEnum.DEVICE_PLATFORMS.value] = available_device_platforms - device_platform_values

        # construct action details
        action_details = {
            "details": {
                "targeting": targeting
            }
        }
        return action_details, not self.USE_ALTERNATIVE_TEMPLATE

    def remove_publisher_platform(self,
                                  structure_details: typing.Dict = None,
                                  value: typing.List[typing.AnyStr] = None) -> \
            typing.Tuple[typing.Union[typing.Dict, typing.NoReturn], bool]:
        targeting = structure_details["targeting"]
        if not targeting:
            return {}, not self.USE_ALTERNATIVE_TEMPLATE

        available_publisher_platforms = set(targeting.get(PlacementEnum.PUBLISHER_PLATFORMS.value, self.__PUBLISHER_PLATFORMS))
        publisher_platform_values = set()

        for entry in value:
            publisher_platform_values.add(entry)

        if publisher_platform_values == available_publisher_platforms:
            action_details, _ = self.pause_structure()
            return action_details, self.USE_ALTERNATIVE_TEMPLATE

        if PlacementEnum.PUBLISHER_PLATFORMS.value in targeting:
            for publisher_platform_value in publisher_platform_values:
                if publisher_platform_value in targeting[PlacementEnum.PUBLISHER_PLATFORMS.value]:
                    targeting[PlacementEnum.PUBLISHER_PLATFORMS.value].remove(publisher_platform_value)
        else:
            targeting[PlacementEnum.PUBLISHER_PLATFORMS.value] = available_publisher_platforms - publisher_platform_values

        action_details = {
            "details": {
                "targeting": targeting
            }
        }
        return action_details, not self.USE_ALTERNATIVE_TEMPLATE

    def increase_budget(self,
                        structure_details: typing.Dict = None, *args, **kwargs) -> \
            typing.Tuple[typing.Union[typing.Dict, typing.NoReturn], bool]:
        value = DEFAULT_BUDGET_CHANGE
        lifetime_budget = structure_details.get(BudgetTypeEnum.LIFETIME.value)
        daily_budget = structure_details.get(BudgetTypeEnum.DAILY.value)

        if daily_budget:
            budget_as_int = int(daily_budget)
            new_budget = budget_as_int + value * budget_as_int
            new_budget = round(new_budget)
            action_details = {
                "details": {
                    BudgetTypeEnum.DAILY.value: new_budget
                }
            }
        elif lifetime_budget:
            budget_as_int = int(lifetime_budget)
            new_budget = budget_as_int + value * budget_as_int
            new_budget = round(new_budget)
            action_details = {
                "details": {
                    BudgetTypeEnum.LIFETIME.value: new_budget
                }
            }
        else:
            action_details = {}

        return action_details, not self.USE_ALTERNATIVE_TEMPLATE

    def decrease_budget(self,
                        structure_details: typing.Dict = None, *args, **kwargs) -> \
            typing.Tuple[typing.Union[typing.Dict, typing.NoReturn], bool]:
        value = DEFAULT_BUDGET_CHANGE
        lifetime_budget = structure_details.get(BudgetTypeEnum.LIFETIME.value)
        daily_budget = structure_details.get(BudgetTypeEnum.DAILY.value)

        if daily_budget:
            budget_as_int = int(daily_budget)
            new_budget = budget_as_int - value * budget_as_int
            new_budget = round(new_budget)
            action_details = {
                "details": {
                    BudgetTypeEnum.DAILY.value: new_budget
                }
            }
        elif lifetime_budget:
            budget_as_int = int(lifetime_budget)
            new_budget = budget_as_int - value * budget_as_int
            new_budget = round(new_budget)
            action_details = {
                "details": {
                    BudgetTypeEnum.LIFETIME.value: new_budget
                }
            }
        else:
            action_details = {}

        return action_details, not self.USE_ALTERNATIVE_TEMPLATE

    def pause_structure(self, *args, **kwargs) -> typing.Tuple[typing.Dict, bool]:
        action_details = {"details": {"status": "PAUSE"}}
        return action_details, not self.USE_ALTERNATIVE_TEMPLATE

    def split_age(self,
                  structure_details: typing.Dict = None,
                  value: typing.List[typing.AnyStr] = None, *args, **kwargs) -> \
            typing.Tuple[typing.Union[typing.Dict, typing.NoReturn], bool]:
        #  todo: find out how to implement an age group split ( i.e. remove age 25-30 )
        age_range = [int(age_group.replace("+", ""))
                     for entry in value
                     for age_group in entry.split("-")]
        targeting = structure_details.get('targeting', None)
        if targeting:
            if (min(age_range) == targeting.get('age_min') and
                max(age_range) == targeting.get('age_max')) or \
                    len(value) == self.AGE_RANGE_GROUPS:
                action_details, _ = self.pause_structure()
                return action_details, self.USE_ALTERNATIVE_TEMPLATE

        return {}, not self.USE_ALTERNATIVE_TEMPLATE

    def duplicate_ad(self, *args, **kwargs):
        ad_ids = self.__repository.get_ads_by_adset_id(key_value=self.__facebook_id)

        calculator = (MetricCalculator().
                      set_level(LevelEnum.AD).
                      set_metric(AvailableMetricEnum.CLICKS.value).
                      set_repository(self.__repository).
                      set_date_stop(self.__date_stop).
                      set_time_interval(self.__time_interval).
                      set_debug_mode(self.__debug).
                      set_breakdown_metadata(BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                               action_breakdown=ActionBreakdownEnum.NONE)))

        average_metric_values = [
            (ad_id, calculator.
             set_facebook_id(ad_id).
             compute_value(atype=AntecedentTypeEnum.VALUE,
                           time_interval=self.__time_interval)) for ad_id in ad_ids]
        try:
            sorted_values = sorted(average_metric_values, key=lambda x: x[1][0], reverse=True)
            if sorted_values[0][1][0]:
                best_performing_ad_id = sorted_values[0][0]
            else:
                return None, None
        except TypeError:
            import traceback
            traceback.print_exc()
            return None

        action_details = {
            "numberOfDuplicates": 1,
            "parentIds": [self.__facebook_id],
            "structureId": best_performing_ad_id
        }

        return action_details, not self.USE_ALTERNATIVE_TEMPLATE

    def no_action_details(self, *args, **kwargs):
        return {}, not self.USE_ALTERNATIVE_TEMPLATE
