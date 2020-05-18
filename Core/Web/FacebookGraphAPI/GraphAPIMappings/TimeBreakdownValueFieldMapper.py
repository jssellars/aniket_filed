import typing

from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperBase import FieldMapperBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperResult import FieldMapperResult


class TimeBreakdownValueFieldMapper(FieldMapperBase):

    def __init__(self):
        super().__init__()

    @classmethod
    def map(cls, data: typing.Dict = None, field: typing.Any = None, **kwargs) -> typing.List[FieldMapperResult]:
        try:
            field_value = data[GraphAPIInsightsFields.date_start] + " - " + data[GraphAPIInsightsFields.date_stop]
        except KeyError as key_err:
            raise KeyError(str(key_err))
        except Exception as e:
            raise NotImplementedError(str(e))

        return [FieldMapperResult().set_field(field.name, field_value)]
