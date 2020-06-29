import typing

from fastnumbers import fast_real

from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import ActionFieldCondition


class FieldMapperBase:

    @property
    def type(self):
        return self.__class__.__name__

    def _is_desired_field(self, data: typing.Dict, field_filter: typing.List[ActionFieldCondition] = None) -> bool:
        for condition in field_filter:
            try:
                if not condition.evaluate(data):
                    return False
            except Exception as e:
                raise NotImplementedError(str(e))
        return True

    @staticmethod
    def _convert_to_float(value):
        try:
            converted_value = fast_real(value)
        except Exception as e:
            converted_value = value
        return converted_value
