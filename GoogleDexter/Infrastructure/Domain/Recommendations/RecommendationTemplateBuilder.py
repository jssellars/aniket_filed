import re
import traceback
import typing
from collections import defaultdict

import requests

from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.logging_legacy import log_message_as_dict
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.GoogleAvailableMetricEnum import \
    GoogleAvailableMetricEnum
from GoogleDexter.Infrastructure.Domain.Breakdowns import GoogleBreakdownEnum, GoogleActionBreakdownEnum
from GoogleDexter.Infrastructure.Domain.GoogleRuleTemplateKeyword import GoogleRuleTemplateKeyword
from GoogleDexter.Infrastructure.Domain.Metrics.GoogleMetricCalculator import GoogleMetricCalculator
from GoogleDexter.Infrastructure.Domain.Metrics.GoogleMetricEnums import GoogleMetricTypeEnum
from GoogleDexter.Infrastructure.Domain.Recommendations.RecommendationTemplateBuilderBase import \
    RecommendationTemplateBuilderBase
from GoogleDexter.Infrastructure.FuzzyEngine.GoogleFuzzySets import GoogleLinguisticVariableEnum


import logging

logger_native = logging.getLogger(__name__)


class RecommendationTemplateBuilder(RecommendationTemplateBuilderBase):
    __keywords_map = {
        "time_interval": DaysEnum,
        "metric_name": GoogleAvailableMetricEnum.get_enum_by_name,
        "metric_type": GoogleMetricTypeEnum,
        "antecedent_type": AntecedentTypeEnum,
        "linguistic_variable": GoogleLinguisticVariableEnum,
        "id": lambda x: int(x),
        "metric_count": lambda x: int(x),
        "value": lambda x: None,
        "breakdown_values": lambda x: None
    }

    def __init__(self, breakdown_values: typing.List[typing.AnyStr] = None):
        super().__init__()
        self.__breakdown_values = breakdown_values

    @property
    def __keyword_value_map(self):
        return {
            'metric_name': lambda x: x.metric_name.value.display_name,
            'value': lambda x: x.value,
            'time_interval': lambda x: str(self._time_interval.value),
            'linguistic_variable': lambda x: GoogleLinguisticVariableEnum(x).name,
            'breakdown_values': lambda x: x.breakdown_values
        }

    def build_template(self, template: typing.AnyStr = None) -> typing.Union[typing.AnyStr, typing.NoReturn]:
        try:
            keywords = self.__build_rule_keyword_templates(template)
            if not keywords:
                return template

            keywords_values = [self.__find_keywords_values(keyword) for keyword in keywords]

            for keyword in self._keywords:
                keyword_id = int(keyword.split("&")[0].split("=")[1])
                keyword_values = [x for x in keywords_values if x.id == keyword_id][0]
                value = self.__get_value_for_keyword(keyword, keyword_values)
                if not value or value == '0.0':
                    return None
                template = template.replace("<" + keyword + ">", value)
        except Exception as e:
            self.logger.logger.info(log_message_as_dict(mtype=logging.ERROR,
                                      name="RecommendationTemplateBuilder",
                                      description=f"Failed to compute keyword value for template {template}",
                                      extra_data={
                                        "error": traceback.format_exc()
                                    }))
            raise e
        return template

    def __build_rule_keyword_templates(self, template: typing.AnyStr = None) -> typing.List[GoogleRuleTemplateKeyword]:
        self._keywords = re.findall('<(.+?)>', template)

        if not self._keywords:
            return []

        keyword_dict = defaultdict()

        for keyword in self._keywords:
            keyword_id = self.__find_keyword_id(keyword)
            keyword_dict.setdefault(keyword_id, GoogleRuleTemplateKeyword())
            keyword_dict[keyword_id] = self.__build_rule_template_keyword(keyword_dict[keyword_id], keyword)

        return list(keyword_dict.values())

    def __find_keywords_values(self, keyword: GoogleRuleTemplateKeyword):
        value = ''
        if keyword.metric_name:
            try:
                if keyword.metric_type == GoogleMetricTypeEnum.INSIGHT:
                    value = self.__find_insight_value(keyword)
                elif keyword.metric_type == GoogleMetricTypeEnum.INTERESTS:
                    value = self.__find_suggested_interests(keyword)
                elif keyword.metric_type == GoogleMetricTypeEnum.AUDIENCE:
                    value = self.__find_audience_size(keyword)
                else:
                    value = ''
                    self.logger.logger.info(log_message_as_dict(mtype=logging.WARNING,
                                              name="RecommendationTemplateBuilder",
                                              description=f"Failed to compute keyword value for metric {keyword.metric_name.value.name}"))

            except Exception as e:
                self.logger.logger.info(log_message_as_dict(mtype=logging.ERROR,
                                          name="RecommendationTemplateBuilder",
                                          description=f"Failed to compute keyword value for metric {keyword.metric_name.value.name}",
                                          extra_data={
                                            "error": traceback.format_exc()
                                        }))
                raise e

        keyword.value = str(value) if value is not None else ''

        return keyword

    def __in_order_traversal(self, node, accumulator):
        if 'children' in node:
            for children in node['children']:
                self.__in_order_traversal(children, accumulator)
        else:
            accumulator.append((node['name'], node['audience_size']))

    @staticmethod
    def __find_keyword_id(keyword):
        keyword_id = re.findall('id=.', keyword)
        if len(keyword_id) > 1:
            raise ValueError('You cannot have more than one id per entry')
        keyword_id = int(keyword_id[0].split('=')[1])
        return keyword_id

    def __build_rule_template_keyword(self,
                                      rule_template_keyword: GoogleRuleTemplateKeyword = None,
                                      keyword: typing.AnyStr = None) -> GoogleRuleTemplateKeyword:
        keywords_list = keyword.split('&')

        for entry in keywords_list:
            entry_name, entry_value = entry.split("=")
            entry_value = int(entry_value) if entry_value.isdigit() else entry_value
            setattr(rule_template_keyword, entry_name, self.__keywords_map[entry_name](entry_value))

        rule_template_keyword.breakdown_values = ", ".join(
            sorted(self.__breakdown_values)) if self.__breakdown_values else ''

        return rule_template_keyword

    def __get_value_for_keyword(self, keyword: typing.AnyStr = None,
                                keywords_values: GoogleRuleTemplateKeyword = None):
        key, value = keyword.split('&')[1].split('=')
        return self.__keyword_value_map[key](keywords_values)

    @staticmethod
    def __is_interest(entry):
        interest_keys = ['interests', 'behaviors', 'life_events', 'industries', 'income', 'family_statuses',
                         'education_schools',
                         'work_employers', 'education_majors', 'work_positions']

        if not isinstance(entry, dict):
            return False

        for key in entry.keys():
            if key not in interest_keys:
                return False

        return True

    def __find_insight_value(self, keyword: GoogleRuleTemplateKeyword = None):
        mc = GoogleMetricCalculator()
        mc = (mc.
              set_structure_id(self._structure_id).
              set_level(self._level).
              set_metric(keyword.metric_name.value).
              set_repository(self._repository).
              set_date_stop(self._date_stop).
              set_time_interval(keyword.time_interval).
              set_breakdown_metadata(BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
                                                           action_breakdown=GoogleActionBreakdownEnum.NONE)))
        value, _ = mc.compute_value(atype=keyword.antecedent_type, time_interval=keyword.time_interval)

        if value:
            value = abs(int(value))

        return value

    def __find_suggested_interests(self, keyword: GoogleRuleTemplateKeyword):
        structure = self._repository.get_structure_details(self._structure_id, LevelEnum.ADGROUP)

        try:
            if 'flexible_spec' in structure['targeting'].keys():
                interests = [interest_dict['name']
                             for entry in structure['targeting']['flexible_spec']
                             for interest_lists in entry.values()
                             for interest_dict in interest_lists
                             if self.__is_interest(entry)]
                if not interests:
                    return ''
            else:
                return ''
        except Exception as e:
            self.logger.logger.info(log_message_as_dict(mtype=logging.ERROR,
                                      name="RecommendationTemplateBuilder",
                                      description="Failed to get interests from structure targeting.",
                                      extra_data={
                                        "error": traceback.format_exc()
                                    }))
            raise e

        self._external_services.targeting_search += ','.join(interests)

        response = requests.get(url=self._external_services.targeting_search)
        if response.status_code != 200:
            self.logger.logger.info(log_message_as_dict(mtype=logging.ERROR,
                                      name="RecommendationTemplateBuilder",
                                      description="Failed to get interests from structure targeting.",
                                      extra_data={
                                        "error": response.json()
                                    }))
            return ''

        response = response.json()
        results_root = response['results']
        interests_accumulator = []
        for response in results_root:
            self.__in_order_traversal(node=response, accumulator=interests_accumulator)

        top_interests = list(
            list(sorted(interests_accumulator, key=lambda x: x[1] if x[1] is not None else 0, reverse=True))[
            :keyword.metric_count])
        top_interests = list(map(lambda x: x[0], top_interests))

        value = ', '.join(top_interests)

        return value

    def __find_audience_size(self, keyword: GoogleRuleTemplateKeyword):
        mc = GoogleMetricCalculator()
        mc = (mc.
              set_structure_id(self._structure_id).
              set_level(self._level).
              set_metric(keyword.metric_name.value).
              set_repository(self._repository).
              set_business_owner_repo_session(self._business_owner_repo_session).
              set_business_owner_id(self._business_owner_id).
              set_date_stop(self._date_stop).
              set_breakdown_metadata(BreakdownMetadataBase(breakdown=GoogleBreakdownEnum.NONE,
                                                           action_breakdown=GoogleActionBreakdownEnum.NONE)))
        value, _ = mc.compute_value(atype=keyword.antecedent_type)

        return int(value)
