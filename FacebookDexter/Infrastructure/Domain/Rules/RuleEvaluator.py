import typing
from collections import defaultdict

from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata
from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum
from FacebookDexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluatorBuilder import RuleEvaluatorBuilder
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluatorData import RuleEvaluatorData


class RuleEvaluator(RuleEvaluatorBuilder):
    OTHER_METRIC_TYPES = [MetricTypeEnum.AUDIENCE, MetricTypeEnum.CREATIVE,
                          MetricTypeEnum.PIXEL, MetricTypeEnum.INSIGHT_CATEGORICAL,
                          MetricTypeEnum.PROSPECTING, MetricTypeEnum.STRUCTURE,
                          MetricTypeEnum.NUMBER_OF_ADS]

    def evaluate(self, rule, metric_calculator) -> typing.List[typing.List[RuleEvaluatorData]]:
        # evaluate every antecedent for all possible breakdown values
        evaluator_data = {}

        for antecedent in rule.antecedents:
            if antecedent.metric.type == MetricTypeEnum.INSIGHT:
                evaluator_data[antecedent.id] = self.__evaluate_insights_antecedent(antecedent, metric_calculator,
                                                                                    rule)
            elif antecedent.metric.type in self.OTHER_METRIC_TYPES:
                evaluator_data[antecedent.id] = self.__evaluate_antecedent_base(antecedent, metric_calculator,
                                                                                rule)

        # evaluate rule truth value for each combination of breakdown values
        data = self.__evaluate_rule(evaluator_data, rule)
        return data

    def __evaluate_rule(self, evaluator_data: typing.Dict, rule) -> typing.List[typing.List[RuleEvaluatorData]]:
        evaluator_data = self.__split_evaluator_data_by_metric_type(evaluator_data, rule)
        structures_truth_value = self.__evaluate_partial_rule_truth_value(evaluator_data[MetricTypeEnum.STRUCTURE],
                                                                          rule)
        if structures_truth_value:
            rule_data = []
            data = evaluator_data[MetricTypeEnum.STRUCTURE]
            data_groups = self.__group_by_antecedent_breakdowns_values(evaluator_data[MetricTypeEnum.INSIGHT])
            for data_group in data_groups.values():
                insights_rule_truth_value = self.__evaluate_partial_rule_truth_value(data_group, rule)
                current_rule_truth_value = rule.connective.evaluate(structures_truth_value,
                                                                    insights_rule_truth_value)
                if current_rule_truth_value:
                    rule_data.append(data + data_group)
            return rule_data
        return list()

    @staticmethod
    def __split_evaluator_data_by_metric_type(evaluator_data: typing.Dict, rule) -> typing.Dict:
        data = defaultdict(list)
        # todo: remove try execpt
        for key, value in evaluator_data.items():
            #  We need to use key-1 because antecedents is a list, index starts at ZERO and ids start at ONE
            metric_type = rule.antecedents[key - 1].metric.type
            data[metric_type] += value
        return data

    @staticmethod
    def __group_by_antecedent_breakdowns_values(evaluator_data: typing.List[RuleEvaluatorData]) -> typing.Dict:
        data = defaultdict(list)
        for value in evaluator_data:
            data[value.breakdown_metadata.breakdown_value, value.breakdown_metadata.action_breakdown_value] += [value]
        return data

    @staticmethod
    def __evaluate_partial_rule_truth_value(evaluator_data: typing.List[RuleEvaluatorData], rule) -> bool:
        truth_value = True
        for data in evaluator_data:
            truth_value = rule.connective.evaluate(truth_value, data.antecedent_truth_value)
            if not truth_value:
                return truth_value
        return truth_value

    def __evaluate_antecedent_base(self, antecedent, metric_calculator, rule) -> typing.List[RuleEvaluatorData]:
        value, _ = (metric_calculator.set_metric(antecedent.metric).
                    set_time_interval(self._time_interval).
                    compute_value(atype=antecedent.type))
        antecedent_truth_value = antecedent.evaluate(value)
        data = RuleEvaluatorData(antecedent_id=antecedent.id,
                                 antecedent_truth_value=antecedent_truth_value,
                                 metric_value=value,
                                 breakdown_metadata=rule.breakdown_metadata)
        return [data]

    def __evaluate_insights_antecedent(self, antecedent: Antecedent, metric_calculator, rule) -> typing.List[
        RuleEvaluatorData]:
        evaluator_data = []
        breakdown_metadata_list = self.__breakdown_metadata(metric_calculator, rule)
        for breakdown_metadata in breakdown_metadata_list:
            data = self.__evaluate_insights_antecedent_base(antecedent=antecedent,
                                                            breakdown_metadata=breakdown_metadata,
                                                            metric_calculator=metric_calculator)
            evaluator_data.append(data)
        return evaluator_data

    def __evaluate_insights_antecedent_base(self,
                                            antecedent: Antecedent,
                                            breakdown_metadata: BreakdownMetadata,
                                            metric_calculator) -> RuleEvaluatorData:
        value, confidence = (metric_calculator.
                             set_metric(antecedent.metric).
                             set_breakdown_metadata(breakdown_metadata).
                             compute_value(atype=antecedent.type, time_interval=self._time_interval))
        antecedent_truth_value = antecedent.evaluate(value)
        data = RuleEvaluatorData(antecedent_id=antecedent.id,
                                 antecedent_truth_value=antecedent_truth_value,
                                 metric_value=value,
                                 metric_value_confidence=confidence,
                                 breakdown_metadata=breakdown_metadata)
        return data

    def __breakdown_metadata(self, metric_calculator, rule):
        self._breakdown_metadata = metric_calculator.get_breakdown_metadata(
            rule.breakdown_metadata.breakdown,
            rule.breakdown_metadata.action_breakdown,
            self._time_interval)
        return self._breakdown_metadata
