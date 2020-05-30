import typing
from enum import Enum

from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldMapper import ActionFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.BreakdownValueFieldMapper import BreakdownValueFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.BudgetFieldMapper import BudgetFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.CostPerActionFieldMapper import CostPerActionFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.OneToOneFieldMapper import OneToOneFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.StructureFieldMapper import StructureFieldMapper
from Core.Web.FacebookGraphAPI.GraphAPIMappings.TimeBreakdownValueFieldMapper import TimeBreakdownValueFieldMapper
from Core.Web.FacebookGraphAPI.Models.FieldAggregationTypeEnum import FieldAggregationTypeEnum
from Core.Web.FacebookGraphAPI.Models.FieldDataTypeEnum import FieldDataTypeEnum

MapperType = typing.Union[ActionFieldMapper,
                          CostPerActionFieldMapper,
                          OneToOneFieldMapper,
                          StructureFieldMapper,
                          BreakdownValueFieldMapper,
                          TimeBreakdownValueFieldMapper,
                          BudgetFieldMapper]


class FieldType(Enum):
    INSIGHT = 1
    ACTION_INSIGHT = 2
    STRUCTURE = 3
    BREAKDOWN = 4
    ACTION_BREAKDOWN = 5
    TIME_BREAKDOWN = 6


class Field:

    def __init__(self,
                 name: typing.AnyStr = None,
                 facebook_fields: typing.List[typing.AnyStr] = None,
                 facebook_value: typing.Union[int, typing.AnyStr] = None,
                 action_breakdowns: typing.List[typing.AnyStr] = None,
                 requested_action_breakdowns: typing.List[typing.Any] = None,  # List<Field>
                 mapper: MapperType = None,
                 field_type: FieldType = FieldType.INSIGHT,
                 aggregation_type_id: int = FieldAggregationTypeEnum.SUM.value,
                 data_type_id: int = FieldDataTypeEnum.NUMBER.value):
        self.name = name
        self.facebook_fields = facebook_fields if facebook_fields else []
        self.facebook_value = facebook_value
        self.action_breakdowns = action_breakdowns if action_breakdowns else []
        self.requested_action_breakdowns = requested_action_breakdowns if requested_action_breakdowns else []
        self.mapper = mapper
        self.field_type = field_type

        # FE properties
        # todo: find a better way to provide these FE properties on a Field
        self.aggregation_id = aggregation_type_id
        self.type_id = data_type_id

        self.__init_mapper()

    def __init_mapper(self):
        mapper_dict = {
            BreakdownValueFieldMapper().type: self.__init_breakdown_mapper,
            OneToOneFieldMapper().type: self.__init_one_to_one_mapper,
            ActionFieldMapper().type: self.__init_action_mapper,
            CostPerActionFieldMapper().type: self.__init_cost_per_action_mapper,
            StructureFieldMapper().type: self.__init_structure_mapper
        }
        if self.mapper:
            init_mapper_method = mapper_dict.get(self.mapper.type, None)
            if init_mapper_method:
                init_mapper_method()

    def __init_breakdown_mapper(self):
        if not self.mapper.facebook_field_names:
            return self.mapper.set_mapper_parameters(self.facebook_fields)

    def __init_one_to_one_mapper(self):
        if not self.mapper.facebook_field_name:
            return self.mapper.set_mapper_parameters(self.facebook_fields[0])

    def __init_action_mapper(self):
        if not self.mapper.facebook_field_name and not self.mapper.facebook_field_value_name:
            return self.mapper.set_mapper_parameters(facebook_field_name=self.facebook_fields[0],
                                                     facebook_field_value_name=GraphAPIInsightsFields.value)

    def __init_cost_per_action_mapper(self):
        if not self.mapper.facebook_field_name and not self.mapper.facebook_field_value_name and not self.mapper.facebook_spend_field_name:
            return self.mapper.set_mapper_parameters(facebook_field_name=self.facebook_fields[0],
                                                     facebook_field_value_name=GraphAPIInsightsFields.value,
                                                     facebook_spend_field_name=GraphAPIInsightsFields.spend)

    def __init_structure_mapper(self):
        if not self.mapper.facebook_field_name:
            return self.mapper.set_mapper_parameters(facebook_field_name=self.facebook_fields[0])

    def to_dict(self):
        return {
            'name': self.name,
            'type_id': self.type_id,
            'aggregation_id': self.aggregation_id,
        }

    def to_json(self):
        return self.to_dict()
