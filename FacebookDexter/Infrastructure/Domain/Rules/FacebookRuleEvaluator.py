import typing

from Core.Dexter.Infrastructure.Domain.Rules.RuleEvaluatorBase import RuleEvaluatorBase
from Core.Dexter.Infrastructure.Domain.Rules.RuleEvaluatorData import RuleEvaluatorData
from FacebookDexter.Infrastructure.Domain.Metrics.FacebookMetricEnums import FacebookMetricTypeEnum
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum


class FacebookRuleEvaluator(RuleEvaluatorBase):
    OTHER_METRIC_TYPES = [FacebookMetricTypeEnum.AUDIENCE, FacebookMetricTypeEnum.CREATIVE,
                          FacebookMetricTypeEnum.PIXEL, FacebookMetricTypeEnum.INSIGHT_CATEGORICAL,
                          FacebookMetricTypeEnum.PROSPECTING, FacebookMetricTypeEnum.STRUCTURE,
                          FacebookMetricTypeEnum.NUMBER_OF_ADS]

    def __init__(self):
        super().__init__()

    def evaluate(self, rule, metric_calculator, antecedent_cache=None) -> typing.List[typing.List[RuleEvaluatorData]]:
        # evaluate every antecedent for all possible breakdown values
        evaluator_data = {}
        for antecedent in rule.antecedents:

            antecedent_string_key = ""
            if antecedent.type == AntecedentTypeEnum.FUZZY_TREND:
                antecedent_string_key = str(antecedent.metric.name) + "_" + str(antecedent.operator.name) + "_" + str(antecedent.expected_value.name)

            if (metric_calculator.get_facebook_id(), antecedent_string_key) in antecedent_cache:
                evaluator_data[antecedent.id] = antecedent_cache[(metric_calculator.get_facebook_id(), antecedent_string_key)]

            else:
                if antecedent.metric.type == FacebookMetricTypeEnum.INSIGHT:
                    evaluator_data[antecedent.id] = self._evaluate_insights_antecedent(antecedent, metric_calculator, rule)
                elif antecedent.metric.type in self.OTHER_METRIC_TYPES:
                    evaluator_data[antecedent.id] = self._evaluate_antecedent_base(antecedent, metric_calculator, rule)

                if antecedent.type == AntecedentTypeEnum.FUZZY_TREND:
                    antecedent_cache[(metric_calculator.get_facebook_id(), antecedent_string_key)] = evaluator_data[antecedent.id]
        # evaluate rule truth value for each combination of breakdown values
        data = self._evaluate_rule(evaluator_data, rule)
        return data

    def _evaluate_rule(self, evaluator_data: typing.Dict, rule) -> typing.List[typing.List[RuleEvaluatorData]]:
        evaluator_data = self._split_evaluator_data_by_metric_type(evaluator_data, rule)
        structures_truth_value = self._evaluate_partial_rule_truth_value(
            evaluator_data[FacebookMetricTypeEnum.STRUCTURE],
            rule)
        if structures_truth_value:
            rule_data = []
            data = evaluator_data[FacebookMetricTypeEnum.STRUCTURE]
            data_groups = self._group_by_antecedent_breakdowns_values(evaluator_data[FacebookMetricTypeEnum.INSIGHT])
            for data_group in data_groups.values():
                insights_rule_truth_value = self._evaluate_partial_rule_truth_value(data_group, rule)
                current_rule_truth_value = rule.connective.evaluate(structures_truth_value,
                                                                    insights_rule_truth_value)
                if current_rule_truth_value:
                    rule_data.append(data + data_group)
            return rule_data
        return list()
