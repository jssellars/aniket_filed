import typing
from collections import defaultdict

from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from Core.Dexter.Infrastructure.Domain.Rules.RuleEvaluatorBuilder import RuleEvaluatorBuilder
from Core.Dexter.Infrastructure.Domain.Rules.RuleEvaluatorData import RuleEvaluatorData


class RuleEvaluatorBase(RuleEvaluatorBuilder):

    def __init__(self):
        super().__init__()

    def evaluate(self, rule, metric_calculator, antecedent_cache=None, metric_cache=None) -> typing.List[typing.List[RuleEvaluatorData]]:
        raise NotImplementedError

    def _evaluate_rule(self, evaluator_data: typing.Dict, rule) -> typing.List[typing.List[RuleEvaluatorData]]:
        raise NotImplementedError

    @staticmethod
    def _split_evaluator_data_by_metric_type(evaluator_data: typing.Dict, rule) -> typing.Dict:
        data = defaultdict(list)
        for key, value in evaluator_data.items():
            #  We need to use key-1 because antecedents is a list, index starts at ZERO and ids start at ONE
            metric_type = rule.antecedents[key - 1].metric.type
            data[metric_type] += value
        return data

    @staticmethod
    def _group_by_antecedent_breakdowns_values(evaluator_data: typing.List[RuleEvaluatorData]) -> typing.Dict:
        data = defaultdict(list)
        for value in evaluator_data:
            data[value.breakdown_metadata.breakdown_value, value.breakdown_metadata.action_breakdown_value] += [value]
        return data

    @staticmethod
    def _evaluate_partial_rule_truth_value(evaluator_data: typing.List[RuleEvaluatorData], rule) -> bool:
        truth_value = True
        for data in evaluator_data:
            truth_value = rule.connective.evaluate(truth_value, data.antecedent_truth_value)
            if not truth_value:
                return truth_value
        return truth_value

    def _evaluate_antecedent_base(self,
                                  antecedent,
                                  metric_calculator,
                                  rule,
                                  metric_cache=None) -> typing.List[RuleEvaluatorData]:
        value, _ = (metric_calculator.set_metric(antecedent.metric).
                    set_time_interval(self._time_interval).
                    compute_value(atype=antecedent.type, metric_cache=metric_cache))
        antecedent_truth_value = antecedent.evaluate(value)
        data = RuleEvaluatorData(antecedent_id=antecedent.id,
                                 antecedent_truth_value=antecedent_truth_value,
                                 metric_value=value,
                                 breakdown_metadata=rule.breakdown_metadata)
        return [data]

    def _evaluate_insights_antecedent(self,
                                      antecedent: Antecedent,
                                      metric_calculator,
                                      rule,
                                      metric_cache: typing.Dict = None) -> typing.List[RuleEvaluatorData]:
        evaluator_data = []
        breakdown_metadata_list = self._breakdown_metadata_(metric_calculator, rule)
        for breakdown_metadata in breakdown_metadata_list:
            data = self._evaluate_insights_antecedent_base(
                antecedent=antecedent,
                breakdown_metadata=breakdown_metadata,
                metric_calculator=metric_calculator,
                metric_cache=metric_cache
            )
            evaluator_data.append(data)
        return evaluator_data

    def _evaluate_insights_antecedent_base(self,
                                           antecedent: Antecedent,
                                           breakdown_metadata: BreakdownMetadataBase,
                                           metric_calculator,
                                           metric_cache: typing.Dict = None) -> RuleEvaluatorData:
        value, confidence = (
            metric_calculator.set_metric(antecedent.metric)
            .set_breakdown_metadata(breakdown_metadata)
            .compute_value(
                atype=antecedent.type,
                time_interval=self._time_interval,
                metric_cache=metric_cache
            )
        )
        antecedent_truth_value = antecedent.evaluate(value)
        data = RuleEvaluatorData(antecedent_id=antecedent.id,
                                 antecedent_truth_value=antecedent_truth_value,
                                 metric_value=value,
                                 metric_value_confidence=confidence,
                                 breakdown_metadata=breakdown_metadata)
        return data

    def _breakdown_metadata_(self, metric_calculator, rule):
        self._breakdown_metadata = metric_calculator.get_breakdown_metadata(
            rule.breakdown_metadata.breakdown,
            rule.breakdown_metadata.action_breakdown,
            self._time_interval)
        return self._breakdown_metadata
