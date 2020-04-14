from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzyMembershipFunction import LinearMembershipFunction
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import Fuzzyfier, LinguisticVariable, LinguisticVariableEnum
from FacebookDexter.Infrastructure.FuzzyEngine.MetricFuzzyfierCollectionBase import MetricFuzzyfierCollectionBase


class AggregatedMetricFuzzyfierCollection(MetricFuzzyfierCollectionBase):
    cpc = Fuzzyfier([LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(a=1, b=1)),
                     LinguisticVariable(LinguisticVariableEnum.MEDIUM, LinearMembershipFunction(a=2, b=2)),
                     LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(a=2, b=2))])