import typing

from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperBase import FieldMapperBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperResult import FieldMapperResult


class OneToOneFieldMapper(FieldMapperBase):
    __non_convertible_fields = [GraphAPIInsightsFields.account_id,
                                GraphAPIInsightsFields.campaign_id,
                                GraphAPIInsightsFields.adset_id,
                                GraphAPIInsightsFields.ad_id]

    def __init__(self, facebook_field_name: typing.AnyStr = None):
        self.facebook_field_name = facebook_field_name
        super().__init__()

    def set_mapper_parameters(self, facebook_field_name: typing.AnyStr = None):
        self.facebook_field_name = facebook_field_name
        return self

    def map(self, data: typing.Dict, field: typing.Any = None, **kwargs) -> typing.List[FieldMapperResult]:
        if field.name in self.__non_convertible_fields:
            field_value = data.get(self.facebook_field_name, None)
        else:
            field_value = data.get(self.facebook_field_name, None)
            field_value = self._convert_to_float(field_value)
        return [FieldMapperResult().set_field(field.name, field_value)]
