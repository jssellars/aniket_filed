import typing

import numpy as np


class FuzzyMembershipFunctionBase:
    _params = None

    def set_params(self, **kwargs):
        self._params = kwargs

    def evaluate(self, x: typing.Union[int, float]) -> typing.Union[float, typing.NoReturn]:
        if x is None:
            return None
        if self._params:
            return self._membership_function(x, **self._params)
        else:
            return self._membership_function(x)

    def _membership_function(self, x: float = None, **kwargs) -> float:
        pass

    @staticmethod
    def _normalize_result(result: float = None):
        if result < 0:
            return 0.0
        if result > 1:
            return 1.0
        return result


class LinearMembershipFunction(FuzzyMembershipFunctionBase):

    def __init__(self, a: float = None, b: float = 0):
        self._params = {
            "a": a,
            "b": b
        }

    def _membership_function(self, x: float = None, a: float = None, b: float = None) -> float:
        result = a * x + b
        return self._normalize_result(result)


class SigmoidMembershipFunction(FuzzyMembershipFunctionBase):
    def __init__(self, L: float = None, k: float = None, x0: float = None):
        self._params = {
            "L": L,
            "k": k,
            "x0": x0
        }

    def _membership_function(self, x: float = None, L: float = None, k: float = None, x0: float = None) -> float:
        result = L / (1 + np.exp(-k * (x - x0)))
        return self._normalize_result(result)


class StepMembershipFunction(FuzzyMembershipFunctionBase):
    def __init__(self, a: float = None, b: float = None):
        self._params = {
            "a": a,
            "b": b
        }

    def _membership_function(self, x: float = None, a: float = None, b: float = None) -> float:
        if a <= x <= b:
            return 1.0
        else:
            return 0.0


class ExponentialMembershipFunction(FuzzyMembershipFunctionBase):
    def __init__(self, x0: float = 0, a: float = None, b: float = None):
        self._params = {
            "x0": x0,
            "a": a,
            "b": b
        }

    def _membership_function(self, x: float = None, x0: float = None, a: float = None, b: float = None) -> float:
        if b is None:
            result = a * np.exp(x - x0)
        else:
            result = a * b ** (x - x0)
        return self._normalize_result(result)


class SawToothMembershipFunction(FuzzyMembershipFunctionBase):
    def __init__(self, x0: float = None, a1: float = None, b1: float = None, a2: float = None, b2: float = None):
        self._params = {
            "x0": x0,
            "a1": a1,
            "b1": b1,
            "a2": a2,
            "b2": b2
        }

    def _membership_function(self, x: float = None, x0: float = None, a1: float = None, b1: float = None,
                             a2: float = None, b2: float = None) -> float:
        if x <= x0:
            result = a1 * x + b1
        else:
            result = a2 * x + b2
        return self._normalize_result(result)


class TrapezeMembershipFunction(FuzzyMembershipFunctionBase):
    def __init__(self, x1: float = None, a1: float = None, b1: float = None, x2: float = None, a2: float = None,
                 b2: float = None):
        self._params = {
            "x1": x1,
            "a1": a1,
            "b1": b1,
            "x2": x2,
            "a2": a2,
            "b2": b2
        }

    def _membership_function(self, x: float = None, x1: float = None, a1: float = None, b1: float = None,
                             x2: float = None, a2: float = None, b2: float = None) -> float:
        if x <= x1:
            result = a1 * x + b1
        elif x1 < x <= x2:
            result = 1
        else:
            result = a2 * x + b2
        return self._normalize_result(result)


class GaussMembershipFunction(FuzzyMembershipFunctionBase):
    def __init__(self, a: float = None, b: float = None, c: float = None):
        self._params = {
            "a": a,
            "b": b,
            "c": c
        }

    def _membership_function(self, x: float = None, a: float = None, b: float = None, c: float = None) -> float:
        exp = (x - b) ** 2 / (2 * c ** 2)
        result = a * np.exp(-exp)
        return self._normalize_result(result)
