import itertools
import typing
from enum import Enum

from Core.Web.FacebookGraphAPI.GraphAPIDomain.GraphAPIInsightsFields import GraphAPIInsightsFields
from Core.Web.FacebookGraphAPI.GraphAPIMappings.ActionFieldCondition import ActionFieldCondition
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperBase import FieldMapperBase
from Core.Web.FacebookGraphAPI.GraphAPIMappings.FieldMapperResult import FieldMapperResult


class StructureDetailsTypeEnum(Enum):
    ADCREATIVES = GraphAPIInsightsFields.adcreatives_structure
    TARGETING_SENTENCE_LINES = GraphAPIInsightsFields.targetingsentencelines
    TRACKING_SPECS = GraphAPIInsightsFields.tracking_specs
    PROMOTED_OBJECT = GraphAPIInsightsFields.promoted_object


class StructureFieldMapper(FieldMapperBase):
    START_INDEX = 0

    def __init__(self,
                 facebook_field_name: typing.AnyStr = None,
                 field_filter: typing.List[ActionFieldCondition] = None,
                 structure_details_type: StructureDetailsTypeEnum = StructureDetailsTypeEnum.ADCREATIVES):
        self.facebook_field_name = facebook_field_name
        self.filter = field_filter
        self.structure_details_type = structure_details_type
        super().__init__()

    def set_mapper_parameters(self, facebook_field_name: typing.List[typing.AnyStr] = None):
        self.facebook_field_name = facebook_field_name
        return self

    def map(self, data: typing.Dict, field: typing.Any = None, **kwargs) -> typing.List[FieldMapperResult]:
        if self.structure_details_type == StructureDetailsTypeEnum.ADCREATIVES:
            adcreatives = data.get(self.structure_details_type.value, None)
            field_value = None
            if adcreatives:
                adcreatives = adcreatives.get(GraphAPIInsightsFields.data_field, None)
                field_value = adcreatives.get(self.facebook_field_name, None)

            return [FieldMapperResult().set_field(field.name, field_value)]

        if self.structure_details_type == StructureDetailsTypeEnum.TARGETING_SENTENCE_LINES:
            values = [value.get(GraphAPIInsightsFields.targeting_sentence_lines_children, None) for value in data
                      if self._is_desired_field(value, self.filter)]
            field_value = ", ".join(list(itertools.chain(*values)))
            return [FieldMapperResult().set_field(field.name, field_value)]

        if self.structure_details_type == StructureDetailsTypeEnum.TRACKING_SPECS:
            values = data.get(GraphAPIInsightsFields.tracking_specs, None)
            field_value = None
            if values:
                field_value = [value.get[GraphAPIInsightsFields.page_id_structure][0] for value in values
                               if GraphAPIInsightsFields.page_id_structure in value.keys()][0]
            return [FieldMapperResult().set_field(field.name, field_value)]

        if self.structure_details_type == StructureDetailsTypeEnum.PROMOTED_OBJECT:
            value = data.get(GraphAPIInsightsFields.promoted_object, None)
            field_value = None
            if value:
                field_value = value.get(self.facebook_field_name, None)
            return [FieldMapperResult().set_field(field.name, field_value)]
