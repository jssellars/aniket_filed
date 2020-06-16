import copy
import typing

from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationBuilder import \
    RuleBasedOptimizationBuilder
from GoogleDexter.Infrastructure.Domain.Actions.ActionDetailsBuilder import ActionEnum
from GoogleDexter.Infrastructure.Domain.Metrics.MetricCalculator import MetricCalculator
from GoogleDexter.Infrastructure.Domain.Recommendations.RecommendationBuilder import RecommendationBuilder
from GoogleDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from GoogleDexter.Infrastructure.Domain.Rules.RuleEvaluatorData import RuleEvaluatorData


class RuleBasedOptimizationBase(RuleBasedOptimizationBuilder):
    def __init__(self):
        super().__init__()

    def run(self, **kwargs) -> typing.List[typing.Dict]:
        raise NotImplementedError("Method run() not implemented.")

    def is_available(self, structure_id: typing.AnyStr):
        return self._mongo_repository.is_available(self._level, structure_id)

    def __evaluate_rules_base(self,
                              structure_id: typing.AnyStr = None,
                              action: ActionEnum = None,
                              fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        applicable_rules = self._rules.get_rules_by_action(action=action,
                                                           level=self._level)

        recommendations = []
        for rule in applicable_rules:
            metric_calculator = (MetricCalculator().
                                 set_business_owner_id(self._business_owner_id).
                                 set_structure_id(structure_id).
                                 set_level(rule.level).
                                 set_repository(self._mongo_repository).
                                 set_business_owner_repo_session(self._business_owner_repo_session).
                                 set_fuzzyfier_factory(fuzzyfier_factory).
                                 set_date_stop(self._date_stop).
                                 set_time_interval(self._time_interval).
                                 set_breakdown_metadata(rule.breakdown_metadata))

            rule_data = (self._rule_evaluator.
                         set_id_and_rule(structure_id=structure_id, rule=rule).
                         set_metric_calculator(metric_calculator).
                         set_time_interval(self._time_interval).
                         evaluate())

            if rule_data:
                try:
                    current_recommendation = self.__create_recommendation(structure_id, rule, rule_data)
                    if current_recommendation.template:
                        recommendations.append(copy.deepcopy(current_recommendation.to_dict()))
                except Exception as e:
                    pass

        return recommendations

    def __create_recommendation(self,
                                structure_id: typing.AnyStr = None,
                                rule: RuleBase = None,
                                rule_data: typing.List[
                                    typing.List[RuleEvaluatorData]] = None) -> RecommendationBuilder:
        recommendation = RecommendationBuilder(mongo_repository=self._mongo_repository,
                                               business_owner_repo_session=self._business_owner_repo_session,
                                               business_owner_id=self._business_owner_id,
                                               date_stop=self._date_stop,
                                               time_interval=self._time_interval)
        return recommendation.create(structure_id, rule, rule_data, external_services=self._external_services)

    def evaluate_remove_rules(self,
                              structure_id: typing.AnyStr = None,
                              fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(structure_id=structure_id, action=ActionEnum.REMOVE,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_create_rules(self,
                              structure_id: typing.AnyStr = None,
                              fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(structure_id=structure_id, action=ActionEnum.CREATE,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_pause_rules(self,
                             structure_id: typing.AnyStr = None,
                             fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(structure_id=structure_id, action=ActionEnum.PAUSE,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_decrease_budget_rules(self,
                                       structure_id: typing.AnyStr = None,
                                       fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(structure_id=structure_id, action=ActionEnum.DECREASE_BUDGET,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_increase_budget_rules(self,
                                       structure_id: typing.AnyStr = None,
                                       fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(structure_id=structure_id, action=ActionEnum.INCREASE_BUDGET,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_general_rules(self,
                               structure_id: typing.AnyStr = None,
                               fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(structure_id=structure_id, action=ActionEnum.GENERAL,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations
