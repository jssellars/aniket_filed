import copy
import typing

from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from Core.Dexter.Infrastructure.Domain.Rules.RuleEvaluatorData import RuleEvaluatorData
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.FacebookRuleBasedOptimizationBuilder import \
    FacebookRuleBasedOptimizationBuilder
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookActionEnum
from FacebookDexter.Infrastructure.Domain.Metrics.FacebookMetricCalculator import FacebookMetricCalculator
from FacebookDexter.Infrastructure.Domain.Recommendations.FacebookRecommendationBuilder import \
    FacebookRecommendationBuilder
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleTypeSelectionEnum


class FacebookRuleBasedOptimizationBase(FacebookRuleBasedOptimizationBuilder):
    def __init__(self):
        super().__init__()

    def rules_selector(self, rule_type: FacebookRuleTypeSelectionEnum = None):
        mapper = {
            FacebookRuleTypeSelectionEnum.REMOVE_BREAKDOWN: [self.evaluate_remove_rules],
            FacebookRuleTypeSelectionEnum.GENERAL: [self.evaluate_general_rules],
            FacebookRuleTypeSelectionEnum.BUDGET: [self.evaluate_increase_budget_rules,
                                                   self.evaluate_decrease_budget_rules],
            FacebookRuleTypeSelectionEnum.PAUSE: [self.evaluate_pause_rules],
            FacebookRuleTypeSelectionEnum.CREATE: [self.evaluate_create_rules]
        }
        return mapper[rule_type]

    def run(self, *args, **kwargs) -> typing.List[typing.Dict]:
        raise NotImplementedError("Method run() not implemented.")

    def check_run_status(self, *args, **kwargs):
        return True

    def is_available(self, facebook_id: typing.AnyStr):
        return self._mongo_repository.is_available(self._level, facebook_id)

    def __evaluate_rules_base(self,
                              facebook_id: typing.AnyStr = None,
                              action: FacebookActionEnum = None,
                              fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:

        applicable_rules = self._rules.get_rules_by_action(action=action,
                                                           level=self._level)
        recommendations = []
        for rule in applicable_rules:
            metric_calculator = (FacebookMetricCalculator().
                                 set_business_owner_id(self._business_owner_id).
                                 set_facebook_id(facebook_id).
                                 set_level(rule.level).
                                 set_business_owner_repo_session(self._business_owner_repo_session).
                                 set_facebook_config(self._facebook_config).
                                 set_fuzzyfier_factory(fuzzyfier_factory).
                                 set_repository(self._mongo_repository).
                                 set_date_stop(self._date_stop).
                                 set_time_interval(self._time_interval).
                                 set_breakdown_metadata(rule.breakdown_metadata).
                                 set_debug_mode(self._debug))

            rule_data = self._rule_evaluator.evaluate(rule=rule, metric_calculator=metric_calculator)

            if rule_data:
                try:
                    current_recommendation = self.__create_recommendation(facebook_id, rule, rule_data)
                    if current_recommendation.template:
                        recommendations.append(copy.deepcopy(current_recommendation.to_dict()))
                except Exception:
                    import traceback
                    traceback.print_exc()

        return recommendations

    def __create_recommendation(self,
                                facebook_id: typing.AnyStr = None,
                                rule: RuleBase = None,
                                rule_data: typing.List[
                                    typing.List[RuleEvaluatorData]] = None) -> FacebookRecommendationBuilder:
        recommendation = FacebookRecommendationBuilder(mongo_repository=self._mongo_repository,
                                                       facebook_config=self._facebook_config,
                                                       business_owner_repo_session=self._business_owner_repo_session,
                                                       business_owner_id=self._business_owner_id,
                                                       date_stop=self._date_stop,
                                                       time_interval=self._time_interval,
                                                       debug_mode=self._debug,
                                                       headers=self._auth_token)
        return recommendation.create(facebook_id, rule, rule_data, external_services=self._external_services)

    def evaluate_remove_rules(self,
                              facebook_id: typing.AnyStr = None,
                              fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=FacebookActionEnum.REMOVE,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_create_rules(self,
                              facebook_id: typing.AnyStr = None,
                              fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=FacebookActionEnum.CREATE,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_pause_rules(self,
                             facebook_id: typing.AnyStr = None,
                             fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=FacebookActionEnum.PAUSE,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_decrease_budget_rules(self,
                                       facebook_id: typing.AnyStr = None,
                                       fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id,
                                                     action=FacebookActionEnum.DECREASE_BUDGET,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_increase_budget_rules(self,
                                       facebook_id: typing.AnyStr = None,
                                       fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id,
                                                     action=FacebookActionEnum.INCREASE_BUDGET,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_general_rules(self,
                               facebook_id: typing.AnyStr = None,
                               fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=FacebookActionEnum.GENERAL,
                                                     fuzzyfier_factory=fuzzyfier_factory)
        return recommendations
