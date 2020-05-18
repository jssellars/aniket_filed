import hashlib
import typing
from datetime import datetime

from Core.Tools.Misc.ObjectSerializers import object_to_json
from FacebookDexter.Infrastructure.Constants import DEFAULT_DATETIME_ISO
from FacebookDexter.Infrastructure.Domain.Actions.ActionDetailsBuilder import ActionDetailsBuilder
from FacebookDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from FacebookDexter.Infrastructure.Domain.Metrics.Metric import MetricBase
from FacebookDexter.Infrastructure.Domain.Metrics.MetricEnums import MetricTypeEnum
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationEnums import \
    RecommendationOptimizationTypeEnum, RecommendationStatusEnum
from FacebookDexter.Infrastructure.Domain.Recommendations.RecommendationTemplateBuilder import \
    RecommendationTemplateBuilder
from FacebookDexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from FacebookDexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Infrastructure.Domain.Rules.RuleEvaluatorData import RuleEvaluatorData
from FacebookDexter.Infrastructure.PersistanceLayer.DexterMongoRepository import DexterMongoRepository


class RecommendationMetaInformationMapping:
    __mapping = {
        LevelEnum.CAMPAIGN: {"structure_id": "campaign_id",
                             "parent_id": "campaign_id",
                             "campaign_id": "campaign_id",
                             "structure_name": "campaign_name",
                             "parent_name": "campaign_name",
                             "campaign_name": "campaign_name",
                             "ad_account_id": "account_id"},
        LevelEnum.ADSET: {"structure_id": "adset_id",
                          "parent_id": "campaign_id",
                          "campaign_id": "campaign_id",
                          "structure_name": "adset_name",
                          "parent_name": "campaign_name",
                          "campaign_name": "campaign_name",
                          "ad_account_id": "account_id"},
        LevelEnum.AD: {"structure_id": "ad_id",
                       "parent_id": "adset_id",
                       "campaign_id": "campaign_id",
                       "structure_name": "ad_name",
                       "parent_name": "adset_name",
                       "campaign_name": "campaign_name",
                       "ad_account_id": "account_id"}
    }

    def __init__(self, level: LevelEnum = None):
        self.__level = level

    def apply_map(self, structure_meta_information: typing.Dict) -> typing.Dict:
        meta_information = {key: structure_meta_information.get(value) for key, value in
                            self.__mapping[self.__level].items()}
        meta_information["ad_account_id"] = self.__map_account_id(meta_information["ad_account_id"])
        return meta_information

    @staticmethod
    def __map_account_id(account_id: typing.AnyStr = None) -> typing.AnyStr:
        return "act_" + account_id


class RecommendationBuilder:

    def __init__(self, mongo_repository: DexterMongoRepository = None,
                 business_owner_repo_session: typing.Any = None,
                 facebook_config: typing.Any = None,
                 business_owner_id: typing.Any = None):
        self.__mongo_repository = mongo_repository
        self.__structure_details = None
        self.__business_owner_repo_session = business_owner_repo_session
        self.__facebook_config = facebook_config
        self.__business_owner_id = business_owner_id

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
        self.set_template(facebook_id, rule, rule_data, external_services)
        self.set_action_details(facebook_id, rule, rule_data)
        self.set_confidence(rule_data)
        self.set_meta_information(facebook_id, rule.level)
        self.last_updated_at = datetime.now().strftime(DEFAULT_DATETIME_ISO)
        self.__set_id()

        return self

    def _structure_details(self, facebook_id: typing.AnyStr = None, level: LevelEnum = None) -> typing.Dict:
        if not self.__structure_details:
            self.__structure_details = self.__mongo_repository.get_structure_details(key_value=facebook_id,
                                                                                     level=level)
        return self.__structure_details

    def set_optimization_type(self, optimization_type: RecommendationOptimizationTypeEnum = None) -> typing.Any:
        self.optimization_type = optimization_type
        return self

    def set_rule_metadata(self, rule: RuleBase = None) -> typing.Any:
        self.channel = rule.channel.value
        self.category = rule.category.value
        self.breakdown = rule.breakdown_metadata.breakdown.value.to_dict()
        self.action_breakdown = rule.breakdown_metadata.action_breakdown.value.to_dict()
        self.template = rule.template
        self.importance = rule.importance.value
        self.source = rule.source.value
        self.level = rule.level.value
        self.created_at = datetime.now().strftime(DEFAULT_DATETIME_ISO)
        self.recommendation_type = rule.type.value
        self.redirect_for_edit = rule.redirect.value
        return self

    def set_metrics(self, antecedents: typing.List[Antecedent] = None) -> typing.Any:
        self.metrics = [MetricBase(antecedent.metric.name, antecedent.metric.display_name) for antecedent in
                        antecedents
                        if antecedent.metric.type == MetricTypeEnum.INSIGHT]
        return self

    def set_template(self,
                     facebook_id: typing.AnyStr = None,
                     rule: RuleBase = None,
                     rule_data: typing.List[typing.List[RuleEvaluatorData]] = None,
                     external_services: typing.AnyStr = None):
        breakdown_values = self.__build_action_details_value(rule_data)
        self.template = (RecommendationTemplateBuilder(breakdown_values).
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
                         build_template(template=rule.template))
        return self

    def set_action_details(self,
                           facebook_id: typing.AnyStr = None,
                           rule: RuleBase = None,
                           rule_data: typing.List[typing.List[RuleEvaluatorData]] = None) -> typing.Any:
        action_details_builder = ActionDetailsBuilder()
        value = self.__build_action_details_value(rule_data)
        self.application_details = action_details_builder.build(action=rule.action,
                                                                breakdown=rule.breakdown_metadata.breakdown,
                                                                action_breakdown=rule.breakdown_metadata.action_breakdown,
                                                                structure_details=self._structure_details(facebook_id,
                                                                                                          rule.level),
                                                                value=value)
        return self

    @staticmethod
    def __build_action_details_value(rule_data: typing.List[typing.List[RuleEvaluatorData]]) -> typing.Any:
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
        mapper = RecommendationMetaInformationMapping(level)
        meta_information = mapper.apply_map(self._structure_details(facebook_id, level))
        for key, value in meta_information.items():
            setattr(self, key, value)
        return self

    def __set_id(self):
        hash_value = self.template + self.structure_id + self.level + self.breakdown['name'] + self.action_breakdown[
            'name']
        self.recommendation_id = hashlib.sha1(hash_value.encode('utf-8')).hexdigest()

    def to_dict(self):
        return object_to_json(self)
