from numpy import asarray
from numpy import where

from Algorithms.Dexter_Fuzzy_Inference.FuzzyEngine.BaseEngine.MembershipFunction import MembershipFunction


class Union(object):

    @staticmethod
    def compute_union(value, membership_function_a, membership_function_b):
        function_a = MembershipFunction().get_membership_function(membership_function_a.function_type)
        function_b = MembershipFunction().get_membership_function(membership_function_b.function_type)

        return max(function_a(x, membership_function_a.parameters), function_b(x, membership_function_b.parameters))


class Intersection(object):

    @staticmethod
    def compute_intersection(value, membership_function_a, membership_function_b):
        function_a = MembershipFunction().get_membership_function(membership_function_a.function_type)
        function_b = MembershipFunction().get_membership_function(membership_function_b.function_type)

        return min(function_a(x, membership_function_a.parameters), function_b(x, membership_function_b.parameters))


class Complement(object):

    @staticmethod
    def compute_complement(value, membership_function_a):
        functionA = MembershipFunction().get_membership_function(membership_function_a.function_type)

        return 1 - functionA(x, membership_function_a.parameters)


class And(object):

    @staticmethod
    def min(precedent, antecedent):
        if precedent is None:
            return antecedent

        if antecedent is None:
            return precedent

        return min(precedent, antecedent)


class Or(object):

    @staticmethod
    def max(precedent, antecedent):
        if precedent is None:
            return antecedent

        if antecedent is None:
            return precedent

        return max(precedent, antecedent)


class Implication(object):

    @staticmethod
    def min(antecedent, consequent):
        if isinstance(consequent, list):
            consequent = asarray(consequent)

        return where(consequent > antecedent, antecedent, consequent)

    @staticmethod
    def product(antecedent, consequent):
        if isinstance(consequent, list):
            consequent = asarray(consequent)

        result = antecedent * consequent
        return where(result > 1, 1, result)  # eliminate values > 1


class Aggregator(object):

    @staticmethod
    def max(*args):
        args = args[0]
        result = args[0]
        if len(args) > 1:
            for arg in args[1:]:
                for index, value in enumerate(arg):
                    if result[index] < value:
                        result[index] = value
        return result
