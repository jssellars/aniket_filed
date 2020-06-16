import typing
from copy import deepcopy

from GoogleDexter.Infrastructure.Domain.Actions.ActionEnums import ActionEnum, GenderEnum, PlacementEnum, \
    ImpressionDeviceEnum, BudgetTypeEnum
from GoogleDexter.Infrastructure.Domain.Breakdowns import BreakdownEnum, ActionBreakdownEnum

DEFAULT_BUDGET_CHANGE = 0.25


class ActionDetailsBuilder:

    def __init__(self):
        self.__builder = {
            (ActionEnum.INCREASE_BUDGET, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.increase_budget,
            (ActionEnum.DECREASE_BUDGET, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.decrease_budget,
            (ActionEnum.PAUSE, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.pause_structure,
            (ActionEnum.REMOVE, BreakdownEnum.AGE, ActionBreakdownEnum.NONE): self.split_age,
            (ActionEnum.REMOVE, BreakdownEnum.GENDER, ActionBreakdownEnum.NONE): self.remove_gender,
            # (ActionEnum.REMOVE, BreakdownEnum.PLACEMENT, ActionBreakdownEnum.NONE): self.remove_placement,
            # (ActionEnum.REMOVE, BreakdownEnum.DEVICE, ActionBreakdownEnum.NONE): self.remove_impression_device,
            # (ActionEnum.REMOVE, BreakdownEnum.PLATFORM, ActionBreakdownEnum.NONE): self.remove_publisher_platform
        }

    def build(self,
              action: ActionEnum = None,
              breakdown: BreakdownEnum = BreakdownEnum.NONE,
              action_breakdown: ActionBreakdownEnum = ActionBreakdownEnum.NONE,
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
            if entry == GenderEnum.MALE.value[0]:
                targeting["genders"] = [GenderEnum.FEMALE.value[1]]
            elif entry == GenderEnum.FEMALE.value[0]:
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
            if publisher_platform_value in targeting["flexible_spec"][PlacementEnum.PUBLISHER_PLATFORMS.value]:
                targeting["flexible_spec"][PlacementEnum.PUBLISHER_PLATFORMS.value].remove(publisher_platform_value)
            # remove placement
            for placement_position in PlacementEnum.PLACEMENT_POSITIONS.value:
                if placement_position_value in targeting["flexible_spec"][placement_position.value]:
                    targeting["flexible_spec"][placement_position.value].remove(placement_position_value)
            # remove device platform
            if device_platform_value in targeting["flexible_spec"][PlacementEnum.DEVICE_PLATFORMS.value]:
                targeting['flexible_spec'][PlacementEnum.DEVICE_PLATFORMS.value].remove(device_platform_value)

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
            if entry in targeting["flexible_spec"][ImpressionDeviceEnum.USER_DEVICE.value]:
                targeting["flexible_spec"][ImpressionDeviceEnum.USER_DEVICE.value].remove(entry)
            elif entry.title() in targeting["flexible_spec"][ImpressionDeviceEnum.USER_DEVICE.value]:
                targeting["flexible_spec"][ImpressionDeviceEnum.USER_DEVICE.value].remove(entry.title())

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
            if publisher_platform_value in targeting["flexible_spec"][PlacementEnum.PUBLISHER_PLATFORMS.value]:
                targeting["flexible_spec"][PlacementEnum.PUBLISHER_PLATFORMS.value].remove(publisher_platform_value)

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

        return action_details

    @staticmethod
    def decrease_budget(structure_details: typing.Dict = None, *args, **kwargs) -> typing.Union[
        typing.Dict, typing.NoReturn]:
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

        return action_details

    @staticmethod
    def pause_structure(*args, **kwargs) -> typing.Dict:
        action_details = {"details": {"status": "PAUSE"}}
        return action_details

    @staticmethod
    def split_age(*args, **kwargs) -> typing.Union[typing.Dict, typing.NoReturn]:
        #  todo: find out how to implement an age group split ( i.e. remove age 25-30 )
        return {}
