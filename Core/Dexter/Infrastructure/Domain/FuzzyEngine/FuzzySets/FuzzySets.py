import typing
from enum import Enum

from Core.Dexter.Infrastructure.Domain.FuzzyEngine.FuzzySets.FuzzyMembershipFunction import FuzzyMembershipFunctionBase


class LinguisticVariableEnumBase(Enum):
    pass


class LinguisticVariable:
    def __init__(self,
                 level: LinguisticVariableEnumBase = None,
                 membership_function: FuzzyMembershipFunctionBase = None):
        self.level = level
        self.membership_function = membership_function


class Fuzzyfier:
    def __init__(self, metric_name: typing.AnyStr = None, linguistic_levels: typing.List[LinguisticVariable] = None):
        self.metric_name = metric_name
        self.linguistic_levels = linguistic_levels
        self.__levels = None

    def fuzzyfy(self,
                value: typing.Any = None,
                linguistic_level: LinguisticVariableEnumBase = None) -> typing.Tuple[
                LinguisticVariableEnumBase, float]:
        fuzzy_class = None
        fuzzy_value = 0.0
        membership_function = self.__get_membership_function_by_linguistic_level(linguistic_level)
        if membership_function:
            fuzzy_value = membership_function.evaluate(value)
            fuzzy_class = linguistic_level
        return fuzzy_class, fuzzy_value

    def __get_membership_function_by_linguistic_level(self,
                                                      linguistic_level: LinguisticVariableEnumBase = None) -> \
            FuzzyMembershipFunctionBase:
        linguistic_level_value = next(filter(lambda x: x.level == linguistic_level, self.linguistic_levels), None)
        if not linguistic_level_value:
            raise ValueError(f"Invalid linguistic variable level {linguistic_level.value}")
        return linguistic_level_value.membership_function

    @property
    def levels(self):
        if not self.__levels:
            self.__levels = [linguistic_level.level for linguistic_level in self.linguistic_levels]
        return self.__levels
