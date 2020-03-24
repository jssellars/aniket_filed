from numpy import linspace

from Algorithms.Dexter_Fuzzy_Inference.FuzzyEngine.BaseEngine.MembershipFunction import MembershipFunction


class Level(object):

    def __init__(self, name, max_value, membership_function_definition):
        self.name = name
        self.max_value = max_value
        self.membership_function_definition = membership_function_definition
        self.membership_function = MembershipFunction().get_membership_function(
            self.membership_function_definition.functionType)

    def get_all_level_values(self, step=0.01):
        n_points = 1.0 / step
        x = linspace(0.0, 1.0, n_points)

        # TODO: rewrite this using map
        values = []
        for xi in x:
            current_value = self.membership_function(xi, self.membership_function_definition.parameters)
            if self.max_value and current_value > self.max_value:
                current_value = self.max_value
            elif current_value < 0:
                current_value = 0
            values.append(current_value)

        return values

    def evaluate_membership(self, value):
        return self.membership_function(value, self.membership_function_definition.parameters)


class MembershipFunctionDefinition(object):

    def __init__(self, function_type=None, parameters=None):
        self.function_type = function_type
        self.parameters = parameters
