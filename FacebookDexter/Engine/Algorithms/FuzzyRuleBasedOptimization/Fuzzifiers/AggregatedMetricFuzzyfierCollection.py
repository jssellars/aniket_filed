from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzyMembershipFunction import LinearMembershipFunction, \
    StepMembershipFunction, \
    TrapezeMembershipFunction
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import Fuzzyfier, LinguisticVariable, \
    LinguisticVariableEnum

LOW_LINEAR_PARAMS = {
    "a": -10.0 / 3.0,
    "b": 1
}

MEDIUM_LINEAR_PARAMS = {
    "x1": 0.4,
    "a1": 20.0 / 3.0,
    "b1": -5.0 / 3.0,
    "x2": 0.6,
    "a2": -20.0 / 3.0,
    "b2": 5
}

HIGH_LINEAR_PARAMS = {
    "a": 10.0 / 3.0,
    "b": -7.0 / 3.0
}

AGGREGATED_METRIC_FUZZYFIER_COLLECTION = [
    Fuzzyfier(metric_name=AvailableMetricEnum.CPC.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.CPM.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.CTR.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.COST_PER_RESULT.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.COST_PER_APP_INSTALL.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.COST_PER_PURCHASE.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.COST_PER_THRUPLAY.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.FREQUENCY.value.name,
              linguistic_levels=[LinguisticVariable(LinguisticVariableEnum.LOW, StepMembershipFunction(a=0, b=3)),
                                 LinguisticVariable(LinguisticVariableEnum.MEDIUM, StepMembershipFunction(a=3, b=7)),
                                 LinguisticVariable(LinguisticVariableEnum.HIGH, StepMembershipFunction(a=7, b=10))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.CR.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.ENGAGEMENT_RATE.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.ROAS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.RESULTS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.SPEND.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.REACH.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.LINK_CLICKS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.PAGE_LIKES.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.IMPRESSIONS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.PURCHASES.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.VIDEO_PLAYS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.LEADS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.RSVPS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.APP_INSTALLS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.CONVERSIONS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.THRUPLAYS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.UNIQUE_CLICKS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.POST_LIKES.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.POST_COMMENTS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.POST_SHARES.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.POST_VIEWS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.PURCHASES_VALUE.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=AvailableMetricEnum.CLICKS.value.name,
              linguistic_levels=[
                  LinguisticVariable(LinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(LinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))])
]
