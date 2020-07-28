import typing
from dataclasses import dataclass
from enum import Enum

from Core.Tools.Misc.ObjectManipulators import extract_class_attributes_values
from Core.Web.FacebookGraphAPI.Models.Field import FieldType
from Core.Web.FacebookGraphAPI.Models.FieldsMetadata import FieldsMetadata
from FacebookTuring.Api.Catalogs.Breakdowns.ActionBreakdowns import ActionBreakdowns
from FacebookTuring.Api.Catalogs.Breakdowns.DeliveryBreakdowns import DeliveryBreakdowns
from FacebookTuring.Api.Catalogs.Breakdowns.TimeBreakdowns import TimeBreakdowns


@dataclass
class Breakdown:
    id: int = None
    column_name: typing.AnyStr = None
    display_name: typing.AnyStr = None


class BreakdownTypeEnum(Enum):
    DELIVERY = 1
    ACTION = 2
    ALL = 3


def get_breakdown_type(metrics):
    metric_types = []
    for metric in metrics:
        metric_field = getattr(FieldsMetadata, metric, None)
        metric_types.append(metric_field.field_type)
    metric_types = list(set(metric_types))
    if FieldType.INSIGHT in metric_types and FieldType.ACTION_INSIGHT in metric_types:
        return BreakdownTypeEnum.ALL

    if FieldType.INSIGHT in metric_types and FieldType.ACTION_INSIGHT not in metric_types:
        return BreakdownTypeEnum.DELIVERY

    if FieldType.INSIGHT not in metric_types and FieldType.ACTION_INSIGHT in metric_types:
        return BreakdownTypeEnum.ACTION


def extract_breakdown_columns(metrics):
    breakdown_type = get_breakdown_type(metrics)
    breakdowns = []
    if breakdown_type == BreakdownTypeEnum.ALL:
        breakdowns = extract_class_attributes_values(DeliveryBreakdowns)
        breakdowns += extract_class_attributes_values(ActionBreakdowns)

    if breakdown_type == BreakdownTypeEnum.DELIVERY:
        breakdowns = extract_class_attributes_values(DeliveryBreakdowns)

    if breakdown_type == BreakdownTypeEnum.ACTION:
        breakdowns = extract_class_attributes_values(ActionBreakdowns)

    breakdowns += extract_class_attributes_values(TimeBreakdowns)
    return breakdowns
