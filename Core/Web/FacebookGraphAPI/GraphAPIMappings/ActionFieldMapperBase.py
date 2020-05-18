import copy
import typing

from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import ActionFieldCondition
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperBase import FieldMapperBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperResult import FieldMapperResult


class ActionFieldMapperBase(FieldMapperBase):

    def __init__(self,
                 facebook_field_value_name: typing.AnyStr = None,
                 field_filter: typing.List[ActionFieldCondition] = None):
        self.facebook_field_value_name = facebook_field_value_name
        self.filter = field_filter
        super().__init__()

    def set_mapper_parameters(self, facebook_field_value_name: typing.AnyStr = None):
        self.facebook_field_value_name = facebook_field_value_name
        return self

    def set_filter(self, field_filter: typing.List[ActionFieldCondition] = None):
        self.filter = field_filter
        return self

    def map(self, **kwargs):
        pass

    def _map(self,
             data: typing.List[typing.Dict] = None,
             field: typing.Any = None,  # Field
             facebook_spend: typing.Union[float, None] = None) -> typing.List[FieldMapperResult]:
        if not data:
            return [FieldMapperResult().set_field(field.name)]

        mapper_results_all = []
        for entry in data:
            if self._is_desired_field(entry, self.filter):
                mapper_results = self.__map_value(entry, field, facebook_spend)
                mapper_results_all = self.__extend_unique_mapper_results(mapper_results_all, mapper_results)
        return mapper_results_all

    @staticmethod
    def __extend_unique_mapper_results(results_all: typing.List[FieldMapperResult] = None,
                                       results_partial: typing.List[FieldMapperResult] = None) -> typing.List[
        FieldMapperResult]:
        for result in results_partial:
            if result not in results_all:
                results_all.append(copy.deepcopy(result))
        return results_all

    def __map_value(self,
                    entry: typing.Dict = None,
                    field: typing.Any = None,
                    facebook_spend: float = None) -> typing.List[FieldMapperResult]:
        if field.requested_action_breakdowns:
            return self.__map_field_with_action_breakdowns(entry, field, facebook_spend)
        else:
            return self.__map_field_without_action_breakdowns(entry, field, facebook_spend)

    def __map_field_without_action_breakdowns(self,
                                              data: typing.Dict = None,
                                              field: typing.Any = None,
                                              facebook_spend: float = None) -> typing.List[FieldMapperResult]:
        results = []
        # create a new mapper result and add field value
        mapper_result = self.__set_result_field_value(data, field)

        # set cost field value if facebook_spend is not null
        mapper_result = self.__set_cost_field_value(mapper_result, field, facebook_spend)

        results.append(copy.deepcopy(mapper_result))
        return results

    def __map_field_with_action_breakdowns(self,
                                           data: typing.Dict = None,
                                           field: typing.Any = None,
                                           facebook_spend: float = None) -> typing.List[FieldMapperResult]:
        results = []
        for action_breakdown_field in field.requested_action_breakdowns:
            # create a new mapper result and add field value
            mapper_result = self.__set_result_field_value(data, field)

            # add action breakdown value to current mapper result
            action_breakdown_field_value = [data.get(facebook_field_name, None)
                                            for facebook_field_name in action_breakdown_field.facebook_fields]

            # only process action breakdown if found in the FB response
            if None not in action_breakdown_field_value:
                action_breakdown_field_value = ", ".join(action_breakdown_field_value)
                mapper_result.set_field(action_breakdown_field.name, action_breakdown_field_value)

                # set cost field value if facebook_spend is not null
                mapper_result = self.__set_cost_field_value(mapper_result, field, facebook_spend)

                results.append(copy.deepcopy(mapper_result))
        return results

    def __set_result_field_value(self, data: typing.Dict = None, field: typing.Any = None) -> FieldMapperResult:
        field_value = self._convert_to_float(data.get(self.facebook_field_value_name, None))
        mapper_result = FieldMapperResult().set_field(field.name, field_value)
        return mapper_result

    @staticmethod
    def __set_cost_field_value(mapper_result: FieldMapperResult = None, field: typing.Any = None,
                               facebook_spend: float = None):
        if facebook_spend:
            cost = facebook_spend / mapper_result[field.name] if mapper_result[field.name] else None
            mapper_result.set_field(field.name, cost)
        return mapper_result
