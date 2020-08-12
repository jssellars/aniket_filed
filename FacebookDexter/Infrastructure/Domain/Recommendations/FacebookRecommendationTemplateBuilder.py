import itertools
import re
import traceback
import typing
from collections import defaultdict

import requests

from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.FacebookAvailableMetricEnum import \
    FacebookAvailableMetricEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import FacebookBreakdownEnum, FacebookActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.FuzzyEngine.FacebookFuzzySets import FacebookLinguisticVariableEnum
from FacebookDexter.Infrastructure.Domain.Metrics.FacebookMetricCalculator import FacebookMetricCalculator
from FacebookDexter.Infrastructure.Domain.Metrics.FacebookMetricEnums import FacebookMetricTypeEnum
from FacebookDexter.Infrastructure.Domain.Recommendations.FacebookRecommendationTemplateBuilderBase import \
    FacebookRecommendationTemplateBuilderBase
from FacebookDexter.Infrastructure.Domain.RuleTemplateKeyword import RuleTemplateKeyword


class FacebookRecommendationTemplateBuilder(FacebookRecommendationTemplateBuilderBase):

    __keywords_map = {
        "time_interval": DaysEnum,
        "metric_name": FacebookAvailableMetricEnum.get_enum_by_name,
        "metric_type": FacebookMetricTypeEnum,
        "antecedent_type": AntecedentTypeEnum,
        "linguistic_variable": FacebookLinguisticVariableEnum,
        "id": lambda x: int(x),
        "metric_count": lambda x: int(x),
        "value": lambda x: None,
        "breakdown_values": lambda x: None,
        "display_metric_name": lambda x: int(x)
    }

    def __init__(self, breakdown_values: typing.List[typing.AnyStr] = None):
        super().__init__()
        self.__breakdown_values = breakdown_values

    @property
    def __keyword_value_map(self):
        return {
            'metric_name': lambda x: x.metric_name.value.display_name if x.display_metric_name else '',
            'value': lambda x: x.value if x.value else None,
            'time_interval': lambda x: str(self._time_interval.value),
            'linguistic_variable': lambda x: FacebookLinguisticVariableEnum(x).name,
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
                if value is None:
                    return value
                template = template.replace("__" + keyword + "__", value)
        except Exception as e:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="RecommendationTemplateBuilder",
                                        description=f"Failed to compute keyword value for template {template}",
                                        extra_data={
                                            "error": traceback.format_exc()
                                        })
                self.logger.logger.info(log)
            raise e
        return template

    def __build_rule_keyword_templates(self, template: typing.AnyStr = None) -> typing.List[RuleTemplateKeyword]:
        self._keywords = re.findall('__(.+?)__', template)

        if not self._keywords:
            return []

        keyword_dict = defaultdict()

        for keyword in self._keywords:
            keyword_id = self.__find_keyword_id(keyword)
            keyword_dict.setdefault(keyword_id, RuleTemplateKeyword())
            keyword_dict[keyword_id] = self.__build_rule_template_keyword(keyword_dict[keyword_id], keyword)

        return list(keyword_dict.values())

    def __find_keywords_values(self, keyword: RuleTemplateKeyword):
        value = ''
        if keyword.metric_name:
            try:
                if keyword.metric_type == FacebookMetricTypeEnum.INSIGHT:
                    value = self.__find_insight_value(keyword)
                elif keyword.metric_type == FacebookMetricTypeEnum.INTERESTS:
                    value = self.__find_suggested_interests(keyword)
                elif keyword.metric_type == FacebookMetricTypeEnum.AUDIENCE:
                    value = self.__find_audience_size(keyword)
                elif keyword.metric_type == FacebookMetricTypeEnum.DUPLICATE_AD:
                    value = self.__find_best_performing_ad_name(keyword)
                else:
                    value = ''
                    if self._debug:
                        log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                                name="RecommendationTemplateBuilder",
                                                description=f"Failed to compute keyword value for "
                                                            f"metric {keyword.metric_name.value.name}")
                        self.logger.logger.info(log)
            except Exception as e:
                if self._debug:
                    log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                            name="RecommendationTemplateBuilder",
                                            description=f"Failed to compute keyword value for "
                                                        f"metric {keyword.metric_name.value.name}",
                                            extra_data={
                                                "error": traceback.format_exc()
                                            })
                    self.logger.logger.info(log)
                raise e

        keyword.value = str(value) if value else ''

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
                                      rule_template_keyword: RuleTemplateKeyword = None,
                                      keyword: typing.AnyStr = None) -> RuleTemplateKeyword:
        keywords_list = keyword.split('&')

        for entry in keywords_list:
            entry_name, entry_value = entry.split("=")
            entry_value = int(entry_value) if entry_value.isdigit() else entry_value
            setattr(rule_template_keyword, entry_name, self.__keywords_map[entry_name](entry_value))

        rule_template_keyword.breakdown_values = ", ".join(
            sorted(self.__breakdown_values)) if self.__breakdown_values else ''

        return rule_template_keyword

    def __get_value_for_keyword(self, keyword: typing.AnyStr = None, keywords_values: RuleTemplateKeyword = None):
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

    def __find_insight_value(self, keyword: RuleTemplateKeyword = None):
        mc = (FacebookMetricCalculator().
            set_facebook_id(self._structure_id).
            set_level(self._level).
            set_metric(keyword.metric_name.value).
            set_repository(self._repository).
            set_date_stop(self._date_stop).
            set_time_interval(self._time_interval).
            set_debug_mode(self._debug).
            set_breakdown_metadata(
            BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                  action_breakdown=FacebookActionBreakdownEnum.NONE)))
        value, _ = mc.compute_value(atype=keyword.antecedent_type, time_interval=self._time_interval)

        if value is not None:
            value = abs(float("{:.2f}".format(value)))

        return value

    def _get_top_interests(self, top_number, endpoint, headers):
        response = requests.get(url=endpoint, headers=headers)
        if response.status_code != 200:
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="RecommendationTemplateBuilder",
                                        description="Failed to get interests from structure targeting.",
                                        extra_data={
                                            "error": response.json()
                                        })
                self.logger.logger.info(log)
            return ''

        results_root = response.json()
        interests_accumulator = []
        for response in results_root:
            self.__in_order_traversal(node=response, accumulator=interests_accumulator)

        # todo: check if this needs list(list(something))
        top_interests = list(
            list(sorted(interests_accumulator, key=lambda x: x[1] if x[1] is not None else 0, reverse=True)))

        top_interests = list(map(lambda x: x[0], top_interests))
        value = ', '.join(top_interests)[:top_number]

        return value

    def __find_suggested_interests(self, keyword: RuleTemplateKeyword):
        structure = self._repository.get_structure_details(self._structure_id, LevelEnum.ADSET)

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
            if self._debug:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.ERROR,
                                        name="RecommendationTemplateBuilder",
                                        description="Failed to get interests from structure targeting.",
                                        extra_data={
                                            "error": traceback.format_exc()
                                        })
                self.logger.logger.info(log)
            raise e

        combinations_of_interests = sum(
            [list(map(list, itertools.combinations(interests, i))) for i in range(len(interests) + 1)], [])
        combinations_of_interests = list(sorted(combinations_of_interests, key=lambda x: len(x), reverse=True))

        for combination in combinations_of_interests:
            endpoint = self._external_services.targeting_search + ','.join(combination)
            value = self._get_top_interests(top_number=keyword.metric_count,
                                            endpoint=endpoint,
                                            headers=self._headers)
            if value:
                return value

        return ''

    def __find_audience_size(self, keyword: RuleTemplateKeyword):
        mc = (FacebookMetricCalculator().
              set_facebook_id(self._structure_id).
              set_level(self._level).
              set_metric(keyword.metric_name.value).
              set_repository(self._repository).
              set_business_owner_repo_session(self._business_owner_repo_session).
              set_facebook_config(self._facebook_config).
              set_business_owner_id(self._business_owner_id).
              set_date_stop(self._date_stop).
              set_debug_mode(self._debug).
              set_breakdown_metadata(BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                           action_breakdown=FacebookActionBreakdownEnum.NONE)))
        value, _ = mc.compute_value(atype=keyword.antecedent_type)

        return int(value)

    def __find_best_performing_ad_name(self, keyword):
        mc = (FacebookMetricCalculator().
              set_facebook_id(self._structure_id).
              set_level(self._level).
              set_metric(keyword.metric_name.value).
              set_repository(self._repository).
              set_business_owner_repo_session(self._business_owner_repo_session).
              set_facebook_config(self._facebook_config).
              set_business_owner_id(self._business_owner_id).
              set_date_stop(self._date_stop).
              set_debug_mode(self._debug).
              set_time_interval(self._time_interval).
              set_breakdown_metadata(BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.NONE,
                                                           action_breakdown=FacebookActionBreakdownEnum.NONE)))
        ad_id, ad_name = mc.compute_value(atype=keyword.antecedent_type)
        return ad_name
