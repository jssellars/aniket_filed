import typing

import numpy as np


class FuzzyMembershipFunctionBase:
    __params = None
    __membership_function = None

    def set_params(self, **kwargs):
        self.__params = kwargs

    def evaluate(self, value: typing.Any) -> typing.Union[float, typing.NoReturn]:
        if self.__params:
            return self._membership_function(value, **self.__params)
        else:
            return self._membership_function(value)

    def _membership_function(self, value: typing.Any, **kwargs):
        pass


class LinearMembershipFunction(FuzzyMembershipFunctionBase):

    def __init__(self, a: float = None, b: float = None):
        self.__params = {
            "a": a,
            "b": b
        }

    def _membership_function(self, value: typing.AnyStr, a: float = None, b: float = None) -> float:
        return a * value + b


class SigmoidMembershipFunction(FuzzyMembershipFunctionBase):
    def __init__(self, L: float = None, k: float = None, x0: float = None):
        self.__params = {
            "L": L,
            "k": k,
            "x0": x0
        }

    def _membership_function(self, value: typing.Any, L: float = None, k: float = None, x0: float = None):
        return L / (1 + np.exp(-k*(value-x0)))
