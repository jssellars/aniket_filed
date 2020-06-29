import itertools
import re
import traceback
import typing
from collections import defaultdict

import requests

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata, BreakdownEnum, ActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.DaysEnum import DaysEnum
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Metrics.MetricCalculator import MetricCalculator
from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationTemplateBuilderBase import \
    RecommendationTemplateBuilderBase
from FacebookDexter.Infrastructure.Domain.RuleTemplateKeyword import RuleTemplateKeyword
from FacebookDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from FacebookDexter.Infrastructure.FuzzyEngine.FuzzySets.FuzzySets import LinguisticVariableEnum


class RecommendationTemplateBuilder(RecommendationTemplateBuilderBase):
    __keywords_map = {
        "time_interval": DaysEnum,
        "metric_name": AvailableMetricEnum.get_enum_by_name,
        "metric_type": MetricTypeEnum,
        "antecedent_type": AntecedentTypeEnum,
        "linguistic_variable": LinguisticVariableEnum,
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
            'linguistic_variable': lambda x: LinguisticVariableEnum(x).name,
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
                    return None
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
                if keyword.metric_type == MetricTypeEnum.INSIGHT:
                    value = self.__find_insight_value(keyword)
                elif keyword.metric_type == MetricTypeEnum.INTERESTS:
                    value = self.__find_suggested_interests(keyword)
                elif keyword.metric_type == MetricTypeEnum.AUDIENCE:
                    value = self.__find_audience_size(keyword)
                elif keyword.metric_type == MetricTypeEnum.DUPLICATE_AD:
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
        mc = (MetricCalculator().
            set_facebook_id(self._structure_id).
            set_level(self._level).
            set_metric(keyword.metric_name.value).
            set_repository(self._repository).
            set_date_stop(self._date_stop).
            set_time_interval(keyword.time_interval).
            set_debug_mode(self._debug).
            set_breakdown_metadata(
            BreakdownMetadata(breakdown=BreakdownEnum.NONE, action_breakdown=ActionBreakdownEnum.NONE)))
        value, _ = mc.compute_value(atype=keyword.antecedent_type, time_interval=keyword.time_interval)

        if value is not None:
            value = abs(int(value))

        return value

    def _get_top_interests(self, top_number, endpoint, headers):
        # todo: get must have auth
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

        token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJiZWFiYWM0NC02NzdkLTQ0MTAtOWJkMy0xMWQxMWY3MTIxYTgiLCJzdWIiOiJhbmRyZWlAZmlsZWQuY29tIiwiVXNlckRldGFpbHNLZXkiOiJ7XCJGaWxlZElkXCI6OCxcIkZpbGVkRmlyc3ROYW1lXCI6XCJBbmRyZWlcIixcIkZpbGVkTGFzdE5hbWVcIjpcIkx1Y2hpY2lcIixcIkZpbGVkUGFyZW50SWRcIjoyLFwiRmFjZWJvb2tCdXNpbmVzc093bmVySWRcIjpcIjE2MjM5NTA2NjEyMzA4NzVcIixcIlJvbGVzXCI6WzVdLFwiQWNjb3VudFN0YXRlXCI6MSxcIkZhY2Vib29rQWRBY2NvdW50UGVybWlzc2lvbnNcIjp7XCJJZHNcIjpbXCJhY3RfMTAxNTIwODIxMDg3MTc5MDlcIixcImFjdF8xMDIwMDg1NjI1NDQwMzM3MVwiLFwiYWN0XzEwNDE2OTQyNzYxNjM1NzlcIixcImFjdF8xMDUwNDA5NDMxOTY5ODZcIixcImFjdF8xMDY1MDY3MDMzMDU2MjFcIixcImFjdF8xMTM2MTE3NDA5OTIxMzA2XCIsXCJhY3RfMTE1NjY4Nzk5MzAxNDU4XCIsXCJhY3RfMTE4MTUzMzAyMDAxODkwXCIsXCJhY3RfMTIwMzYxODI4NjM4MTM4NFwiLFwiYWN0XzEyNDY3ODcyMTMyNTExNFwiLFwiYWN0XzEyNDgwNjg1MTIwNTIwNzZcIixcImFjdF8xMzAzNTM1ODY5NzEyNjc5XCIsXCJhY3RfMTMwNjM3OTZcIixcImFjdF8xMzA5MjgzMjQ5MjY5OTc4XCIsXCJhY3RfMTM0ODQ1NjEzMTk5MTg4NlwiLFwiYWN0XzE0NDQ4ODM0XCIsXCJhY3RfMTUyMjI2NDE2ODA2NjE5MlwiLFwiYWN0XzE1MjY0NzIxODIwNDY4N1wiLFwiYWN0XzE1NDAyOTI5MjI3NjE0ODdcIixcImFjdF8xNjU0ODY5NTMxMzI4NzU5XCIsXCJhY3RfMTY5MzUyODY2NTM0MDEyXCIsXCJhY3RfMTcwMDEyNDQxMDgzODE5XCIsXCJhY3RfMTcyMTQ5Mzk4NzkxNzU1N1wiLFwiYWN0XzE3MjM5ODU0NTQ0ODE3NThcIixcImFjdF8xNzI1NzgwNTc0MzAyMjQ2XCIsXCJhY3RfMTcyNTc4MDYzMDk2ODkwN1wiLFwiYWN0XzE3MjY4NDY0MDc1Mjg5OTZcIixcImFjdF8xNzc3NzA0MjY5MTE0MTU4XCIsXCJhY3RfMTc5NTEyMTI1MDUzNTc3OFwiLFwiYWN0XzE4MTAzMjU4MjI1MTQzODdcIixcImFjdF8xODI1NTU5ODI4NTU4OTRcIixcImFjdF8xODM0MzcwNjczMjQ1OTE1XCIsXCJhY3RfMTg1MzE2NTE5NTgyMTY0XCIsXCJhY3RfMTg5Njc3MDk3NzAwNTg4NFwiLFwiYWN0XzE4OTgzOTc4MzAzNzM4NTJcIixcImFjdF8xOTIxNjM3MTM0NzE2NTg4XCIsXCJhY3RfMTkzNjE5OTMxMTkxNDI1XCIsXCJhY3RfMTk2NjI1Njk4NjkyMTI2OVwiLFwiYWN0XzE5ODI2NzY1NzUyNzkzMTBcIixcImFjdF8yMDM1OTU1NzA4NzY2MTVcIixcImFjdF8yMDQyMzEzMjE5MTUxMDI4XCIsXCJhY3RfMjA2NjkwNDQ2MDE4OTg1NFwiLFwiYWN0XzIwNzY3OTc4Mzc4MTA4MlwiLFwiYWN0XzIyMTAyNjA5NTIzNDMwNTdcIixcImFjdF8yMjE3NDM5MDM4NTAxMTQ4XCIsXCJhY3RfMjI1MDg1MTkxOTQ1NDU5XCIsXCJhY3RfMjMxOTMyNzczMTcyMTExMlwiLFwiYWN0XzIzNDU4MzE4OTU2NjY1MjJcIixcImFjdF8yMzU1ODc3NDExMTg2MzBcIixcImFjdF8yMzgxNzkwNzQxODY4NzM1XCIsXCJhY3RfMjQyMjExMDEwMTg0MzUxXCIsXCJhY3RfMjQ1MTA0NTcyODU0MjQzNFwiLFwiYWN0XzI0Njc1ODc1OTM1NTgyMVwiLFwiYWN0XzI1MjY0NDEwMjY0OTM3OVwiLFwiYWN0XzI1MzkzOTYxOTE2NzgyNVwiLFwiYWN0XzI2MTg3NTExNlwiLFwiYWN0XzI3MzUzODc4OTk0NzE4NlwiLFwiYWN0XzI3NTU3ODc4NFwiLFwiYWN0XzI5MDg2NDY5NDI1MzM2MjNcIixcImFjdF8yOTU3NDg5NVwiLFwiYWN0XzMwNjIwNjEyNzA1MTI4ODdcIixcImFjdF8zNTY4MzU4NzE0NzEzOTFcIixcImFjdF8zNzc5NzkxNFwiLFwiYWN0XzM4OTEwOTE1ODU4ODA2NVwiLFwiYWN0XzQwMDgxNDEwMDg0NTAxMlwiLFwiYWN0XzQwMjk0MTI4Njc5NzgxMFwiLFwiYWN0XzQwMzg1NzM3Njk4MjkyMFwiLFwiYWN0XzQyMDc0NjM5NTQ4NDc1OVwiLFwiYWN0XzQ0NjQyNDkxMjM1OTkyM1wiLFwiYWN0XzQ1MzAxMzkwMjAyNjUxNFwiLFwiYWN0XzQ4MTgxODUyNTcxNjc4MFwiLFwiYWN0XzQ5NDY4MDgxODA5Mzc5MVwiLFwiYWN0XzUxNDc4ODc1OTM4MDczM1wiLFwiYWN0XzUyMTI3OTg4XCIsXCJhY3RfNTIyOTYyNDg4NDI0MTUyXCIsXCJhY3RfNTIzODY2Nzg1MDEwNTgzXCIsXCJhY3RfNTI1NzEwMTg0NTY2NDE0XCIsXCJhY3RfNTU5MzExOTMxMjE3NDI3XCIsXCJhY3RfNTc0NDEwOTI5ODU2NjExXCIsXCJhY3RfNjA0MzQ4NDgzNzUyODY1XCIsXCJhY3RfNjI4NTQ0NTBcIixcImFjdF82MzUwNzAzODM2NTU1OTBcIixcImFjdF83MDk2OTU3MFwiLFwiYWN0Xzc0NDE5OTAwOTM1NTA4OFwiLFwiYWN0Xzc1Njg4MjIzMTM5OTExN1wiLFwiYWN0Xzc5MjM2NTYxNzQ5NjM3NlwiLFwiYWN0Xzg0NjYyMTIyMjM2MjI4NFwiLFwiYWN0Xzg2MTgxMjQ2NzU5NzAwMVwiLFwiYWN0Xzg2NzMxMjg1NzAyMzUwNVwiLFwiYWN0XzkwODA2MjQ5NjMxODE5NlwiLFwiYWN0Xzk4MjA4NTMwODgxMTg5OFwiLFwiYWN0Xzk4NDk0Mzg3MTU2NDgzNFwiXSxcIlJvbGVzXCI6WzAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMCwwLDAsMF19LFwiRmFjZWJvb2tCdXNpbmVzc1Blcm1pc3Npb25zXCI6e1wiSWRzXCI6W1wiMTM3NTM5MjQ0MzQzMzc5XCIsXCIxNzIxMjg1OTQ4MDg1MDQyXCIsXCIxNzg5OTAzNTAxMTYwNjBcIixcIjMxNjAwNjg2NTU2OTM0N1wiLFwiMzM0NzE2MDQwNzA3ODM0XCIsXCI0NzQ4NDQ4ODMxMjExMTJcIixcIjUyMDA5ODE3NDg1MDUzOVwiXSxcIlJvbGVzXCI6WzAsMCwwLDAsMCwwLDBdfSxcIklzRnJvbnRPZmZpY2VVc2VyXCI6dHJ1ZX0iLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJGYWNlYm9vayBCdXNpbmVzcyBPd25lciIsImV4cCI6MTU5ODEzNjE5OCwiaXNzIjoiRmlsZWQtVG9rZW4tSXNzdWVyIiwiYXVkIjoiRmlsZWQtQ2xpZW50LUFwcHMifQ.H7tPnXOwPqzak0UlPOQ_5sCvpUqkA3E50Exk2u0_ZoU'
        headers = {'Authorization': 'Bearer ' + token}
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
                                            headers=headers)
            if value:
                return value

        return ''

    def __find_audience_size(self, keyword: RuleTemplateKeyword):
        mc = (MetricCalculator().
              set_facebook_id(self._structure_id).
              set_level(self._level).
              set_metric(keyword.metric_name.value).
              set_repository(self._repository).
              set_business_owner_repo_session(self._business_owner_repo_session).
              set_facebook_config(self._facebook_config).
              set_business_owner_id(self._business_owner_id).
              set_date_stop(self._date_stop).
              set_debug_mode(self._debug).
              set_breakdown_metadata(BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                       action_breakdown=ActionBreakdownEnum.NONE)))
        value, _ = mc.compute_value(atype=keyword.antecedent_type)

        return int(value)

    def __find_best_performing_ad_name(self, keyword):
        mc = (MetricCalculator().
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
              set_breakdown_metadata(BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                       action_breakdown=ActionBreakdownEnum.NONE)))
        ad_id, ad_name = mc.compute_value(atype=keyword.antecedent_type)
        return ad_name
