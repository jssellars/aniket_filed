from Core.Dexter.Infrastructure.Domain.Breakdowns import BreakdownMetadataBase
from Core.Dexter.Infrastructure.Domain.ChannelEnum import ChannelEnum
from Core.Dexter.Infrastructure.Domain.DaysEnum import DaysEnum
from Core.Dexter.Infrastructure.Domain.LevelEnums import LevelEnum
from Core.Dexter.Infrastructure.Domain.LogicalOperatorEnum import LogicOperatorEnum
from Core.Dexter.Infrastructure.Domain.Rules.Antecedent import Antecedent
from Core.Dexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum
from Core.Dexter.Infrastructure.Domain.Rules.Connective import Connective
from Core.Dexter.Infrastructure.Domain.Rules.RuleBase import RuleBase
from FacebookDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.FacebookAvailableMetricEnum import \
    FacebookAvailableMetricEnum
from FacebookDexter.Infrastructure.Domain.Actions.ActionEnums import FacebookActionEnum
from FacebookDexter.Infrastructure.Domain.Breakdowns import FacebookBreakdownEnum, FacebookActionBreakdownEnum
from FacebookDexter.Infrastructure.Domain.FuzzyEngine.FacebookFuzzySets import FacebookLinguisticVariableEnum
from FacebookDexter.Infrastructure.Domain.Rules.FacebookRuleEnums import FacebookRuleTypeEnum, \
    FacebookRuleCategoryEnum, FacebookRuleImportanceEnum, FacebookRuleSourceEnum, FacebookRuleRedirectEnum

RULES_ADSET_REMOVE_GENDER = [
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.REMOVE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have "
                      "decreased by __id=1&value=null__% in the last __id=1&time_interval=7__ days for some of the "
                      "genders groups you are targeting. Dexter suggests you stop targeting the following genders "
                      "__id=1&breakdown_values=null__.",
             alternative_template="Dexter noticed your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ "
                                  "have decreased by __id=1&value=null__% in the last __id=1&time_interval=7__ days "
                                  "for all genders you are targeting. Dexter suggests you pause this ad set.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.GENDER,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.LOW),
                 Antecedent(aid=3,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.REMOVE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have "
                      "decreased by __id=1&value=null__% in the last __id=1&time_interval=7__ days for some of the "
                      "genders you are targeting. Dexter suggests you stop targeting the following genders "
                      "__id=1&breakdown_values=null__.",
             alternative_template="Dexter noticed your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ "
                                  "have decreased by __id=1&value=null__% in the last __id=1&time_interval=7__ days "
                                  "for all genders you are targeting. Dexter suggests you pause this ad set.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.GENDER,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.SPEND.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.LOW),
                 Antecedent(aid=3,
                            atype=AntecedentTypeEnum.FUZZY_TREND,
                            metric=FacebookAvailableMetricEnum.COST_PER_RESULT.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.INCREASING)
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.REMOVE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have "
                      "decreased by __id=1&value=null__% in the last __id=1&time_interval=7__ days for some of the "
                      "genders you are targeting. Dexter suggests you stop targeting the following genders "
                      "__id=1&breakdown_values=null__.",
             alternative_template="Dexter noticed your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ "
                                  "have decreased by __id=1&value=null__% in the last __id=1&time_interval=7__ days "
                                  "for all genders you are targeting. Dexter suggests you pause this ad set.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.GENDER,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.LOW),
             ]),
    RuleBase(rtype=FacebookRuleTypeEnum.AUDIENCE,
             channel=ChannelEnum.FACEBOOK,
             category=FacebookRuleCategoryEnum.OPTIMIZE_TARGETING,
             importance=FacebookRuleImportanceEnum.MEDIUM,
             source=FacebookRuleSourceEnum.DEXTER,
             level=LevelEnum.ADSET,
             action=FacebookActionEnum.REMOVE,
             redirect=FacebookRuleRedirectEnum.CAMPAIGN_MANAGER,
             template="Dexter noticed your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ have "
                      "decreased by __id=1&value=null__% in the last __id=1&time_interval=7__ days for some of the "
                      "genders you are targeting. Dexter suggests you stop targeting the "
                      "following genders __id=1&breakdown_values=null__.",
             alternative_template="Dexter noticed your __id=1&metric_name=RESULTS&metric_type=1&antecedent_type=8__ "
                                  "have decreased by __id=1&value=null__% in the last __id=1&time_interval=7__ days "
                                  "for all genders you are targeting. Dexter suggests you pause this ad set.",
             breakdown_metadata=BreakdownMetadataBase(breakdown=FacebookBreakdownEnum.GENDER,
                                                      action_breakdown=FacebookActionBreakdownEnum.NONE),
             time_interval=DaysEnum.THREE_MONTHS,
             connective=Connective(LogicOperatorEnum.AND),
             antecedents=[
                 Antecedent(aid=1,
                            atype=AntecedentTypeEnum.FUZZY_VALUE,
                            metric=FacebookAvailableMetricEnum.CPC.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=FacebookLinguisticVariableEnum.HIGH),
                 Antecedent(aid=2,
                            atype=AntecedentTypeEnum.VALUE,
                            metric=FacebookAvailableMetricEnum.RESULTS.value,
                            operator=LogicOperatorEnum.EQUALS,
                            expected_value=0),
             ])
]
