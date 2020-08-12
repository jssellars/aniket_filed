import hashlib
import typing
from datetime import datetime

from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.Metrics.Metric import MetricBase
from Core.Dexter.Infrastructure.Domain.Recommendations.RecommendationEnums import RecommendationOptimizationTypeEnum, \
    RecommendationStatusEnum
from Core.Dexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from Core.Dexter.Infrastructure.Domain.Rules.RuleEvaluatorData import RuleEvaluatorData
from Core.Tools.Misc.Constants import DEFAULT_DATETIME_ISO
from Core.Tools.Misc.ObjectSerializers import object_to_json
from FacebookDexter.Engine.Algorithms.FacebookRecommendationEnhancer.FacebookRecommendationEnum import \
    FacebookRecommendationImportanceEnum
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.FacebookAvailableMetricEnum import \
    FacebookAvailableMetricEnum
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookGenderEnum
from FacebookDexter.Infrastructure.Domain.Actions.FacebookActionDetailsBuilder import FacebookActionDetailsBuilder
from FacebookDexter.Infrastructure.Domain.Breakdowns import FacebookBreakdownEnum, FacebookActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.Metrics.FacebookMetricEnums import FacebookMetricTypeEnum
from FacebookDexter.Infrastructure.Domain.Recommendations.FacebookRecommendationMetaInformationMapping import \
    FacebookRecommendationMetaInformationMapping
from FacebookDexter.Infrastructure.Domain.Recommendations.FacebookRecommendationTemplateBuilder import \
    FacebookRecommendationTemplateBuilder
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleRedirectEnum, \
    FacebookRuleTypeEnum, FacebookRuleSourceEnum, FacebookRuleCategoryEnum
from FacebookDexter.Infrastructure.PersistanceLayer.FacebookDexterMongoRepository import FacebookDexterMongoRepository


class FacebookRecommendationBuilder:

    def __init__(self, mongo_repository: FacebookDexterMongoRepository = None,
                 business_owner_repo_session: typing.Any = None,
                 facebook_config: typing.Any = None,
                 business_owner_id: typing.Any = None,
                 date_stop: typing.AnyStr = None,
                 time_interval: DaysEnum = DaysEnum.MONTH,
                 debug_mode=None,
                 headers: typing.AnyStr = None):
        self.__mongo_repository = mongo_repository
        self.__business_owner_repo_session = business_owner_repo_session
        self.__facebook_config = facebook_config
        self.__business_owner_id = business_owner_id
        self.__use_alternative_template = False
        self._date_stop = date_stop
        self._debug = debug_mode
        self._headers = headers

        self.time_interval = time_interval
        self.recommendation_id = None
        self.category = None
        self.metrics = []
        self.breakdown = None
        self.action_breakdown = None
        self.channel = None
        self.level = None
        self.optimization_type = RecommendationOptimizationTypeEnum.RULE_BASED.value
        self.recommendation_type = None
        self.confidence = None
        self.importance = None
        self.source = None
        self.created_at = None
        self.template = None
        self.application_details = None
        self.redirect_for_edit = None
        self.structure_id = None  # for campaign, structure, parent, and campaign id have the same value
        self.parent_id = None
        self.campaign_id = None
        self.ad_account_id = None  # act_12345
        self.structure_name = None
        self.parent_name = None
        self.campaign_name = None
        self.status = RecommendationStatusEnum.ACTIVE.value
        self.last_updated_at = None
        # for campaigns, structure, parent, and campaign name have the same value

    def __eq__(self, other) -> bool:
        return self.recommendation_id == other.recommendation_id

    def create(self,
               facebook_id: typing.AnyStr = None,
               rule: RuleBase = None,
               rule_data: typing.List[typing.List[RuleEvaluatorData]] = None,
               optimization_type: RecommendationOptimizationTypeEnum = RecommendationOptimizationTypeEnum.RULE_BASED,
               external_services: typing.Any = None) -> typing.Any:
        self.set_rule_metadata(rule)
        self.set_optimization_type(optimization_type)
        self.set_metrics(rule.antecedents)
        self.set_action_details(facebook_id, rule, rule_data)
        self.set_template(facebook_id, rule, rule_data, external_services)
        self.set_confidence(rule_data)
        self.set_meta_information(facebook_id, rule.level)
        self.last_updated_at = datetime.now().strftime(DEFAULT_DATETIME_ISO)
        # self.set_output_extra_information()
        self.__set_id()

        return self

    def create_facebook_recommendation(self, facebook_id: typing.AnyStr = None,
                                       level: LevelEnum = None,
                                       template: typing.AnyStr = None,
                                       confidence: float = None,
                                       importance: FacebookRecommendationImportanceEnum = None):
        self.category = FacebookRuleCategoryEnum.IMPROVE_CPR.value
        self.metrics = [MetricBase(name='cpc_all', display_name="CPC")]
        self.breakdown = FacebookBreakdownEnum.NONE.value.to_dict()
        self.action_breakdown = FacebookActionBreakdownEnum.NONE.value.to_dict()
        self.channel = ChannelEnum.FACEBOOK.value
        self.optimization_type = RecommendationOptimizationTypeEnum.FACEBOOK.value
        self.recommendation_type = FacebookRuleTypeEnum.PERFORMANCE.value
        self.source = FacebookRuleSourceEnum.FACEBOOK.value
        self.created_at = datetime.now().strftime(DEFAULT_DATETIME_ISO)
        self.application_details = {}
        self.redirect_for_edit = FacebookRuleRedirectEnum.CAMPAIGN_MANAGER.value
        self.set_meta_information(facebook_id=facebook_id, level=level)
        self.status = RecommendationStatusEnum.ACTIVE.value
        self.last_updated_at = datetime.now().strftime(DEFAULT_DATETIME_ISO)
        self.level = level.value
        self.template = template
        self.confidence = confidence
        self.importance = importance.value
        self.__set_id()

        return self

    def _structure_details(self, facebook_id: typing.AnyStr = None, level: LevelEnum = None) -> typing.Dict:
        return self.__mongo_repository.get_structure_details(key_value=facebook_id, level=level)

    def set_optimization_type(self, optimization_type: RecommendationOptimizationTypeEnum = None) -> typing.Any:
        self.optimization_type = optimization_type
        return self

    def set_rule_metadata(self, rule: RuleBase = None) -> typing.Any:
        self.channel = rule.channel.value
        self.category = rule.category.value
        self.breakdown = rule.breakdown_metadata.breakdown.value
        self.action_breakdown = rule.breakdown_metadata.action_breakdown.value
        self.template = rule.template
        self.importance = rule.importance.value
        self.source = rule.source.value
        # required by FE. will change after FE refactor
        self.level = rule.level.value if rule.level != LevelEnum.ADSET else 'adSet'
        self.created_at = datetime.now().strftime(DEFAULT_DATETIME_ISO)
        self.recommendation_type = rule.type.value
        self.redirect_for_edit = rule.redirect.value
        return self

    def set_metrics(self, antecedents: typing.List[Antecedent] = None) -> typing.Any:
        antecedent_metrics = [MetricBase(antecedent.metric.name, antecedent.metric.display_name)
                              for antecedent in antecedents
                              if antecedent.metric.type == FacebookMetricTypeEnum.INSIGHT]

        for metric in antecedent_metrics:
            current_metrics = [metric.name for metric in self.metrics]
            if metric.name not in current_metrics:
                self.metrics.append(metric)

        if not self.metrics:
            self.metrics = [MetricBase(FacebookAvailableMetricEnum.CPC.value.name,
                                       FacebookAvailableMetricEnum.CPC.value.display_name)]

        return self

    def set_template(self,
                     facebook_id: typing.AnyStr = None,
                     rule: RuleBase = None,
                     rule_data: typing.List[typing.List[RuleEvaluatorData]] = None,
                     external_services: typing.AnyStr = None):
        breakdown_values = self.__build_action_details_value(rule_data=rule_data)
        # FB has an UNKNOWN gender value. we need to remove it from the template, as you cannot directly specify
        # it on FB
        if rule.breakdown_metadata.breakdown == FacebookBreakdownEnum.GENDER:
            breakdown_values = [value for value in breakdown_values if value != FacebookGenderEnum.UNKNOWN.value[0]]
        elif rule.breakdown_metadata.breakdown == FacebookBreakdownEnum.PLACEMENT:
            breakdown_values = [value.replace(", ", "-") for value in breakdown_values]

        self.template = (FacebookRecommendationTemplateBuilder(breakdown_values).
                         set_repository(self.__mongo_repository).
                         set_structure_id(facebook_id).
                         set_level(rule.level).
                         set_breakdown(rule.breakdown_metadata.breakdown).
                         set_action_breakdown(rule.breakdown_metadata.action_breakdown).
                         set_external_services(external_services).
                         set_ad_account_id(ad_account_id=self.ad_account_id).
                         set_business_onwer_repo_session(self.__business_owner_repo_session).
                         set_facebook_config(self.__facebook_config).
                         set_business_owner_id(self.__business_owner_id).
                         set_date_stop(self._date_stop).
                         set_time_interval(self.time_interval).
                         set_headers(self._headers).
                         set_debug_mode(self._debug).
                         set_rule(rule))

        if self.__use_alternative_template:
            self.template = self.template.build_template(template=rule.alternative_template)
        else:
            self.template = self.template.build_template(template=rule.template)

        return self

    def set_action_details(self,
                           facebook_id: typing.AnyStr = None,
                           rule: RuleBase = None,
                           rule_data: typing.List[typing.List[RuleEvaluatorData]] = None) -> typing.Any:
        action_details_builder = FacebookActionDetailsBuilder(facebook_id=facebook_id,
                                                              repository=self.__mongo_repository,
                                                              time_interval=self.time_interval,
                                                              debug=self._debug,
                                                              date_stop=self._date_stop)
        value = self.__build_action_details_value(rule_data)
        self.application_details, self.__use_alternative_template = \
            action_details_builder.build(action=rule.action,
                                         breakdown=rule.breakdown_metadata.breakdown,
                                         action_breakdown=rule.breakdown_metadata.action_breakdown,
                                         structure_details=self._structure_details(
                                             facebook_id=facebook_id,
                                             level=rule.level),
                                         value=value)
        return self

    def __build_action_details_value(self,
                                     rule_data: typing.List[typing.List[RuleEvaluatorData]] = None) -> \
            typing.Union[typing.List[typing.AnyStr], typing.List[int]]:
        value = [data.breakdown_metadata.breakdown_value
                 for rule_data_entry in rule_data
                 for data in rule_data_entry
                 if data.breakdown_metadata.breakdown_value is not None]
        return list(set(value))

    def set_confidence(self, rule_data: typing.List[typing.List[RuleEvaluatorData]] = None) -> typing.Any:
        confidence = 1.0
        for rule_data_entry in rule_data:
            for value in rule_data_entry:
                if value.metric_value_confidence and value.metric_value_confidence < confidence:
                    confidence = value.metric_value_confidence
        self.confidence = confidence
        return self

    def set_meta_information(self, facebook_id: typing.AnyStr = None, level: LevelEnum = None) -> typing.NoReturn:
        mapper = FacebookRecommendationMetaInformationMapping(level)
        meta_information = mapper.apply_map(self._structure_details(facebook_id, level))
        for key, value in meta_information.items():
            setattr(self, key, value)
        return self

    def __set_id(self):
        try:
            hash_value = self.structure_id + self.level + self.breakdown.name + self.action_breakdown.name \
                         + "".join([metric.display_name for metric in self.metrics])
            self.recommendation_id = hashlib.sha1(hash_value.encode('utf-8')).hexdigest()
        except Exception as e:
            self.recommendation_id = None
            print(e)

    def to_dict(self):
        return object_to_json(self)
