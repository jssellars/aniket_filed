from numpy import asarray
from numpy import where 

from Algorithms.Algorithm1.FuzzyEngine.BaseEngine.MembershipFunction import MembershipFunction


class Union(object):

    @staticmethod 
    def ComputeUnion(value, membershipFunctionA, membershipFunctionB):
        functionA = MembershipFunction().GetMembershipFunction(membershipFunctionA.functionType)
        functionB = MembershipFunction().GetMembershipFunction(membershipFunctionB.functionType)

        return max(functionA(x, membershipFunctionA.parameters), functionB(x, membershipFunctionB.parameters))


class Intersection(object):
    
    @staticmethod
    def ComputeIntersection(value, membershipFunctionA, membershipFunctionB):
        functionA = MembershipFunction().GetMembershipFunction(membershipFunctionA.functionType)
        functionB = MembershipFunction().GetMembershipFunction(membershipFunctionB.functionType)

        return min(functionA(x, membershipFunctionA.parameters), functionB(x, membershipFunctionB.parameters))


class Complement(object):

    @staticmethod
    def ComputeComplement(value, membershipFunctionA):
        functionA = MembershipFunction().GetMembershipFunction(membershipFunctionA.functionType)

        return 1 - functionA(x, membershipFunctionA.parameters)


class And(object):
    
    @staticmethod
    def Min(precedent, antecedent):
        if precedent is None:
            return antecedent

        if antecedent is None:
            return precedent

        return min(precedent, antecedent)


class Or(object):
    
    @staticmethod
    def Max(precedent, antecedent):
        if precedent is None:
            return antecedent

        if antecedent is None:
            return precedent

        return max(precedent, antecedent)


class Implication(object):

    @staticmethod
    def Min(antecedent, consequent):
        if isinstance(consequent, list):
            consequent = asarray(consequent)

        return where(consequent > antecedent, antecedent, consequent)

    @staticmethod
    def Product(antecedent, consequent):
        if isinstance(consequent, list):
            consequent = asarray(consequent)

        result = antecedent * consequent
        return where(result > 1, 1, result) # eliminate values > 1 


class Aggregator(object):

    @staticmethod
    def Max(*args):
        args = args[0]
        result = args[0]
        if len(args) > 1:
            for arg in args[1:]:
                for index, value in enumerate(arg):
                    if result[index] < value:
                        result[index] = value
        return result
