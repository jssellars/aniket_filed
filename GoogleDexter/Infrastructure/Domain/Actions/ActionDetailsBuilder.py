import typing
from copy import deepcopy

from GoogleDexter.Infrastructure.Domain.Actions.ActionEnums import GoogleActionEnum, GoogleGenderEnum, \
    GooglePlacementEnum, GoogleImpressionDeviceEnum, GoogleBudgetTypeEnum
from GoogleDexter.Infrastructure.Domain.Breakdowns import GoogleActionBreakdownEnum, GoogleBreakdownEnum

DEFAULT_BUDGET_CHANGE = 0.25


class ActionDetailsBuilder:

    def __init__(self):
        self.__builder = {
            (GoogleActionEnum.INCREASE_BUDGET, GoogleBreakdownEnum.NONE,
             GoogleActionBreakdownEnum.NONE): self.increase_budget,
            (GoogleActionEnum.DECREASE_BUDGET, GoogleBreakdownEnum.NONE,
             GoogleActionBreakdownEnum.NONE): self.decrease_budget,
            (GoogleActionEnum.PAUSE, GoogleBreakdownEnum.NONE, GoogleActionBreakdownEnum.NONE): self.pause_structure,
            (GoogleActionEnum.REMOVE, GoogleBreakdownEnum.AGE, GoogleActionBreakdownEnum.NONE): self.split_age,
            (GoogleActionEnum.REMOVE, GoogleBreakdownEnum.GENDER, GoogleActionBreakdownEnum.NONE): self.remove_gender,
            # (ActionEnum.REMOVE, GoogleBreakdownEnum.PLACEMENT, GoogleActionBreakdownEnum.NONE): self.remove_placement,
            # (ActionEnum.REMOVE, GoogleBreakdownEnum.DEVICE, GoogleActionBreakdownEnum.NONE): self.remove_impression_device,
            # (ActionEnum.REMOVE, GoogleBreakdownEnum.PLATFORM, GoogleActionBreakdownEnum.NONE): self.remove_publisher_platform
        }

    def build(self,
              action: GoogleActionEnum = None,
              breakdown: GoogleBreakdownEnum = GoogleBreakdownEnum.NONE,
              action_breakdown: GoogleActionBreakdownEnum = GoogleActionBreakdownEnum.NONE,
              structure_details: typing.Dict = None,
              value: typing.List[typing.AnyStr] = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        builder = self.__builder.get((action, breakdown, action_breakdown))
        if builder:
            return builder(structure_details, value)
        return None

    @staticmethod
    def remove_gender(structure_details: typing.Dict = None,
                      value: typing.List[typing.AnyStr] = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        targeting = deepcopy(structure_details["targeting"])

        for entry in value:
            if entry == GoogleGenderEnum.MALE.value[0]:
                targeting["genders"] = [GoogleGenderEnum.FEMALE.value[1]]
            elif entry == GoogleGenderEnum.FEMALE.value[0]:
                targeting["genders"] = [GoogleGenderEnum.MALE.value[1]]
            elif entry == GoogleGenderEnum.UNKNOWN.value[0]:
                targeting["genders"] = [GoogleGenderEnum.MALE.value[1], GoogleGenderEnum.FEMALE.value[1]]
            else:
                raise ValueError(f"Unknown gender {entry}")

        # construct action details
        action_details = {
            "details": {
                "targeting": targeting
            }
        }

        return action_details

    @staticmethod
    def remove_placement(structure_details: typing.Dict = None,
                         value: typing.List[typing.AnyStr] = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        targeting = structure_details["targeting"]
        if 'flexible_spec' not in targeting.keys():
            return {}

        for entry in value:
            publisher_platform_value, placement_position_value, device_platform_value = entry.split(",")
            # remove publisher platform
            #  publisher platform breakdowns give data for {publisher_platform}_app and
            # {publisher_platform}_web, but targeting only accepts {publisher_platform}
            publisher_platform_value = publisher_platform_value.split("_")[0]
            if publisher_platform_value in targeting["flexible_spec"][GooglePlacementEnum.PUBLISHER_PLATFORMS.value]:
                targeting["flexible_spec"][GooglePlacementEnum.PUBLISHER_PLATFORMS.value].remove(
                    publisher_platform_value)
            # remove placement
            for placement_position in GooglePlacementEnum.PLACEMENT_POSITIONS.value:
                if placement_position_value in targeting["flexible_spec"][placement_position.value]:
                    targeting["flexible_spec"][placement_position.value].remove(placement_position_value)
            # remove device platform
            if device_platform_value in targeting["flexible_spec"][GooglePlacementEnum.DEVICE_PLATFORMS.value]:
                targeting['flexible_spec'][GooglePlacementEnum.DEVICE_PLATFORMS.value].remove(device_platform_value)

        # construct action details
        action_details = {
            "details": {
                "targeting": targeting
            }
        }

        return action_details

    @staticmethod
    def remove_impression_device(structure_details: typing.Dict = None,
                                 value: typing.List[typing.AnyStr] = None) -> typing.Union[
        typing.Dict, typing.NoReturn]:
        targeting = structure_details["targeting"]
        if 'flexible_spec' not in targeting.keys():
            return {}

        for entry in value:
            if entry in targeting["flexible_spec"][GoogleImpressionDeviceEnum.USER_DEVICE.value]:
                targeting["flexible_spec"][GoogleImpressionDeviceEnum.USER_DEVICE.value].remove(entry)
            elif entry.title() in targeting["flexible_spec"][GoogleImpressionDeviceEnum.USER_DEVICE.value]:
                targeting["flexible_spec"][GoogleImpressionDeviceEnum.USER_DEVICE.value].remove(entry.title())

        # construct action details
        action_details = {
            "details": {
                "targeting": targeting
            }
        }
        return action_details

    @staticmethod
    def remove_publisher_platform(structure_details: typing.Dict = None,
                                  value: typing.List[typing.AnyStr] = None) -> typing.Union[
        typing.Dict, typing.NoReturn]:
        targeting = structure_details["targeting"]
        if 'flexible_spec' not in targeting.keys():
            return {}

        for entry in value:
            # remove publisher platform
            #  publisher platform breakdowns give data for {publisher_platform}_app and
            # {publisher_platform}_web, but targeting only accepts {publisher_platform}
            publisher_platform_value = entry.split("_")[0]
            if publisher_platform_value in targeting["flexible_spec"][GooglePlacementEnum.PUBLISHER_PLATFORMS.value]:
                targeting["flexible_spec"][GooglePlacementEnum.PUBLISHER_PLATFORMS.value].remove(
                    publisher_platform_value)

        action_details = {
            "details": {
                "targeting": targeting
            }
        }
        return action_details

    @staticmethod
    def increase_budget(structure_details: typing.Dict = None, *args, **kwargs) -> typing.Union[
        typing.Dict, typing.NoReturn]:
        value = DEFAULT_BUDGET_CHANGE
        lifetime_budget = structure_details.get(GoogleBudgetTypeEnum.LIFETIME.value)
        daily_budget = structure_details.get(GoogleBudgetTypeEnum.DAILY.value)

        if daily_budget:
            budget_as_int = int(daily_budget)
            new_budget = budget_as_int + value * budget_as_int
            new_budget = round(new_budget)
            action_details = {
                "details": {
                    GoogleBudgetTypeEnum.DAILY.value: new_budget
                }
            }
        elif lifetime_budget:
            budget_as_int = int(lifetime_budget)
            new_budget = budget_as_int + value * budget_as_int
            new_budget = round(new_budget)
            action_details = {
                "details": {
                    GoogleBudgetTypeEnum.LIFETIME.value: new_budget
                }
            }
        else:
            action_details = {}

        return action_details

    @staticmethod
    def decrease_budget(structure_details: typing.Dict = None, *args, **kwargs) -> typing.Union[
        typing.Dict, typing.NoReturn]:
        value = DEFAULT_BUDGET_CHANGE
        lifetime_budget = structure_details.get(GoogleBudgetTypeEnum.LIFETIME.value)
        daily_budget = structure_details.get(GoogleBudgetTypeEnum.DAILY.value)

        if daily_budget:
            budget_as_int = int(daily_budget)
            new_budget = budget_as_int - value * budget_as_int
            new_budget = round(new_budget)
            action_details = {
                "details": {
                    GoogleBudgetTypeEnum.DAILY.value: new_budget
                }
            }
        elif lifetime_budget:
            budget_as_int = int(lifetime_budget)
            new_budget = budget_as_int - value * budget_as_int
            new_budget = round(new_budget)
            action_details = {
                "details": {
                    GoogleBudgetTypeEnum.LIFETIME.value: new_budget
                }
            }
        else:
            action_details = {}

        return action_details

    @staticmethod
    def pause_structure(*args, **kwargs) -> typing.Dict:
        action_details = {"details": {"status": "PAUSE"}}
        return action_details

    @staticmethod
    def split_age(*args, **kwargs) -> typing.Union[typing.Dict, typing.NoReturn]:
        #  todo: find out how to implement an age group split ( i.e. remove age 25-30 )
        return {}
