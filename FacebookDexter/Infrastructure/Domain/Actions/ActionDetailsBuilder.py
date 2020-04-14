import typing

from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import ActionEnum, GenderEnum, PlacementEnum, ImpressionDeviceEnum, BudgetTypeEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownEnum, ActionBreakdownEnum


class ActionDetailsBuilder:

    def __init__(self):
        self.__builder = {
            (ActionEnum.INCREASE_BUDGET, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.change_budget,
            (ActionEnum.DECREASE_BUDGET, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.change_budget,
            (ActionEnum.PAUSE, BreakdownEnum.NONE, ActionBreakdownEnum.NONE): self.pause_structure,
            (ActionEnum.REMOVE, BreakdownEnum.AGE, ActionBreakdownEnum.NONE): self.split_age,
            (ActionEnum.REMOVE, BreakdownEnum.GENDER, ActionBreakdownEnum.NONE): self.remove_gender,
            (ActionEnum.REMOVE, BreakdownEnum.PLACEMENT, ActionBreakdownEnum.NONE): self.remove_placement,
            (ActionEnum.REMOVE, BreakdownEnum.DEVICE, ActionBreakdownEnum.NONE): self.remove_impression_device
        }

    def build(self,
              action: ActionEnum = None,
              breakdown: BreakdownEnum = BreakdownEnum.NONE,
              action_breakdown: ActionBreakdownEnum = ActionBreakdownEnum.NONE,
              structure_details: typing.Dict = None,
              value: typing.AnyStr = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        return self.__builder[(action, breakdown, action_breakdown)](structure_details, value)

    def remove_gender(self, structure_details: typing.Dict = None, value: typing.AnyStr = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        targeting = structure_details["targeting"]
        if value == GenderEnum.MALE.value[0]:
            targeting["flexible_spec"]["genders"] = [GenderEnum.FEMALE.value[1]]
        elif value == GenderEnum.FEMALE.value[0]:
            targeting["flexible_spec"]["genders"] = [GenderEnum.MALE.value[1]]
        elif value == GenderEnum.UNKNOWN.value[0]:
            targeting["flexible_spec"]["genders"] = [GenderEnum.MALE.value[1], GenderEnum.FEMALE.value[1]]
        else:
            raise ValueError(f"Unknown gender {value}")

        action_details = {
            "details": {
                "targeting": targeting
            }
        }
        return action_details

    def remove_placement(self, structure_details: typing.Dict = None, value: typing.AnyStr = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        targeting = structure_details["targeting"]
        if value:
            publisher_platform_value, placement_position_value, device_platform_value = value.split(",")
            # remove publisher platform
            #  publisher platform breakdowns give data for {publisher_platform}_app and {
            # publisher_platform}_web, but targeting only accepts {publisher_platform}
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
        else:
            raise ValueError("Missing placement information.")

    def remove_impression_device(self,
                                 structure_details: typing.Dict = None,
                                 value: typing.AnyStr = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        targeting = structure_details["targeting"]
        if value in targeting["flexible_spec"][ImpressionDeviceEnum.USER_DEVICE.value]:
            targeting["flexible_spec"][ImpressionDeviceEnum.USER_DEVICE.value].remove(value)
        elif value.title() in targeting["flexible_spec"][ImpressionDeviceEnum.USER_DEVICE.value]:
            targeting["flexible_spec"][ImpressionDeviceEnum.USER_DEVICE.value].remove(value.title())
            # construct action details
            action_details = {
                "details": {
                    "targeting": targeting
                }
            }
            return action_details

    def change_budget(self, structure_details: typing.Dict = None, value: typing.AnyStr = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        if structure_details[BudgetTypeEnum.DAILY.value]:
            action_details = {
                "details": {
                    BudgetTypeEnum.DAILY.value: value * 100
                }
            }
        elif structure_details[BudgetTypeEnum.LIFETIME.value]:
            action_details = {
                "details": {
                    BudgetTypeEnum.LIFETIME.value: value * 100
                }
            }
        else:
            raise ValueError(f"Unknown budget type.")

        return action_details

    def pause_structure(self, structure_details: typing.Dict = None, value: typing.AnyStr = None) -> typing.Dict:
        action_details = {"details": {"status": "PAUSE"}}
        return action_details

    def split_age(self, structure_details: typing.Dict = None, value: typing.AnyStr = None) -> typing.Union[typing.Dict, typing.NoReturn]:
        #  todo: find out how to implement an age group split ( i.e. remove age 25-30 )
        return None
