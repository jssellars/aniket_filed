import typing

from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldMapperBase import ActionFieldMapperBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperResult import FieldMapperResult


class ActionFieldMapper(ActionFieldMapperBase):

    def __init__(self,
                 facebook_field_name: typing.AnyStr = None,
                 **kwargs):
        self.facebook_field_name = facebook_field_name
        super().__init__(**kwargs)

    def set_mapper_parameters(self,
                              facebook_field_name: typing.AnyStr = None,
                              facebook_field_value_name: typing.AnyStr = None):
        self.facebook_field_name = facebook_field_name
        self.facebook_field_value_name = facebook_field_value_name
        return self

    def map(self, data: typing.Dict = None, field: typing.Any = None) -> typing.List[FieldMapperResult]:
        result = self._map(data.get(self.facebook_field_name, None), field)
        if not result:
            result = [FieldMapperResult().set_field(field.name, None)]
        return result
