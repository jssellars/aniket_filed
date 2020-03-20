from enum import Enum


class FacebookFieldType(Enum):
    SIMPLE = 1
    NESTED = 2
    STRUCTURE = 3
    TOTAL = 4
    COST = 5
    BREAKDOWN = 6
    ACTION_BREAKDOWN = 7
    TIME_BREAKDOWN = 8


class FacebookField:

    def __init__(self,
                 name=None,
                 field_name=None,
                 fields=None,
                 breakdowns=None,
                 action_breakdowns=None,
                 action_field_name_key=None,
                 action_field_name_value=None,
                 action_field_value_key=None,
                 spend_field_name=None,
                 field_type=FacebookFieldType.SIMPLE):

        self.name = name

        self.field_name = field_name

        self.fields = fields if fields else []

        self.breakdowns = breakdowns if breakdowns else []

        self.action_breakdowns = action_breakdowns if action_breakdowns else []

        self.action_field_name_key = action_field_name_key

        self.action_field_name_value = action_field_name_value

        self.action_field_value_key = action_field_value_key if action_field_value_key else "value"

        self.spend_field_name = spend_field_name if spend_field_name else "spend"

        self.field_type = field_type