import itertools
import typing
from collections import ChainMap, namedtuple

from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperResult import FieldMapperResult
from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ObjectiveToResultsMapper import (
    PixelCustomEventTypeToResult,
    AdSetOptimizationToResult,
    PixelCustomEventTypeToCostPerResult,
    AdSetOptimizationToCostPerResult
)
from Core.Web.FacebookGraphAPI.Models.Field import Field, FieldType
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata

ActionBreakdownMinimal = namedtuple('ActionBreakdownMinimal', ['name', 'facebook_fields'])


class GraphAPIInsightsMapper:

    def map(self, requested_fields=None, response=None):
        if not response:
            return []
        return self.map_response(
            requested_fields=requested_fields,
            response=response
        )

    @classmethod
    def map_response(cls, requested_fields: typing.List[Field] = None, response: typing.List[typing.Dict] = None):
        mapped_response = []
        for data in response:
            mapped_fields = []
            try:
                mapped_fields = cls.map_field_all(requested_fields, data)
            except Exception as e:
                import traceback
                traceback.print_exc()
                pass

            if mapped_fields:
                mapped_fields = [field for field in mapped_fields if field is not None]
                mapped_data = [dict(ChainMap(*entry)) for entry in itertools.product(*mapped_fields)]
                mapped_response.extend(mapped_data)
        return mapped_response

    @classmethod
    def map_field_all(cls,
                      requested_fields: typing.List[Field] = None,
                      data: typing.Dict = None) -> typing.List[typing.List[FieldMapperResult]]:
        requested_fields = cls.__append_requested_action_breakdowns(requested_fields)
        mapped_fields = []
        for index in range(len(requested_fields)):
            if requested_fields[index].field_type != FieldType.ACTION_BREAKDOWN:
                if requested_fields[index].name == FieldsMetadata.results.name or \
                        requested_fields[index].name == FieldsMetadata.cost_per_result.name:
                    cls.__get_results_from_data(
                        data=data,
                        mapped_fields=mapped_fields,
                        requested_field=requested_fields[index]
                    )
                else:
                    mapped_fields.append(requested_fields[index].mapper.map(data, requested_fields[index]))
        return mapped_fields

    @classmethod
    def __append_requested_action_breakdowns(cls, requested_fields: typing.List[Field]):
        action_breakdowns = [field for field in requested_fields
                             if field is not None and field.field_type == FieldType.ACTION_BREAKDOWN]
        for index in range(len(requested_fields)):
            if requested_fields[index].field_type == FieldType.ACTION_INSIGHT:
                requested_fields[index].requested_action_breakdowns.extend(action_breakdowns)
        return requested_fields

    @classmethod
    def __get_results_from_data(cls, data, mapped_fields, requested_field):
        facebook_results_field_value = None

        if requested_field.name == FieldsMetadata.results.name:
            if GraphAPIInsightsFields.custom_event_type in data.keys():
                custom_event_type = PixelCustomEventTypeToResult.get_enum_by_name(data[GraphAPIInsightsFields.custom_event_type])
                if custom_event_type:
                    facebook_results_field_value = custom_event_type.value
            elif GraphAPIInsightsFields.optimization_goal in data.keys():
                optimization_goal = AdSetOptimizationToResult.get_enum_by_name(data[GraphAPIInsightsFields.optimization_goal])
                if optimization_goal:
                    facebook_results_field_value = optimization_goal.value

        elif requested_field.name == FieldsMetadata.cost_per_result.name:
            if GraphAPIInsightsFields.custom_event_type in data.keys():
                cost_per_custom_event_type = PixelCustomEventTypeToCostPerResult.get_enum_by_name(data[GraphAPIInsightsFields.custom_event_type])
                if cost_per_custom_event_type:
                    facebook_results_field_value = cost_per_custom_event_type.value
            elif GraphAPIInsightsFields.optimization_goal in data.keys():
                cost_per_optimization_goal = AdSetOptimizationToCostPerResult.get_enum_by_name(data[GraphAPIInsightsFields.optimization_goal])
                if cost_per_optimization_goal:
                    facebook_results_field_value = cost_per_optimization_goal.value

        if facebook_results_field_value:
            result_value = facebook_results_field_value.mapper.map(data, facebook_results_field_value)
            mapped_fields.append([{requested_field.name: result_value[0].get(facebook_results_field_value.name)}])

