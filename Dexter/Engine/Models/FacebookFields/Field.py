# TODO: Change FieldType to real enum :)
# TODO: Make Field more abstract to allow you to represent any information from FB easily
class FieldType:
    simple = 1
    nested = 2
    structure = 3
    total = 4
    cost = 5
    breakdown = 6
    action_breakdown = 7
    time_breakdown = 8


class Field:

    def __init__(self,
                 name=None,
                 source_field_name=None,
                 fields=None,
                 breakdowns=None,
                 action_breakdowns=None,
                 action_field_name_key=None,
                 action_field_name_value=None,
                 action_field_value_key=None,
                 spend_value_key=None,
                 type_id=FieldType.simple):

        self.__name = name

        self.__source_field_name = source_field_name

        self.__fields = fields if fields else []

        self.__breakdowns = breakdowns if breakdowns else []

        self.__action_breakdowns = action_breakdowns if action_breakdowns else []

        self.__action_field_name_key = action_field_name_key

        self.__action_field_name_value = action_field_name_value

        self.__action_field_value_key = action_field_value_key if action_field_value_key else "value"

        self.__spend_value_key = spend_value_key if spend_value_key else "spend"

        self.__type_id = type_id

    @property
    def name(self):
        return self.__name

    @property
    def source_field_name(self):
        return self.__source_field_name

    @property
    def fields(self):
        return self.__fields

    @property
    def breakdowns(self):
        return self.__breakdowns

    @property
    def action_breakdowns(self):
        return self.__action_breakdowns

    @property
    def action_field_name_key(self):
        return self.__action_field_name_key

    @property
    def action_field_name_value(self):
        return self.__action_field_name_value

    @property
    def action_field_value_key(self):
        return self.__action_field_value_key

    @property
    def spend_value_key(self):
        return self.__spend_value_key

    @property
    def type_id(self):
        return self.__type_id