import typing
from collections import defaultdict

from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum
from FacebookDexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluatorBuilder import RuleEvaluatorBuilder
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluatorData import RuleEvaluatorData


class RuleEvaluator(RuleEvaluatorBuilder):

    @property
    def _breakdown_metadata(self, time_interval: DaysEnum = None):
        if not self.__breakdown_metadata:
            self.__breakdown_metadata = self.__metric_calculator.get_breakdown_metadata(time_interval)
        return self._breakdown_metadata

    def evaluate(self) -> typing.List[typing.List[RuleEvaluatorData]]:
        # evaluate every antecedent for all possible breakdown values
        evaluator_data = {}
        for antecedent in self.__rule.antecedents:
            if antecedent.metric.type == MetricTypeEnum.STRUCTURE:
                evaluator_data[antecedent.id] = self.__evaluate_structure_antecedent(antecedent)
            elif antecedent.metric.type == MetricTypeEnum.INSIGHT:
                evaluator_data[antecedent.id] = self.__evaluate_insights_antecedent(antecedent)

        # evaluate rule truth value for each combination of breakdown values
        data = self.__evaluate_rule(evaluator_data)

        return data

    def __evaluate_rule(self, evaluator_data: typing.Dict[int]) -> typing.List[typing.List[RuleEvaluatorData]]:
        evaluator_data = self.__split_evaluator_data_by_metric_type(evaluator_data)
        structures_truth_value = self.__evaluate_partial_rule_truth_value(evaluator_data[MetricTypeEnum.STRUCTURE])

        if structures_truth_value:
            rule_data = []
            data = evaluator_data[MetricTypeEnum.STRUCTURE]
            data_groups = self.__group_by_antecedent_id_and_breakdown_metadata(evaluator_data[MetricTypeEnum.INSIGHT])
            for data_group in data_groups.values():
                insights_rule_truth_value = self.__evaluate_partial_rule_truth_value(data_group)
                current_rule_truth_value = self.__rule.connective(structures_truth_value, insights_rule_truth_value)
                if current_rule_truth_value:
                    rule_data.append(data+data_group)
            return rule_data
        return list()

    def __split_evaluator_data_by_metric_type(self, evaluator_data: typing.Dict[int] = None) -> typing.Dict[MetricTypeEnum]:
        data = defaultdict(default_factory=list)
        for key, value in evaluator_data.items():
            metric_type = self.__rule.antecedents[key].metric.type
            data[metric_type] += value
        return data

    @staticmethod
    def __group_by_antecedent_id_and_breakdown_metadata(evaluator_data: typing.List[RuleEvaluatorData]) -> typing.Dict:
        data = defaultdict(default_factory=list)
        for value in evaluator_data:
            data[value.antecedent_id, value.breakdown_metadata.breakdown_value, value.breakdown_metadata.action_breakdown_value] += value
        return data

    def __evaluate_partial_rule_truth_value(self, evaluator_data: typing.List[RuleEvaluatorData]) -> bool:
        truth_value = True
        for data in evaluator_data:
            truth_value = self.__rule.connective(truth_value, data.antecedent_truth_value)
            if not truth_value:
                return truth_value

        return truth_value

    def __evaluate_structure_antecedent(self, antecedent: Antecedent = None) -> RuleEvaluatorData:
        value, _ = self.__metric_calculator.set_metric(antecedent.metric).compute_value(atype=antecedent.type)
        antecedent_truth_value = antecedent.evaluate(value)
        data = RuleEvaluatorData(antecedent_id=antecedent.id,
                                 antecedent_truth_value=antecedent_truth_value,
                                 metric_value=value,
                                 breakdown_metadata=self.__rule.breakdown_metadata)
        return data

    def __evaluate_insights_antecedent(self, antecedent: Antecedent = None) -> typing.List[RuleEvaluatorData]:
        evaluator_data = []

        for breakdown_metadata in self._breakdown_metadata:
            value, confidence = self.__metric_calculator.\
                set_metric(antecedent.metric).\
                set_breakdown_metadata(breakdown_metadata).\
                compute_value(atype=antecedent.type, time_interval=self.__rule.time_interval)
            antecedent_truth_value = antecedent.evaluate(value)
            data = RuleEvaluatorData(antecedent_id=antecedent.id,
                                     antecedent_truth_value=antecedent_truth_value,
                                     metric_value=value,
                                     metric_value_confidence=confidence,
                                     breakdown_metadata=breakdown_metadata)
            evaluator_data.append(data)

        return evaluator_data
