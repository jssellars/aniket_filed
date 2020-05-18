import typing

from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperBase import FieldMapperBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperResult import FieldMapperResult


class BreakdownValueFieldMapper(FieldMapperBase):

    def __init__(self, facebook_field_names: typing.List[typing.AnyStr] = None):
        self.facebook_field_names = facebook_field_names
        super().__init__()

    def set_mapper_parameters(self, facebook_field_names: typing.List[typing.AnyStr] = None):
        self.facebook_field_names = facebook_field_names
        return self

    def map(self, data: typing.Dict = None, field: typing.Any = None, **kwargs) -> typing.List[FieldMapperResult]:
        try:
            breakdown_values = [data[field_name] for field_name in self.facebook_field_names]
        except KeyError as key_err:
            raise KeyError(str(key_err))
        except Exception as e:
            raise NotImplementedError(str(e))
        field_value = ", ".join(breakdown_values)
        return [FieldMapperResult().set_field(field.name, field_value)]
