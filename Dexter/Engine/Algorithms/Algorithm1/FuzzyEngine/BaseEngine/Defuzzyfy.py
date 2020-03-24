from numpy import asarray
from numpy import sum 


class Defuzzyfy(object):
    
    @staticmethod
    def Centroid(support, membershipFunctionValues):
        if isinstance(support, list):
            support = asarray(support)

        if isinstance(membershipFunctionValues, list):
            membershipFunctionValues = asarray(membershipFunctionValues)

        return sum(support * membershipFunctionValues) / sum(membershipFunctionValues)
