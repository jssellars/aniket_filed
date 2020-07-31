from Core.Dexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum


class Connective:

    def __init__(self, operator: LogicOperatorEnum = None):
        self.__operator = operator

    def evaluate(self, lvalue: bool = None, rvalue: bool = None) -> bool:
        if self.__operator == LogicOperatorEnum.AND:
            return lvalue and rvalue

        if self.__operator == LogicOperatorEnum.OR:
            return lvalue or rvalue
