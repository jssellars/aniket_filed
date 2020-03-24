from numpy import asarray
from numpy import sum 


class Defuzzyfy(object):
    
    @staticmethod
    def centroid(support, membership_function_values):
        if isinstance(support, list):
            support = asarray(support)

        if isinstance(membership_function_values, list):
            membership_function_values = asarray(membership_function_values)

        return sum(support * membership_function_values) / sum(membership_function_values)
