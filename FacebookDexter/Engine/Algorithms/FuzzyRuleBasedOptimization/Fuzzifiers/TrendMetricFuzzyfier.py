from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets import LinearMembershipFunction
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets import Fuzzyfier, LinguisticVariable, LinguisticVariableEnum
from FacebookDexter.Engine.Algorithms.Algorithm2.RuleBasedOptimization.MetricFuzzyfierCollectionBase import MetricFuzzyfierCollectionBase


class TrendMetricFuzzyfierCollection(MetricFuzzyfierCollectionBase):
    cpc = Fuzzyfier([LinguisticVariable(LinguisticVariableEnum.DECREASING, LinearMembershipFunction(a=1, b=1)),
                     LinguisticVariable(LinguisticVariableEnum.INCREASING, LinearMembershipFunction(a=2, b=2))])

