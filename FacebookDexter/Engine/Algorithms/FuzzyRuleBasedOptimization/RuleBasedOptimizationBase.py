import abc
import copy
import typing

from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Rules import Rules
from FacebookDexter.Infrastructure.Domain.Actions.ActionDetailsBuilder import ActionEnum
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationBuilder import RecommendationBuilder
from FacebookDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluator import RuleEvaluator
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluatorData import RuleEvaluatorData
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository


class RuleBasedOptimizationBase(metaclass=abc.ABCMeta):
    def __init__(self,
                 rules: Rules = None,
                 mongo_repository: DexterMongoRepository = None):
        self._mongo_repository = mongo_repository
        self._rules = rules
        self._rule_evaluator = RuleEvaluator()

    @abc.abstractmethod
    def run(self, **kwargs) -> typing.List[typing.Dict]:
        pass

    def __evaluate_rules_base(self,
                              facebook_id: typing.AnyStr = None,
                              action: ActionEnum = None,
                              fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        self._rule_evaluator = self._rule_evaluator.\
            set_fuzzyfier_factory(fuzzyfier_factory).\
            set_metric_calculator_repository(self._mongo_repository)

        applicable_rules = self._rules.get_rules_by_action(action=action)

        recommendations = []
        for rule in applicable_rules:
            rule_data = self._rule_evaluator.set_id_and_rule(facebook_id=facebook_id, rule=rule).evaluate()
            current_recommendations = [self.__create_recommendation(facebook_id, rule, data) for data in rule_data]
            recommendations += copy.deepcopy(current_recommendations)
        return recommendations

    def __create_recommendation(self,
                                facebook_id: typing.AnyStr = None,
                                rule: RuleBase = None,
                                rule_data: RuleEvaluatorData = None) -> typing.Dict:
        recommendation = RecommendationBuilder(self._mongo_repository)
        return recommendation.create(facebook_id, rule, rule_data).to_dict()

    def evaluate_remove_rules(self, facebook_id: typing.AnyStr = None, fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.REMOVE, fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_create_rules(self, facebook_id: typing.AnyStr = None, fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.CREATE, fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_pause_rules(self, facebook_id: typing.AnyStr = None, fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.PAUSE, fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_decrease_budget_rules(self, facebook_id: typing.AnyStr = None, fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.DECREASE_BUDGET, fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_increase_budget_rules(self, facebook_id: typing.AnyStr = None, fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.INCREASE_BUDGET, fuzzyfier_factory=fuzzyfier_factory)
        return recommendations

    def evaluate_general_rules(self, facebook_id: typing.AnyStr = None, fuzzyfier_factory: typing.Any = None) -> typing.List[typing.Dict]:
        recommendations = self.__evaluate_rules_base(facebook_id=facebook_id, action=ActionEnum.GENERAL, fuzzyfier_factory=fuzzyfier_factory)
        return recommendations


