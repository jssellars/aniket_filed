import typing
from datetime import datetime, timedelta

from Core.Tools.Logger.LoggerMessageBase import LoggerMessageBase, LoggerMessageTypeEnum
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.Metrics.AvailableMetricEnum import AvailableMetricEnum
from GoogleDexter.Engine.Algorithms.FuzzyRuleBasedOptimization.RuleBasedOptimizationBase import \
    RuleBasedOptimizationBase
from GoogleDexter.Infrastructure.Constants import DEFAULT_DATETIME_ISO
from GoogleDexter.Infrastructure.Domain.Breakdowns import BreakdownMetadata, BreakdownEnum, ActionBreakdownEnum
from GoogleDexter.Infrastructure.Domain.LevelEnums import LevelEnum
from GoogleDexter.Infrastructure.Domain.Metrics.MetricCalculator import MetricCalculator
from GoogleDexter.Infrastructure.Domain.Rules.AntecedentEnums import AntecedentTypeEnum


class RuleBasedOptimizationCampaignLevel(RuleBasedOptimizationBase):

    def __init__(self):
        super().__init__()
        self.set_level(LevelEnum.CAMPAIGN)

    def run(self, campaign_id: typing.AnyStr = None) -> typing.List[typing.Dict]:
        recommendations = []

        if self.is_available(campaign_id):
            recommendations += self.evaluate_general_rules(campaign_id, self._fuzzyfier_factory)
            recommendations += self.evaluate_create_rules(campaign_id, self._fuzzyfier_factory)

        return recommendations

    def check_run_status(self, campaign_id):
        if self.__check_last_x_days_since_update(campaign_id):
            return True

        return self.__check_in_last_x_days(campaign_id)

    def __check_in_last_x_days(self, campaign_id):
        date_stop = self._date_stop
        date_start = date_stop - timedelta(days=self._dexter_config.days_since_last_change)
        breakdown_metadata = BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                               action_breakdown=ActionBreakdownEnum.NONE)
        time_interval = (date_stop - date_start).days

        results, _ = (MetricCalculator().
                      set_metric(AvailableMetricEnum.RESULTS.value).
                      set_breakdown_metadata(breakdown_metadata).
                      set_structure_id(campaign_id).
                      set_repository(self._mongo_repository).
                      set_level(self._level).
                      set_date_stop(self._date_stop).
                      compute_value(atype=AntecedentTypeEnum.VALUE, time_interval=time_interval))

        if results < self._dexter_config.min_results:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="RuleBasedOptimizationCampaignLevel",
                                    description=f"Campaign {campaign_id} has less than {self._dexter_config.min_results} results",
                                    extra_data={
                                        "values": results,
                                        "structure_id": campaign_id,
                                        "config": self._dexter_config
                                    })
            self.get_logger().logger.info(log)
            return False
        else:
            return True

    def __check_last_x_days_since_update(self, campaign_id):
        structure_details = self._mongo_repository.get_structure_details(key_value=campaign_id,
                                                                         level=LevelEnum.CAMPAIGN)
        updated_time = structure_details.get('updated_time').split("+")[0]
        updated_time = datetime.strptime(updated_time, DEFAULT_DATETIME_ISO)
        date_stop = self._date_stop.date()

        if (date_stop - updated_time).days >= self._dexter_config.recommendation_days_last_updated:
            breakdown_metadata = BreakdownMetadata(breakdown=BreakdownEnum.NONE,
                                                   action_breakdown=ActionBreakdownEnum.NONE)
            time_interval_days = (date_stop - updated_time).days
            results, _ = (MetricCalculator().
                          set_metric(AvailableMetricEnum.RESULTS.value).
                          set_breakdown_metadata(breakdown_metadata).
                          set_structure_id(campaign_id).
                          set_repository(self._mongo_repository).
                          set_level(self._level).
                          compute_value(atype=AntecedentTypeEnum.VALUE, time_interval=time_interval_days))

            if results > self._dexter_config.min_results:
                return True
            else:
                log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                        name="RuleBasedOptimizationCampaignLevel",
                                        description=f"Campaign {campaign_id} has less than {self._dexter_config.min_results} results",
                                        extra_data={
                                            "values": results,
                                            "structure_id": campaign_id,
                                            "config": self._dexter_config
                                        })
                self.get_logger().logger.info(log)

        else:
            log = LoggerMessageBase(mtype=LoggerMessageTypeEnum.WARNING,
                                    name="RuleBasedOptimizationCampaignLevel",
                                    description=f"A more recent change was not made for {campaign_id} in the last"
                                                f" {self._dexter_config.days_since_last_change} days",
                                    extra_data={
                                        "structure_id": campaign_id,
                                        "config": self._dexter_config
                                    })
            self.get_logger().logger.info(log)

        return False