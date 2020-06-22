import typing

from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperBase import FieldMapperBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperResult import FieldMapperResult


class BudgetFieldMapper(FieldMapperBase):
    __non_convertible_fields = [GraphAPIInsightsFields.account_id,
                                GraphAPIInsightsFields.campaign_id,
                                GraphAPIInsightsFields.adset_id,
                                GraphAPIInsightsFields.ad_id]

    def __init__(self, facebook_field_names: typing.List[typing.Any] = None):
        self.facebook_field_names = facebook_field_names
        super().__init__()

    def set_mapper_parameters(self, facebook_field_names: typing.List[typing.Any] = None):
        self.facebook_field_names = facebook_field_names
        return self

    def map(self, data: typing.Dict, field: typing.Any = None, **kwargs) -> typing.List[FieldMapperResult]:
        budget = data.get(field.name, None)
        if budget is not None:
            field_value = self._convert_to_float(budget)
            return [FieldMapperResult().set_field(field.name, field_value)]
