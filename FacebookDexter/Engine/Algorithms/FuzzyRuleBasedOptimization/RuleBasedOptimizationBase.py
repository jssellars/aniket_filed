import copy
import typing

from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationBuilder import \
    RuleBasedOptimizationBuilder
from FacebookDexter.Infrastructure.Domain.Actions.ActionDetailsBuilder import ActionEnum
from FacebookDexter.Infrastructure.Domain.Metrics.MetricCalculator import MetricCalculator
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationBuilder import RecommendationBuilder
from FacebookDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluatorData import RuleEvaluatorData


class RuleBasedOptimizationBase(RuleBasedOptimizationBuilder):
    def __init__(self):
        super().__init__()

    def run(self, **kwargs) -> typing.List[typing.Dict]:
        raise NotImplementedError("Method run() not implemented.")

    def __evaluate_rules_base(self,
                              facebook_id: typing.AnyStr = None,
                              action: ActionEnum = None,
                              fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        applicable_rules = self._rules.get_rules_by_action(action=action,
                                                           level=self._level)

        recommendations = []
        for rule in applicable_rules:
            metric_calculator = (MetricCalculator().
                                 set_business_owner_id(self._business_owner_id).
                                 set_facebook_id(facebook_id).
                                 set_level(rule.level).
                                 set_repository(self._mongo_repository).
                                 set_business_owner_repo_session(self._business_owner_repo_session).
                                 set_facebook_config(self._facebook_config).
                                 set_fuzzyfier_factory(fuzzyfier_factory).
                                 set_breakdown_metadata(rule.breakdown_metadata))

            rule_data = (self._rule_evaluator.
                         set_id_and_rule(facebook_id=facebook_id, rule=rule).
                         set_metric_calculator(metric_calculator).
                         evaluate())

            if rule_data:
                try:
                    current_recommendation = self.__create_recommendation(facebook_id, rule, rule_data)
                    recommendations.append(copy.deepcopy(current_recommendation))
                except Exception as e:
                    pass

        return recommendations

    def __create_recommendation(self,
                                facebook_id: typing.AnyStr = None,
                                rule: RuleBase = None,
                                rule_data: typing.List[typing.List[RuleEvaluatorData]] = None) -> typing.Dict:
        recommendation = RecommendationBuilder(mongo_repository=self._mongo_repository,
                                               facebook_config=self._facebook_config,
                                               business_owner_repo_session=self._business_owner_repo_session,
                                               business_owner_id=self._business_owner_id)
        return recommendation.create(facebook_id, rule, rule_data, external_services=self._external_services).to_dict()

    def evaluate_remove_rules(self, facebook_id: typing.AnyStr = None, fuzzyfier_factory: typing.Any = None) -> \
            typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.REMOVE,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_create_rules(self, facebook_id: typing.AnyStr = None, fuzzyfier_factory: typing.Any = None) -> \
            typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.CREATE,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_pause_rules(self, facebook_id: typing.AnyStr = None, fuzzyfier_factory: typing.Any = None) -> \
            typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.PAUSE,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_decrease_budget_rules(self, facebook_id: typing.AnyStr = None,
                                       fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.DECREASE_BUDGET,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_increase_budget_rules(self, facebook_id: typing.AnyStr = None,
                                       fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.INCREASE_BUDGET,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_general_rules(self, facebook_id: typing.AnyStr = None, fuzzyfier_factory: typing.Any = None) -> \
            typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.GENERAL,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations
