import typing

from GoogleDexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from GoogleDexter.Infrastructure.Domain.Metrics.Metric import Metric
from GoogleDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum


class Antecedent:

    def __init__(self,
                 aid: int = None,
                 metric: Metric = None,
                 expected_value: typing.Any = None,
                 operator: LogicOperatorEnum = None,
                 atype: AntecedentTypeEnum = None):
        self.id = aid
        self.metric = metric
        self.expected_value = expected_value
        self.operator = operator
        self.type = atype
        self.__metric_value = None

    def evaluate(self, metric_value: typing.Any = None) -> bool:
        self.__metric_value = metric_value
        return self.__evaluate()

    def __evaluate(self):
        if self.operator == LogicOperatorEnum.AND:
            if self.__metric_value is None:
                return False
            return self.__metric_value and self.expected_value

        if self.operator == LogicOperatorEnum.OR:
            if self.__metric_value is None:
                return False
            return self.__metric_value or self.expected_value

        if self.operator == LogicOperatorEnum.NOT:
            if self.__metric_value is None:
                return False
            return not self.__metric_value

        if self.operator == LogicOperatorEnum.EQUALS:
            if self.__metric_value is None:
                return False
            return self.__metric_value == self.expected_value

        if self.operator == LogicOperatorEnum.NOT_EQUAL:
            if self.__metric_value is None:
                return False
            return self.__metric_value != self.expected_value

        if self.operator == LogicOperatorEnum.EQUAL_OR_GREATER_THAN:
            if self.__metric_value is None:
                return False
            return self.__metric_value >= self.expected_value

        if self.operator == LogicOperatorEnum.EQUAL_OR_LESS_THAN:
            if self.__metric_value is None:
                return False
            return self.__metric_value <= self.expected_value

        if self.operator == LogicOperatorEnum.LESS_THAN:
            if self.__metric_value is None:
                return False
            return self.__metric_value < self.expected_value

        if self.operator == LogicOperatorEnum.IN:
            if self.__metric_value is None:
                return False
            return self.__metric_value in self.expected_value

        if self.operator == LogicOperatorEnum.NOT_IN:
            if self.__metric_value is None:
                return False
            return self.__metric_value not in self.expected_value
