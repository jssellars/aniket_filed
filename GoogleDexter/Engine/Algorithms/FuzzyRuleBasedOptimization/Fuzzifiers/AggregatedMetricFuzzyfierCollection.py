from Core.Dexter.Infrastructure.Domain.FuzzyEngine.FuzzySets.FuzzyMembershipFunction import LinearMembershipFunction, \
    TrapezeMembershipFunction, StepMembershipFunction
from Core.Dexter.Infrastructure.Domain.FuzzyEngine.FuzzySets.FuzzySets import Fuzzyfier, LinguisticVariable
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.GoogleAvailableMetricEnum import \
    GoogleAvailableMetricEnum
from GoogleDexter.Infrastructure.FuzzyEngine.GoogleFuzzySets import GoogleLinguisticVariableEnum

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
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.CPC.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.CPM.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.CTR.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.COST_PER_RESULT.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.COST_PER_APP_INSTALL.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.COST_PER_CONVERSION.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.COST_PER_THRUPLAY.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.FREQUENCY.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, StepMembershipFunction(a=0, b=3)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, StepMembershipFunction(a=3, b=7)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, StepMembershipFunction(a=7, b=10))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.CR.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.ENGAGEMENT_RATE.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.ROAS.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.RESULTS.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.SPEND.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.REACH.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.LINK_CLICKS.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.PAGE_LIKES.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.IMPRESSIONS.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.PURCHASES.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.VIDEO_PLAYS.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.LEADS.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.RSVPS.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.APP_INSTALLS.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.CONVERSIONS.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.THRUPLAYS.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # # Fuzzyfier(metric_name=AvailableMetricEnum.UNIQUE_CLICKS.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # # Fuzzyfier(metric_name=AvailableMetricEnum.POST_LIKES.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.POST_COMMENTS.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.POST_SHARES.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    # Fuzzyfier(metric_name=AvailableMetricEnum.POST_VIEWS.value.name,
    #           linguistic_levels=[
    #               LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM, TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
    #               LinguisticVariable(GoogleLinguisticVariableEnum.HIGH, LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.PURCHASES_VALUE.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))]),
    Fuzzyfier(metric_name=GoogleAvailableMetricEnum.CLICKS.value.name,
              linguistic_levels=[
                  LinguisticVariable(GoogleLinguisticVariableEnum.LOW, LinearMembershipFunction(**LOW_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.MEDIUM,
                                     TrapezeMembershipFunction(**MEDIUM_LINEAR_PARAMS)),
                  LinguisticVariable(GoogleLinguisticVariableEnum.HIGH,
                                     LinearMembershipFunction(**HIGH_LINEAR_PARAMS))])
]
