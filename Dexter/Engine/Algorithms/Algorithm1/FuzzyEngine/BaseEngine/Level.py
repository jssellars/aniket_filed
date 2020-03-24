from numpy import linspace

from Algorithms.Algorithm1.FuzzyEngine.BaseEngine.MembershipFunction import MembershipFunction


class Level(object):

    def __init__(self, name, maxValue, membershipFunctionDefinition):
        self.name = name
        self.maxValue = maxValue
        self.membershipFunctionDefinition = membershipFunctionDefinition
        self.membershipFunction = MembershipFunction().GetMembershipFunction(
            self.membershipFunctionDefinition.functionType)

    def GetAllLevelValues(self, step=0.01):
        nPoints = 1.0 / step
        x = linspace(0.0, 1.0, nPoints)

        # TODO: rewrite this using map
        values = []
        for xi in x:
            currentValue = self.membershipFunction(xi, self.membershipFunctionDefinition.parameters)
            if self.maxValue and currentValue > self.maxValue:
                currentValue = self.maxValue
            elif currentValue < 0:
                currentValue = 0
            values.append(currentValue)

        return values

    def EvaluateMembership(self, value):
        return self.membershipFunction(value, self.membershipFunctionDefinition.parameters)


class MembershipFunctionDefinition(object):

    def __init__(self, functionType=None, parameters=None):
        self.functionType = functionType
        self.parameters = parameters
